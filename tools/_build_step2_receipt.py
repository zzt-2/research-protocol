"""Build persistent Step 2 acquisition receipt for AMC GW (D003). Idempotent."""
import json, pathlib, hashlib, datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
now = datetime.datetime.now().astimezone().isoformat()

def sha256(p):
    b = pathlib.Path(p).read_bytes()
    return hashlib.sha256(b).hexdigest()

def nlines(p):
    try:
        return sum(1 for _ in open(p, encoding='utf-8'))
    except Exception:
        return 0

receipt = {
    'schema': 'amc_step2_acquisition_receipt_v1',
    'generated_at': now,
    'topic': '2026-08-02-fso-amc-groundwork',
    'purpose': 'Persistent acquisition receipt for GW Step 2 Phase A coverage-correction round (D003). Survives worktree deletion; reconstructs source identity + CORE judgment even when PDFs/content are gitignored.',
    'governing_decision': 'D003 (STEP2_BLOCKED_BY_COVERAGE_GAP)',
    'core_definition': 'CORE = runtime-deployable AMC action (modulation/coding/rate/power/HARQ) AND FSO/CSI-uncertainty/turbulence/feedback-delay condition AND NOT pure-classification/AO/fixed/post-hoc AND can enter AMC M-C-A or be a direct comparator. Full text required to count toward the >=5 threshold.',
    'papers': []
}

# 4 CORE with full text
core_fulltext = [
    ('L023', 'papers/doi/10.1109_jlt.2023.3242215',
     'Adaptive Transceiver Design for High-Capacity Multi-Modal FSO',
     '10.1109/jlt.2023.3242215', 'A', 'CORE',
     'action=mod format(2/4/8-QAM)+per-mode power loading + RX MIMO decoder switch, driven by per-mode post-eq SNR; condition=MDM-FSO turbulence(von Karman phase screen, r0=0.5/0.9/1.1mm), NOT GG; deployable runtime TX+RX adaptation; key=590Gbit/s, adaptive +5.2dB vs uniform; CSI=pilot LMS+linear interp, analyzed feedback staleness limit ~60km LEO/Greenwood tau~4ms'),
    ('L096', 'papers/doi/10.1109_tvt.2021.3127193',
     'On the Design of FSO-Based Satellite Systems Using IR-HARQ With Rate Adaptation',
     '10.1109/tvt.2021.3127193', 'B', 'CORE',
     'action=RCPC code-rate(4/5,1/2,1/3)+Mn-QAM mode per channel state via IR-HARQ sliding-window; condition=LEO sat-ground FSO, lognormal turbulence(Cn2=1e-14/5e-14/1e-13), pointing, FSMC; deployable cross-layer TX link-adaptation; key=IR-HARQ-SW beats SW-ARQ/IR-SaW, ~600Mbps; CSI=ACK/NAK+CSI assumed reliable per Tslot, perfect-CSI assumption (imperfect feedback = future work)'),
    ('L146', 'papers/doi/10.1109_jiot.2025.3600439',
     'Robust Joint Opt FSO/RF sat-UAV-terrestrial Imperfect Channel',
     '10.1109/jiot.2025.3600439', 'A', 'CORE',
     'action=joint adaptive MCS(mf-QAM FSO + 3GPP MCS RF)+UAV power+trajectory via DDPG, robust JOMPT-CU under CSI uncertainty; condition=FSO/RF SUTIN, lognormal FSO+pointing, Nakagami RF, IMPERFECT CSI(Gaussian est error sigma^2=1/N pilot), FER-constrained; deployable runtime TX MCS controller; key=0.85Gb/s, robust keeps FER<0.1; CSI=pilot-based, uncertainty regions, coherence>>feedback so timely'),
    ('Galijasevic', 'papers/doi/10.1109_ojcoms.2024.011100',
     'Predicting Channel Conditions for Adaptive LDPC Coding in a Fading FSO Channel',
     '10.1109/OJCOMS.2024.011100', 'A', 'CORE',
     'action=runtime TX dynamic LDPC code-rate selection(PBRL, 8/9..8/80, k=8192, 16 rates ~0.5dB spacing) from threshold table for FER<1e-6 fed back to TX; condition=FSO lognormal turbulence, 10ms coherence(LEO PSI=10), FEEDBACK DELAY 1-4ms with zero/linear/quadratic CSI predictors; deployable real runtime link-adaptation; key=linear best <=2ms(98-101% zero-delay throughput), quadratic best 3-4ms;'),
]
for L, dd, t, d, fam, judg, src in core_fulltext:
    base = ROOT / dd
    src_pdf = base / 'source.pdf'
    cmd = base / 'content.md'
    receipt['papers'].append({
        'L': L, 'identity': {'title': t, 'doi': d, 'family': fam},
        'source_path': dd, 'content_path': str(cmd) if cmd.exists() else None,
        'source_pdf_sha256': sha256(src_pdf) if src_pdf.exists() else None,
        'acquired_at': now, 'core': 'CORE', 'core_judgment': judg, 'source': src,
        'content_lines': nlines(cmd) if cmd.exists() else 0
    })

