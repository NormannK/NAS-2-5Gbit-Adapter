#!/bin/bash
# DS220j only: use the official RTD1296 DSM 7.4 cross-build environment.
set -Eeuo pipefail
[[ $# -eq 0 ]] || { echo "No arguments supported; target is RTD1296 DSM 7.4." >&2; exit 2; }
[[ -f /input/r8152.c && -f /input/INFO.sh && -d /input/SynoBuildConf ]] || {
    echo "Mount the selected repository checkout read-only at /input." >&2; exit 2;
}
[[ -d /out && -w /out ]] || { echo "Mount a writable output directory at /out." >&2; exit 2; }
# Unique directory prevents stale output being mistaken for this build's result.
result=$(mktemp -d /out/ds220j.XXXXXX)
exec > >(tee "$result/build.log") 2>&1
trap 'echo "Build failed; see $result/build.log" >&2' ERR
echo "Experimental DS220j build: DSM 7.4 / rtd1296"
echo "Output: $result"
# Toolkit, source and chroot must share a filesystem for toolkit hard links.
mkdir -p /toolkit/source/r8152
rsync -a --delete \
    --exclude=.git --exclude=build --exclude=dist --exclude=output \
    --exclude='*.o' --exclude='*.ko' --exclude='*.spk' \
    --exclude='.*.cmd' --exclude='.tmp_versions' \
    --exclude='*.mod' --exclude='*.mod.c' --exclude=Module.symvers \
    --exclude=modules.order --exclude=spk_su --exclude=INFO \
    /input/ /toolkit/source/r8152/
cd /toolkit/source/r8152
find . -type f -print0 | sort -z | xargs -0 sha256sum > "$result/source-sha256.txt"
cd /toolkit/pkgscripts-ng
git rev-parse HEAD > "$result/toolkit-commit.txt"
printf 'DSM=7.4\nPLATFORM=rtd1296\n' > "$result/target.txt"
# Deployment happens here (privileged runtime), never during docker build.
# Do not pass -t for an empty cache: that means no-download in EnvDeploy.
./EnvDeploy -q -v 7.4 -p rtd1296
# -c collects packages. DSM7.4 PkgCreate.py does not support -S.
./PkgCreate.py -v 7.4 -p rtd1296 -c r8152
mapfile -d '' packages < <(find /toolkit/result_spk -type f -name '*.spk' -print0)
(( ${#packages[@]} > 0 )) || { echo "No SPK collected." >&2; exit 1; }
for package in "${packages[@]}"; do
    # Preserve subdirectories rather than silently overwriting duplicate names.
    relative=${package#/toolkit/result_spk/}
    mkdir -p "$result/packages/$(dirname "$relative")"
    cp "$package" "$result/packages/$relative"
done
cd "$result"
find packages -type f -name '*.spk' -print0 | sort -z | xargs -0 sha256sum > package-sha256.txt
echo "Build completed. Compilation does not establish NAS stability."
