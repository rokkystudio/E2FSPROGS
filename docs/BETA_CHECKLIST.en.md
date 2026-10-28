# Beta acceptance and flashing gate

Status: **NOT READY TO FLASH**. Passing one set of tests does not ensure Android boot safety.

- [ ] Automated clean-clone build with pinned compiler versions and EXE hashes
- [ ] Ext4 matrix: 16/64/256 MiB, 1/2/4 KiB blocks, default ext4 features
- [ ] Binary round-trips: NUL, CR/LF/CRLF, 1 byte, multi-block and multi-megabyte files
- [ ] Filesystem checksums and fsck after writes
- [ ] Superblock, inode and bitmap corruption detection and repairs on disposable copies only
- [ ] Size preservation and out-of-bounds write checks
- [ ] Independent Windows-only ext4 parsing and content-hash comparison (see WINDOWS_ONLY.en.md)
- [ ] PE import audit ensuring no non-Windows runtime DLLs
- [ ] Test ext4 `shared_blocks`: reject unsafe writes or safely unshare blocks
- [ ] Read actual device AVB/vbmeta and dm-verity configuration without modifying it
- [ ] Verified backups of all affected partitions and proven accessible fastboot/EDL rollback
- [ ] Validate modified image and restoration procedure before any flash

No `fastboot flash`, `adb remount`, or repair of original images until all gates are satisfied.