# Safi - CORE but no full text (PROVISIONAL)
receipt['papers'].append({
    'L': 'Safi2019',
    'identity': {'title': 'Adaptive Channel Coding and Power Control for Practical FSO Communication Systems Under Channel Estimation Error',
                 'doi': '10.1109/tvt.2019.2916843', 'venue': 'IEEE TVT 68(8):7566-7577, 2019',
                 'authors': ['Safi', 'Sharifi', 'Dabiri', 'Ansari', 'Cheng'], 'citation_count': 58, 'family': 'A'},
    'source_url': 'doi.org/10.1109/tvt.2019.2916843', 'content_path': None, 'source_pdf_sha256': None,
    'acquired_at': now, 'core': 'CORE_PROVISIONAL_ABSTRACT_ONLY',
    'core_judgment': 'PROVISIONAL: abstract verifies action=joint/standalone adaptive coding-rate AND TX power control with optimization (power-min under BER/outage/peak-power), closed-form throughput; condition=Gamma-Gamma turbulence + IMPERFECT CSI via channel-estimation error dependent on observation-window length. Strong direct AMC comparator likely covering "GG+est-error+adaptive coding/power" (brief warning). NO full text (IEEE paywall, no OA/preprint found via Crossref/S2/Unpaywall).',
    'blocker': 'ieee_paywall_no_oa',
    'failure_paths_tried': ['tools/download --doi (Round1 all_failed)',
                            'subagent Crossref+Unpaywall+S2 openAccessPdf (all empty)'],
    'counted_toward_5_threshold': False
})

# L075 DISPUTED
p075 = ROOT / 'papers/doi/10.1109_access.2025.3650714'
receipt['papers'].append({
    'L': 'L075', 'identity': {'title': 'Hybrid Deep Learning-Based Adaptive Modulation for FSO', 'doi': '10.1109/access.2025.3650714', 'family': 'A(disputed)'},
    'source_path': str(p075), 'content_path': str(p075 / 'content.md'),
    'source_pdf_sha256': sha256(p075 / 'source.pdf'),
    'acquired_at': now, 'core': 'DISPUTED',
    'core_judgment': 'action=CNN-LSTM-Attention softmax CLASSIFIER on RX STFT spectrograms -> 5 modulation labels, "mapped to TX"; condition=GG turbulence(alpha2.1,beta1.7), Cn2, fog/haze/rain, pointing. Core artifact is modulation CLASSIFICATION (MFI, dead-end#8 family): confusion-matrix eval + true-label training. AMC framing claimed but no explicit CSI estimate/feedback loop. SEMANTICALLY_DISPUTED_PENDING_FULL_READ per D003 - NOT counted as CORE.',
    'content_lines': nlines(p075 / 'content.md')
})

# L165 NO (AO only)
p165 = ROOT / 'papers/doi/10.1038_s41377-023-01201-7'
receipt['papers'].append({
    'L': 'L165', 'identity': {'title': 'Tbit/s feeder links coherent modulation + full-adaptive optics', 'doi': '10.1038/s41377-023-01201-7', 'family': 'C(boundary)'},
    'source_path': str(p165), 'source_pdf_sha256': sha256(p165 / 'source.pdf'),
    'acquired_at': now, 'core': 'BOUNDARY',
    'core_judgment': 'NO - adaptive action is AO wavefront correction (Shack-Hartmann + 97-actuator DM 1.5kHz), NOT AMC. Modulation (PM-16/64-QAM, 4QAM, PS-QPSK, 4D-BPSK) fixed per measurement, compared not switched. AO-boundary / coherent-FSO comparator only.',
    'content_lines': nlines(p165 / 'content.md')
})

