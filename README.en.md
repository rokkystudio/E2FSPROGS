# E2FSPROGS — Native Windows ext2/ext3/ext4 utilities

[Русский](README.ru.md) | [English](README.en.md)

An experimental Windows x64 port of [e2fsprogs 1.47.3](https://github.com/tytso/e2fsprogs), built with MinGW-w64. The binaries depend on Windows system DLLs only and do not require an MSYS2/Cygwin runtime to execute.

## Utilities

| Tool | Purpose | Validated scope |
| --- | --- | --- |
| `debugfs.exe` | Inspect and extract ext2/3/4 files; modify disposable test images | Read/write binary round-trips |
| `dumpe2fs.exe` | Read superblock and filesystem metadata | Tested |
| `e2fsck.exe` | Validate and repair ext filesystems | Repairs tested on disposable images only |
| `mke2fs.exe` | Format disposable ext4 images | Limited matrix validated, not in published alpha release |


## Install

The published [v0.1.0-alpha.1 archive](https://github.com/rokkystudio/E2FSPROGS/releases/tag/v0.1.0-alpha.1) contains the previous three-tool build. The newer four-tool candidate currently exists only on ASHOT at `artifacts/beta-candidate/`. Do not mix binary revisions.

## Read-only examples

```bat
dumpe2fs.exe -h C:\images\test.img
debugfs.exe -R "stat /path/to/file" C:\images\test.img
e2fsck.exe -fn C:\images\test.img
```

`-fn` prevents repairs. Back up original images and verify SHA-256 before experimenting. **Do not use `e2fsck -y` or `debugfs -w` on your only copy.**

## Repository layout

- `upstream/`: original e2fsprogs pinned as a Git submodule;
- `patches/windows-port.patch`: native Windows changes;
- `tools/configure_win32_makefiles.py`: generated Makefile adjustments;
- `tests/`: disposable-image integration and regression suites;
- `docs/`: extended documentation and acceptance checklists;
- `build-clean/`, `build-local/`, `artifacts/`: local gitignored build results.

## Build and test

```bat
git clone --recurse-submodules https://github.com/rokkystudio/E2FSPROGS.git
cd E2FSPROGS
git -C upstream apply ..\patches\windows-port.patch
```

Building requires MSYS2 **as a build environment**, MinGW-w64 GCC and Python. In the MSYS2 shell:

```bash
mkdir -p build-clean
cd build-clean
../upstream/configure --build=x86_64-w64-mingw32 --host=x86_64-w64-mingw32 --disable-nls --disable-uuidd --disable-tls --disable-tdb --disable-mmp CC=/mingw64/bin/gcc
python ../tools/configure_win32_makefiles.py .
make -C lib/ext2fs -j4
make -C lib/blkid -j4
make -C lib/support -j4
make -C debugfs -j4
make -C misc mke2fs dumpe2fs -j4
make -C e2fsck -j4
```

Only these explicitly selected targets are qualified for compilation; `make -j4` across all upstream programs also attempts to build `tune2fs`, which is not ported yet.

On ASHOT, run `tools\run_beta_tests.cmd` to test EXEs in `artifacts\beta-candidate`. The test images are disposable and automatically removed.

## Validation and limitations

Tests cover ext4 images from 16 to 256 MiB, block sizes of 1024/2048/4096 bytes, binary payloads up to 4 MiB, corruption detection, and disposable-image repairs of inode link counts and superblocks. This is **not** a complete ext4/Android certification.


## Licensing

Upstream e2fsprogs licensing (GPL/LGPL and individual source notices) remains in effect. See `upstream/NOTICE` and source headers. Binary distributions must provide the corresponding sources and Windows-port patch.

## Windows-only qualification / Квалификация Windows-only

[Windows-only validation](docs/WINDOWS_ONLY.en.md). MSYS2 is used only at build time.
