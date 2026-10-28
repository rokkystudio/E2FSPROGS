#!/usr/bin/env bash
set -euo pipefail
export PATH="/mingw64/bin:/usr/bin:$PATH"
ROOT=/c/FILES/PROJECTS/E2FSPROGS
cd "$ROOT/build-local"
if [ ! -f Makefile ]; then
  echo "Clean Windows configure not automated: generated Makefiles are required." >&2
  exit 2
fi
make -C lib/ext2fs -j4
make -C lib/blkid -j4
make -C lib/support -j4
make -C debugfs -j4
make -C misc dumpe2fs -j4
make -C e2fsck -j4
mkdir -p "$ROOT/artifacts"
cp debugfs/debugfs.exe misc/dumpe2fs.exe e2fsck/e2fsck.exe "$ROOT/artifacts/"
