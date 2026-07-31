"""P06 master dataset builder — runs all (phase, fg, snr) chunks sequentially.
Resumable (skips existing chunks). Intended as one long background job.
"""
from __future__ import annotations
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve()
BUILD_DATASETS = HERE.parent / "build_datasets.py"
sys.path.insert(0, str(HERE.parent))
import run_p06 as P  # noqa: E402

PY = sys.executable


def main():
    chunks = []
    for fg in P.FROZEN["fg_hz_list"]:
        for snr in P.FROZEN["snr_db_list"]:
            for phase in ("train", "dev", "test"):
                chunks.append((phase, fg, snr))
    t0 = time.time()
    for i, (phase, fg, snr) in enumerate(chunks, 1):
        tag = f"{phase}_fg{int(fg)}_snr{int(snr)}"
        out = P.RESULTS_DIR / "chunks" / f"chunk_{tag}.json"
        if out.exists():
            print(f"[{i}/{len(chunks)}] SKIP {tag} (exists)", flush=True)
            continue
        print(f"[{i}/{len(chunks)}] BUILD {tag} ...", flush=True)
        ts = time.time()
        r = subprocess.run(
            [PY, str(BUILD_DATASETS), "--phase", phase, "--fg", str(fg), "--snr", str(snr)],
            capture_output=False)
        print(f"[{i}/{len(chunks)}] {tag} done in {time.time()-ts:.0f}s (rc={r.returncode}) "
              f"elapsed={time.time()-t0:.0f}s", flush=True)
    print(f"[master] ALL CHUNKS DONE in {time.time()-t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
