# Beta candidate: validated results and remaining limits

Date: October 28, 2026. ASHOT produced four executables from independently configured `build-clean`: `debugfs.exe`, `dumpe2fs.exe`, `e2fsck.exe`, `mke2fs.exe`. PE imports contain only Windows-supplied DLLs.

**Result:** all five automated test suites passed (`tools/run_beta_tests.cmd`, exit code 0). Tests cover 1/2/4 KiB ext4 blocks, images up to 256 MiB, binary files up to 4 MiB, inode link-count repair, superblock recovery, and image-size preservation.


## Remaining gates
- Independent baseline Windows verification passed for root-level files with depth-0 extents; other ext4 structures remain untested.
- Full upstream `make` remains blocked by unported `tune2fs`; all four selected targets built.
- Clean environment CI/second host, larger ext4 filesystems, real deduplicated shared-block filesystem tests and interrupted-write recovery.


## Windows-only update
All six test suites passed, including an independent Python standard-library reader for 1/2/4 KiB blocks. Linux/WSL is not required. See WINDOWS_ONLY.en.md.
