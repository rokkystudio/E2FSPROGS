# Beta qualification without Linux

**Policy:** all qualification work runs on Windows x64. No Linux, WSL, Unix VM or remote Unix host is required.

- **Build:** MinGW-w64 GCC with the Windows-hosted MSYS2 build shell; MSYS2 is **only a development-time tool**. The native Windows PE EXEs import Windows-supplied DLLs only.
- **Independent filesystem verification:** `tests/ext4_independent_reader.py` uses only Python's standard library to parse ext4 superblocks, group descriptors, inodes, depth-0 extents and root-directory file contents. It independently compares file SHA-256 hashes, without invoking debugfs to verify them.
- **Test:** `tests/test_independent_windows.py` covers 1024/2048/4096-byte ext4 blocks; all six independent binary-content comparisons passed.
- **Other suites:** `tools/run_beta_tests.cmd` verifies creation, image-size preservation, binary round trips, superblock and inode repairs, and the write-refusal guard for `shared_blocks`.

**Independent reader limitations:** nested directories, extent trees above depth 0, uninitialized extents and several ext4 features are unsupported; the reader fails explicitly rather than pretending full validation. This is not an independent audit of every filesystem structure.


### Negative tests
The tests/test_independent_negative.py suite rejects invalid magic, impossible block layout, corrupt extent headers and missing paths: 4/4 PASS. This is not a replacement for a full fsck.
