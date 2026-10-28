# Test report — Windows x64 prototype (2026-10-28)

## Pass

- `tests/test_native_ext4.py` (after project relocation): exit code 0. On disposable 64 MiB ext4 images, runs `dumpe2fs -h`, `e2fsck -fn` (five passes), `debugfs -w` file insertion, `debugfs -R stat`, binary `debugfs -R dump`, byte-for-byte round-trip, a second `e2fsck -fn`, and detects a deliberately corrupted copy of the superblock (e2fsck exit code 8).
- Original `system_b_original.img` and `product_b_original.img` previously checked in read-only mode (`e2fsck -fn`, exit code 0). Baseline SHA-256 hashes matched after checks.
- `debugfs.exe`, `e2fsck.exe`, `dumpe2fs.exe` import Windows system DLLs only (KERNEL32, msvcrt and where needed bcrypt), with third-party runtime statically linked.

## Known issues and limits

- **`mke2fs` truncation bug**: native mke2fs shortens a newly formatted preallocated image; the disposable test fixture works around this by restoring the original length, and also explicitly disables `resize_inode`. `mke2fs.exe` is **not** included in this pre-release.
- Writes and `e2fsck` repairs have **not** been tested on images containing Android `shared_blocks` or verified dm-verity/AVB metadata. Do not flash modified Android images based on these tests.
- Clean Autoconf/Make rebuild after cloning requires additional work because some generated Makefiles were manually adjusted in `build-local` (which is intentionally ignored).
- These tools remain experimental; tests do not demonstrate production safety.

## Reproduction

Run `python tests/test_native_ext4.py` locally with the experimental mke2fs build present at `build-local/misc/mke2fs.exe` and the three executables in `artifacts/`. The test creates disposable files under the project directory and removes them automatically.
