"""
MVE: GNN vs FC on graph matching scheduling problem.
Verifies structural advantage of GNN on max-weight matching (ISL scheduling core subproblem).
"""

import random
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
import torch_geometric
from torch_geometric.nn import GATv2Conv
from torch_geometric.data import Data
import networkx as nx
import warnings
warnings.filterwarnings("ignore")

# ── Reproducibility ──
SEED = 42
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)

# ── Problem Parameters ──
N_NODES = 20
N_INSTANCES = 2000
DIST_THRESHOLD = 0.5
TRAIN_RATIO = 0.8
N_TRAIN = int(N_INSTANCES * TRAIN_RATIO)
N_TEST = N_INSTANCES - N_TRAIN

# ── Training Parameters ──
BATCH_SIZE = 32
EPOCHS = 100
LR = 1e-3
PATIENCE = 10

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# ══════════════════════════════════════════
# Data Generation
# ══════════════════════════════════════════

def generate_instance():
    """Generate one random geometric graph + optimal matching."""
    positions = np.random.rand(N_NODES, 2)

    G = nx.Graph()
    for i in range(N_NODES):
        G.add_node(i, pos=positions[i])

    edges = []
    edge_features = []
    for i in range(N_NODES):
        for j in range(i + 1, N_NODES):
            dist = np.linalg.norm(positions[i] - positions[j])
            if dist < DIST_THRESHOLD:
                weight = 1.0 / (dist + 0.1)
                G.add_edge(i, j, weight=weight, distance=dist)
                edges.append((i, j))
                edge_features.append([dist, weight])

    if len(edges) == 0:
        return generate_instance()  # retry if no edges

    # Optimal matching
    matching = nx.max_weight_matching(G, maxcardinality=False, weight="weight")
    matched_edges = set()
    for u, v in matching:
        if u > v:
            u, v = v, u
        matched_edges.add((u, v))

    return {
        "positions": positions,
        "edges": edges,
        "edge_features": np.array(edge_features, dtype=np.float32),
        "matched": np.array([1.0 if e in matched_edges else 0.0 for e in edges], dtype=np.float32),
        "optimal_weight": sum(G[u][v]["weight"] for u, v in matching),
    }


def greedy_matching(pred_probs, edges, n_nodes):
    """Greedy matching from predicted probabilities. Returns total weight."""
    paired = set()
    total_weight = 0.0
    # Sort by predicted probability descending
    order = np.argsort(-pred_probs)
    for idx in order:
        u, v = edges[idx]
        if u not in paired and v not in paired:
            paired.add(u)
            paired.add(v)
            # weight = 1.0 / (distance + 0.1), but we use the true weight
            dist = np.sqrt((1.0 - 0) + 0)  # placeholder; we pass real weight below
            total_weight += 1.0  # will be replaced with actual weight
    return total_weight


def greedy_matching_with_weights(pred_probs, edges, edge_features):
    """Greedy matching from predicted probabilities using true weights."""
    paired = set()
    total_weight = 0.0
    order = np.argsort(-pred_probs)
    for idx in order:
        u, v = edges[idx]
        if u not in paired and v not in paired:
            paired.add(u)
            paired.add(v)
            total_weight += edge_features[idx, 1]  # true weight
    return total_weight


# ══════════════════════════════════════════
# Dataset for GNN (PyG)
# ══════════════════════════════════════════

class GraphMatchingDataset(Dataset):
    def __init__(self, instances):
        self.instances = instances

    def __len__(self):
        return len(self.instances)

    def __getitem__(self, idx):
        inst = self.instances[idx]
        pos = torch.tensor(inst["positions"], dtype=torch.float32)
        edges = inst["edges"]
        edge_feat = torch.tensor(inst["edge_features"], dtype=torch.float32)
        labels = torch.tensor(inst["matched"], dtype=torch.float32)

        # Build edge_index (undirected: add both directions)
        src = [e[0] for e in edges] + [e[1] for e in edges]
        dst = [e[1] for e in edges] + [e[0] for e in edges]
        edge_index = torch.tensor([src, dst], dtype=torch.long)

        # Edge features duplicated for both directions
        edge_attr = torch.cat([edge_feat, edge_feat], dim=0)

        return pos, edge_index, edge_attr, labels, torch.tensor(len(edges))


