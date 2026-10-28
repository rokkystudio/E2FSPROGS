# E2FSPROGS for Windows (experimental port)

Native Windows x64 tools based on **e2fsprogs 1.47.3**, built with MinGW-w64, statically linking non-Windows runtime libraries.

## Tools
- `debugfs.exe`: inspect ext2/3/4 filesystem and extract files; write only to disposable images.
- `dumpe2fs.exe`: inspect ext filesystem superblocks and metadata.
- `e2fsck.exe`: filesystem checks; `-fn` performs a no-repair inspection.
- `mke2fs.exe`: experimental ext4 formatter, not included in the alpha release.

## Install
Preview release: https://github.com/rokkystudio/E2FSPROGS/releases/tag/v0.1.0-alpha.1
Unzip to a dedicated directory. No MSYS2/Cygwin runtime DLLs are needed, but native Windows OS libraries remain required.

## Read-only examples
```bat
dumpe2fs.exe -h C:\images\test.img
debugfs.exe -R "stat /path/to/file" C:\images\test.img
e2fsck.exe -fn C:\images\test.img
```
**Never use `e2fsck -y` or `debugfs -w` on the only copy of important data.** Keep SHA-256-verified backups.

## Build and test
Run `python tests/test_native_ext4.py` for disposable image integration tests. The EXEs are expected in `artifacts/`, with experimental mke2fs at `build-local/misc/`. Clean builds are not yet reproducible: some generated Autoconf Makefiles received manual patches. Clone with `git clone --recurse-submodules`; upstream sources are pinned in a Git submodule and Windows changes live in `patches/windows-port.patch`.

## Readiness
Alpha indicates basic read-only tests and disposable-image integration tests. Beta should require a range of filesystem sizes/features, repair behavior testing, large and binary files, a clean rebuild, dependency audit, and published test results. **Beta status and device flashing readiness are not established yet.**

## Android / REDMAGIC warning
Android ext4 partitions may contain `shared_blocks` and be protected by AVB/dm-verity. Passing fsck does not prove a modified partition can boot. Before flashing: examine vbmeta/verity configuration, preserve verified rollback images, verify partition mappings and test edits against copies. The project checklist blocks flashing until those conditions are met.

## Licensing
Upstream e2fsprogs GPL/LGPL licenses and notices apply; see upstream/NOTICE and file headers. The matching upstream source plus Windows patch must be made available with binaries.

See `TEST_RESULTS.md` and `MKE2FS_FIX.md`.
