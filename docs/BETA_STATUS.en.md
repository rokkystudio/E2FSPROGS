# Beta candidate: validated results and remaining limits

Date: October 28, 2026. ASHOT produced four executables from independently configured `build-clean`: `debugfs.exe`, `dumpe2fs.exe`, `e2fsck.exe`, `mke2fs.exe`. PE imports contain only Windows-supplied DLLs.

**Result:** all five automated test suites passed (`tools/run_beta_tests.cmd`, exit code 0). Tests cover 1/2/4 KiB ext4 blocks, images up to 256 MiB, binary files up to 4 MiB, inode link-count repair, superblock recovery, and image-size preservation.

**Additional guard:** `debugfs -w` rejects ext4 images with `shared_blocks` set. A disposable-image test toggles the superblock flag and confirms refusal plus unchanged SHA-256. This tests safe rejection, **not** correct modification of a real deduplicated Android image. `e2fsck -y` on `shared_blocks` is not certified.

## Remaining gates
- Independent baseline Windows verification passed for root-level files with depth-0 extents; other ext4 structures remain untested.
- Full upstream `make` remains blocked by unported `tune2fs`; all four selected targets built.
- Clean environment CI/second host, larger ext4 filesystems, real deduplicated shared-block filesystem tests and interrupted-write recovery.
- AVB/dm-verity validation, proven firmware rollback, exact partition mapping and Android boot compatibility.

**Decision:** the Windows candidate passes five suites but this is not evidence of safe device flashing or a stable release. The previous alpha ZIP does not include these changes.

## Windows-only update
All six test suites passed, including an independent Python standard-library reader for 1/2/4 KiB blocks. Linux/WSL is not required. See WINDOWS_ONLY.en.md.
