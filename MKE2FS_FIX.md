# mke2fs Windows image-size regression — fixed in source (2026-10-28)

## Root cause and solution

Native `lib/ext2fs/windows_io.c` contained a `windows_zeroout()` implementation that attempted POSIX `fstat()` / `ftruncate()` on an MSVC/MinGW CRT descriptor mapped to a Win32 HANDLE. In this port, the resulting zeroout sequence could shrink a preallocated image rather than only zeroing the requested region.

The safe Windows behavior now returns `EXT2_ET_UNIMPLEMENTED` for the unsupported fast-zeroout operation, allowing the existing portable fallback to perform explicit zero writes. This deliberately prioritizes image integrity over fast zeroout performance; it is **not** a Windows optimized zeroout implementation.

## Regression test

`python tests/test_native_ext4.py` succeeded on an independently generated, disposable 64 MiB image **without** any post-format file resize and **without** disabling `resize_inode` or requiring `nodiscard`. The assertion checks exact 67,108,864-byte length. `e2fsck -fn` exited 0 after formatting and after debugfs writing; binary dump matched source; intentional superblock damage was detected.

Separately, `mke2fs -F -t ext4 -E nodiscard <64 MiB test image>` preserved the exact size, and `e2fsck -fn` exited 0 with the default ext4 feature set.

## Remaining limitations

More extensive file-size tests, sparse-file handling, zeroout performance, partition alignment, repair writes, Android `shared_blocks`, and clean reproducible builds remain unvalidated. No phone or original Android backups were modified. The previously published `v0.1.0-alpha.1` release does **not** contain these changes; a future release should be built and packaged separately after further testing.