def gnn_collate(batch):
    """Custom collate for variable-size graphs."""
    pos_list, ei_list, ea_list, label_list, nedge_list = [], [], [], [], []
    offset = 0
    for pos, ei, ea, labels, ne in batch:
        pos_list.append(pos)
        ei_list.append(ei + offset)
        ea_list.append(ea)
        # Labels are per-original-edge, need to track which edges are original
        label_list.append(labels)
        nedge_list.append(ne)
        offset += pos.size(0)

    return (
        torch.cat(pos_list, dim=0),
        torch.cat(ei_list, dim=1),
        torch.cat(ea_list, dim=0),
        label_list,
        nedge_list,
    )


# ══════════════════════════════════════════
# GNN Model (GATv2)
# ══════════════════════════════════════════

class GNNMatcher(nn.Module):
    def __init__(self, node_dim=2, edge_dim=2, hidden=32, heads=4):
        super().__init__()
        self.node_enc = nn.Linear(node_dim, hidden)
        self.edge_enc = nn.Linear(edge_dim, hidden)

        self.conv1 = GATv2Conv(hidden, hidden // heads, heads=heads, edge_dim=hidden, add_self_loops=False)
        self.conv2 = GATv2Conv(hidden, hidden // heads, heads=heads, edge_dim=hidden, add_self_loops=False)

        self.edge_mlp = nn.Sequential(
            nn.Linear(hidden * 3, hidden),
            nn.ReLU(),
            nn.Linear(hidden, 1),
        )

    def forward(self, x, edge_index, edge_attr, n_original_edges_list):
        # Node encoding
        h = self.node_enc(x)
        # Edge encoding
        e = self.edge_enc(edge_attr)

        # GNN layers
        h = F.elu(self.conv1(h, edge_index, e))
        h = F.elu(self.conv2(h, edge_index, e))

        # Edge prediction: for each original (undirected) edge, take src+dst+edge_emb
        # edge_index has 2*n_original_edges rows (both directions)
        # We only take the first n_original_edges (src→dst direction)
        outputs = []
        offset = 0
        for ne in n_original_edges_list:
            # First ne edges in the batch segment are src→dst
            src_idx = edge_index[0, offset:offset + ne]
            dst_idx = edge_index[1, offset:offset + ne]

            src_h = h[src_idx]
            dst_h = h[dst_idx]
            # Edge attributes for forward direction only
            e_fwd = e[offset:offset + ne]

            edge_repr = torch.cat([src_h, dst_h, e_fwd], dim=-1)
            pred = torch.sigmoid(self.edge_mlp(edge_repr)).squeeze(-1)
            outputs.append(pred)
            offset += ne * 2  # skip both directions

        return outputs


# ══════════════════════════════════════════
# FC Model (3-layer MLP on flattened adjacency)
# ══════════════════════════════════════════

class FCMatcher(nn.Module):
    def __init__(self, n_nodes=N_NODES, feat_dim=2):
        super().__init__()
        self.n_nodes = n_nodes
        self.feat_dim = feat_dim
        input_dim = n_nodes * n_nodes * feat_dim

        self.net = nn.Sequential(
            nn.Linear(input_dim, 512),
            nn.ReLU(),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Linear(256, n_nodes * n_nodes),
        )

    def forward(self, adj_features):
        """adj_features: (B, N, N, 2) — flattened full adjacency features."""
        B = adj_features.size(0)
        x = adj_features.view(B, -1)
        out = self.net(x)
        out = torch.sigmoid(out)
        out = out.view(B, self.n_nodes, self.n_nodes)
        return out


# ══════════════════════════════════════════
# Build FC Dataset
# ══════════════════════════════════════════

def build_fc_features(instance):
    """Build (N, N, 2) adjacency feature matrix."""
    adj = np.zeros((N_NODES, N_NODES, 2), dtype=np.float32)
    for idx, (u, v) in enumerate(instance["edges"]):
        feat = instance["edge_features"][idx]
        adj[u, v] = feat
        adj[v, u] = feat
    return adj

def build_fc_labels(instance):
    """Build (N, N) label matrix (upper triangle only matters)."""
    labels = np.zeros((N_NODES, N_NODES), dtype=np.float32)
    for idx, (u, v) in enumerate(instance["edges"]):
        if instance["matched"][idx] > 0.5:
            labels[u, v] = 1.0
            labels[v, u] = 1.0
    return labels


# ══════════════════════════════════════════
# Training & Evaluation
# ══════════════════════════════════════════

def train_gnn(train_loader, test_loader, test_instances):
    model = GNNMatcher().to(DEVICE)
    optimizer = torch.optim.Adam(model.parameters(), lr=LR)

    best_test_ratio = 0.0
    patience_counter = 0
    all_losses = []

    for epoch in range(1, EPOCHS + 1):
        model.train()
        total_loss = 0.0
        n_batches = 0
        for pos, ei, ea, label_list, nedge_list in train_loader:
            pos, ei, ea = pos.to(DEVICE), ei.to(DEVICE), ea.to(DEVICE)
            optimizer.zero_grad()
            preds = model(pos, ei, ea, nedge_list)

            loss = 0.0
            for pred, label in zip(preds, label_list):
                label = label.to(DEVICE)
                loss += F.binary_cross_entropy(pred, label)
            loss /= len(preds)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
            n_batches += 1

        avg_loss = total_loss / max(n_batches, 1)
        all_losses.append(avg_loss)

        # Evaluate
        test_ratio = eval_gnn(model, test_loader, test_instances)

        if test_ratio > best_test_ratio:
            best_test_ratio = test_ratio
            patience_counter = 0
        else:
            patience_counter += 1

        if patience_counter >= PATIENCE:
            print(f"  [GNN] Early stop at epoch {epoch}, best_test_ratio={best_test_ratio:.4f}")
            break

    train_losses_last5 = all_losses[-5:] if len(all_losses) >= 5 else all_losses
    return best_test_ratio, train_losses_last5


def eval_gnn(model, loader, instances):
    model.eval()
    ratios = []
    inst_idx = 0

    with torch.no_grad():
        for pos, ei, ea, label_list, nedge_list in loader:
            pos, ei, ea = pos.to(DEVICE), ei.to(DEVICE), ea.to(DEVICE)
            preds = model(pos, ei, ea, nedge_list)

            for pred in preds:
                inst = instances[inst_idx]
                inst_idx += 1
                pred_np = pred.cpu().numpy()
                pred_reward = greedy_matching_with_weights(
                    pred_np, inst["edges"], inst["edge_features"]
                )
                opt = inst["optimal_weight"]
                if opt > 0:
                    ratios.append(pred_reward / opt)

    return np.mean(ratios) if ratios else 0.0


def train_fc(train_dataset, test_dataset):
    model = FCMatcher().to(DEVICE)
    optimizer = torch.optim.Adam(model.parameters(), lr=LR)

    # Build tensors
    train_adjs = torch.tensor(
        np.array([build_fc_features(inst) for inst in train_dataset]), dtype=torch.float32
    ).to(DEVICE)
    train_labels = torch.tensor(
        np.array([build_fc_labels(inst) for inst in train_dataset]), dtype=torch.float32
    ).to(DEVICE)
    test_adjs = torch.tensor(
        np.array([build_fc_features(inst) for inst in test_dataset]), dtype=torch.float32
    ).to(DEVICE)
    test_labels = torch.tensor(
        np.array([build_fc_labels(inst) for inst in test_dataset]), dtype=torch.float32
    ).to(DEVICE)

    best_test_ratio = 0.0
    patience_counter = 0
    all_losses = []

    for epoch in range(1, EPOCHS + 1):
        model.train()
        # Mini-batch training
        perm = torch.randperm(len(train_adjs), device=DEVICE)
        total_loss = 0.0
        n_batches = 0

        for i in range(0, len(train_adjs), BATCH_SIZE):
            idx = perm[i:i + BATCH_SIZE]
            batch_x = train_adjs[idx]
            batch_y = train_labels[idx]

            optimizer.zero_grad()
            pred = model(batch_x)
            # Only compute loss on upper triangle + valid edges
            loss = F.binary_cross_entropy(pred, batch_y)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
            n_batches += 1

        avg_loss = total_loss / max(n_batches, 1)
        all_losses.append(avg_loss)

        # Evaluate
        model.eval()
        with torch.no_grad():
            pred_all = model(test_adjs)
            ratios = []
            for i, inst in enumerate(test_dataset):
                pred_mat = pred_all[i].cpu().numpy()
                # Extract predictions for actual edges
                pred_probs = []
                for eidx, (u, v) in enumerate(inst["edges"]):
                    pred_probs.append(pred_mat[u, v])
                pred_probs = np.array(pred_probs)
                pred_reward = greedy_matching_with_weights(
                    pred_probs, inst["edges"], inst["edge_features"]
                )
                opt = inst["optimal_weight"]
                if opt > 0:
                    ratios.append(pred_reward / opt)
            test_ratio = np.mean(ratios) if ratios else 0.0

        if test_ratio > best_test_ratio:
            best_test_ratio = test_ratio
            patience_counter = 0
        else:
            patience_counter += 1

        if patience_counter >= PATIENCE:
            print(f"  [FC] Early stop at epoch {epoch}, best_test_ratio={best_test_ratio:.4f}")
            break

    train_losses_last5 = all_losses[-5:] if len(all_losses) >= 5 else all_losses
    return best_test_ratio, train_losses_last5


# ══════════════════════════════════════════
# Main
# ══════════════════════════════════════════

def main():
    print(f"Device: {DEVICE}")
    print(f"Generating {N_INSTANCES} instances (n_nodes={N_NODES}, dist_threshold={DIST_THRESHOLD})...")

    instances = [generate_instance() for _ in range(N_INSTANCES)]
    train_instances = instances[:N_TRAIN]
    test_instances = instances[N_TRAIN:]

    # Check data stats
    avg_edges = np.mean([len(inst["edges"]) for inst in instances])
    avg_opt = np.mean([inst["optimal_weight"] for inst in instances])
    print(f"Avg edges per graph: {avg_edges:.1f}, Avg optimal weight: {avg_opt:.2f}")

    # ── GNN ──
    print("\n=== GNN (GATv2) ===")
    train_ds = GraphMatchingDataset(train_instances)
    test_ds = GraphMatchingDataset(test_instances)
    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True, collate_fn=gnn_collate)
    test_loader = DataLoader(test_ds, batch_size=BATCH_SIZE, shuffle=False, collate_fn=gnn_collate)

    gnn_ratio, gnn_losses = train_gnn(train_loader, test_loader, test_instances)
    print(f"GNN test reward/optimal: {gnn_ratio:.4f}")
    if gnn_losses:
        print(f"GNN last 5 train losses: {[f'{l:.4f}' for l in gnn_losses]}")

    # ── FC ──
    print("\n=== FC (3-layer MLP) ===")
    fc_ratio, fc_losses = train_fc(train_instances, test_instances)
    print(f"FC test reward/optimal: {fc_ratio:.4f}")
    if fc_losses:
        print(f"FC last 5 train losses: {[f'{l:.4f}' for l in fc_losses]}")

    # ── Verdict ──
    improvement = (gnn_ratio - fc_ratio) / fc_ratio * 100 if fc_ratio > 0 else float('inf')
    print(f"\n{'='*50}")
    print(f"GNN ratio: {gnn_ratio:.4f}")
    print(f"FC  ratio: {fc_ratio:.4f}")
    print(f"GNN vs FC improvement: {improvement:+.2f}%")

    if gnn_ratio >= 0.85 and gnn_ratio >= fc_ratio * 1.10:
        verdict = "PASS"
    elif gnn_ratio >= fc_ratio * 1.05:
        verdict = "CONDITIONAL PASS"
    else:
        verdict = "FAIL"
    print(f"Verdict: {verdict}")

    # Structured output
    print(f"\n{'='*50}")
    print("STRUCTURED RESULTS:")
    print(f"  gnn_ratio: {gnn_ratio:.4f}")
    print(f"  fc_ratio: {fc_ratio:.4f}")
    print(f"  improvement_pct: {improvement:.2f}")
    print(f"  verdict: {verdict}")
    print(f"  gnn_losses_last5: {[round(l, 4) for l in gnn_losses]}")
    print(f"  fc_losses_last5: {[round(l, 4) for l in fc_losses]}")


if __name__ == "__main__":
    main()
