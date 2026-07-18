#!/usr/bin/env bash
# drawio2png.sh — 批量将 drawio 导出为 PNG
# 用法: bash drawio2png.sh [--skip-obsolete]
# 依赖: draw.io 桌面版 (Windows)
# 输出: figures/png/ 下同名 .png

set -euo pipefail

DRAWIO_EXE="/mnt/d/Software/drawio/draw.io/draw.io.exe"
DRAWIO_DIR="$(cd "$(dirname "$0")/drawio" && pwd)"
OUT_DIR="$(cd "$(dirname "$0")/png" && pwd)"
SCALE=2  # 2x for decent resolution

# 废弃/跳过的文件
SKIP_PATTERNS=(
    "fig_link_budget"    # 废弃
    ".bkp"               # 备份文件
)

skip_file() {
    local f="$1"
    for pat in "${SKIP_PATTERNS[@]}"; do
        [[ "$f" == *"$pat"* ]] && return 0
    done
    return 1
}

# 检查 draw.io
if [[ ! -f "$DRAWIO_EXE" ]]; then
    echo "ERROR: draw.io not found at $DRAWIO_EXE"
    exit 1
fi

count=0
ok=0
fail=0

for f in "$DRAWIO_DIR"/*.drawio; do
    [[ -f "$f" ]] || continue

    basename=$(basename "$f" .drawio)

    if skip_file "$f"; then
        echo "SKIP: $basename (obsolete/backup)"
        continue
    fi

    count=$((count + 1))

    # Windows 路径
    win_in=$(wslpath -w "$f")
    win_out=$(wslpath -w "$OUT_DIR/${basename}.png")

    echo -n "EXPORT: $basename ... "
    if "$DRAWIO_EXE" --export --format png --scale $SCALE \
         --output "$win_out" "$win_in" 2>/dev/null; then
        echo "OK"
        ok=$((ok + 1))
    else
        echo "FAIL"
        fail=$((fail + 1))
    fi
done

echo ""
echo "Done: $ok exported, $fail failed, $count total (skipped obsolete/backup)"
