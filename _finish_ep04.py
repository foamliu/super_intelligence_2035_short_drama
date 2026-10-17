import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "OUTPUT" / "04_棋子" / "videos"
PY = r"D:\Python310\python.exe"
TOTAL = 55


def count():
    return len(list(OUT.glob("EP04_SHOT-*_H3_*.mp4")))


def main():
    print(f"[finish] start. videos={count()}/{TOTAL}", flush=True)
    deadline = time.time() + 5400
    while count() < TOTAL and time.time() < deadline:
        time.sleep(20)
        print(f"[finish] waiting... videos={count()}/{TOTAL}", flush=True)
    print(f"[finish] videos={count()}/{TOTAL}", flush=True)
    if count() < TOTAL:
        print("[finish] TIMEOUT waiting for videos", flush=True)
        sys.exit(1)
    r = subprocess.run([PY, "scripts/gen_ep04_subtitles.py"], cwd=str(ROOT))
    print(f"[finish] subtitles exit={r.returncode}", flush=True)
    r = subprocess.run([PY, "scripts/synth_ep04.py"], cwd=str(ROOT))
    print(f"[finish] synth exit={r.returncode}", flush=True)
    print("FINISH_EP04_COMPLETE", flush=True)


if __name__ == "__main__":
    main()