# L090 NO (fixed STTC)
p090 = ROOT / 'papers/manual/L090-intechopen'
receipt['papers'].append({
    'L': 'L090', 'identity': {'title': 'Mitigating Turbulence-Induced Fading in Coherent FSO: Adaptive Space-Time Code', 'doi': '10.5772/intechopen.84911', 'family': 'C(boundary)',
                              'path_note': 'papers/manual/L090-intechopen/ (manual slug; real DOI 10.5772/intechopen.84911 in metadata - path-compliant for manual acquisition)'},
    'source_path': str(p090), 'source_pdf_sha256': sha256(p090 / 'source.pdf'),
    'acquired_at': now, 'core': 'BOUNDARY',
    'core_judgment': 'NO - 4-state STTC, 2 TX lasers, QPSK coherent. "Adaptive orthogonality controller" = mathematical xi-parameterization for arbitrary STCs, design-time config NOT feedback-driven switch. Fixed-scheme performance study, no CSI feedback, no runtime AMC action. "Adaptive" is nominal. Coherent-FSO STTC reference only.',
    'content_lines': nlines(p090 / 'content.md')
})

# Unacquired (3 stop-loss): Chang, Sun, L124
unacq = [
    ('Chang2025', '10.1109/JPHOT.2025.3602148',
     'Integrated FEC, Interleaving, ARQ, and Adaptive Modulation for Long-Distance Maritime Communication Systems: Design and Analysis',
     'IEEE Photonics J 17(5):1-9, 2025 (gold OA CC-BY)', 'B',
     'ieee_gold_oa_bot_blocked',
     ['tools/download --doi (Round1 fail)', 'direct ieeexplore stampPDF/stamp.jsp (404 -> /denied/)', 'subagent confirms gold OA but automated access blocked']),
    ('Sun2018', '10.1364/OE.26.029319',
     'Run-time reconfigurable adaptive LDPC coding for optical channels',
     'Optics Express 26(22):29319, 2018 (gold OA CC-BY)', 'A',
     'optica_gold_oa_bot_challenge',
     ['tools/download --doi (Round1 fail - Optica not in wrapper channels)', 'subagent confirms gold OA but opg.optica.org viewmedia.cfm -> Radware bot-challenge (validate.perfdrive.com)']),
    ('L124', '10.1364/oe.595557',
     'Physics-informed adaptive transmission for coherent FSO: multi-dimensional amplitude-phase statistics',
     'Optics Express 34(14):26128, 2026 (gold OA VOR)', 'C',
     'C_L124_FULLTEXT_BLOCKED',
     ['tools/download --doi (Round1 fail - Optica JS-challenge HTTP 202, carried from prior round)', 'subagent: same Radware bot-challenge; no author preprint found']),
]
for L, d, t, v, fam, bl, paths in unacq:
    receipt['papers'].append({
        'L': L, 'identity': {'title': t, 'doi': d, 'venue': v, 'family': fam},
        'content_path': None, 'source_pdf_sha256': None, 'acquired_at': now, 'core': 'UNACQUIRED',
        'blocker': bl, 'failure_paths_tried': paths, 'counted_toward_5_threshold': False,
        'note': '>=3 paths tried, stop-loss per gw-acquire.md. Legal OA exists but automated download blocked by publisher bot-defense; user manual acquisition required.'
    })

receipt['coverage_summary'] = {
    'core_with_fulltext': 4,
    'core_with_fulltext_list': ['L023', 'L096', 'L146', 'Galijasevic'],
    'core_no_fulltext': ['Safi2019 (PROVISIONAL, IEEE paywall)'],
    'disputed': ['L075 (classification artifact)'],
    'boundary_no': ['L165 (AO)', 'L090 (fixed STTC)'],
    'unacquired_stoploss': ['Chang2025', 'Sun2018', 'L124'],
    'threshold': 5,
    'step2_verdict': 'STEP2_BLOCKED_BY_COVERAGE_GAP (4 CORE fulltext < 5 threshold; Safi CORE but no fulltext; L075 DISPUTED not counted; 3 unacquired)',
    'legal_next_action': 'Per D003 + brief: report Step 2 blocker honestly; do NOT fabricate Step 3. User must manually acquire Safi(IEEE) and/or Chang/Sun/L124 (Optica/IEEE OA via browser) to reach >=5 CORE fulltext, OR confirm 4-CORE-fulltext + Safi-abstract coverage is acceptable to proceed with A/B families only (C family stays BLOCKED pending L124 fulltext).'
}

out = ROOT / 'search-archive/2026-08-02/_step2_acquisition_receipt.json'
out.write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding='utf-8')
print('receipt written:', out, 'papers:', len(receipt['papers']))
print('verdict:', receipt['coverage_summary']['step2_verdict'])
