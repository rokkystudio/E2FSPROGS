# Executed test matrix (2026-10-28)

Command: `python tests/test_beta_matrix.py`; result **PASS (4/4)** on ASHOT. All tests use disposable temporary images automatically removed after execution.

| Image size | ext4 block size | Result |
|---|---|---|
| 16 MiB | 1024 bytes | PASS |
| 64 MiB | 4096 bytes | PASS |
| 64 MiB | 2048 bytes | PASS |
| 128 MiB | 4096 bytes | PASS |

Each case checks: file size retention during filesystem creation, metadata inspection, read-only fsck before and after writing, binary file insertion and extraction with NUL/CR/LF/FF, and exact byte comparison. All three EXE files are audited for non-Windows DLL imports.

Not tested: shared_blocks writing, fsck repairs, large files, independent Linux comparison, clean reproducible builds, AVB/dm-verity handling and tested device recovery. **This is not permission to flash.**

Machine-readable report on ASHOT: `artifacts/beta-test-results.json` (generated locally and gitignored).
