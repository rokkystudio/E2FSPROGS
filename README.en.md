# E2FSPROGS — native ext2/ext3/ext4 utilities for Windows

**[Русский](README.ru.md) | [English](README.en.md)**

This project ports the open-source [e2fsprogs 1.47.3](https://github.com/tytso/e2fsprogs) utilities to native Windows x64 using MinGW-w64. Executables run without MSYS2/Cygwin runtime DLLs.

## Programs

| Program | Purpose |
| --- | --- |
| `debugfs.exe` | Inspect, debug, read and extract files from ext2/ext3/ext4 |
| `dumpe2fs.exe` | Inspect superblock, block groups and filesystem metadata |
| `e2fsck.exe` | Check filesystems and repair errors |
| `mke2fs.exe` | Create ext2/ext3/ext4 filesystems in images |

**Latest version:** [v0.2.0-beta.2](https://github.com/rokkystudio/E2FSPROGS/releases/tag/v0.2.0-beta.2). This is an experimental beta: always test repair and write operations on copies of valuable data. To prevent unsafe changes, `debugfs` refuses write access to ext4 filesystems using `shared_blocks`.

## Installation

Download the Windows x64 ZIP from [GitHub Releases](https://github.com/rokkystudio/E2FSPROGS/releases) and extract it to a dedicated directory. No Unix environment is needed to run the binaries.

## Examples

```cmd
dumpe2fs.exe -h D:\images\sample.img
debugfs.exe -R "stat /example.txt" D:\images\sample.img
e2fsck.exe -fn D:\images\sample.img
```

`-fn` checks without applying repairs. Use write or repair commands only on disposable or fully backed-up filesystem images.

## Repository layout

- `upstream/` — upstream e2fsprogs source (Git submodule).
- `patches/windows-port.patch` — native Windows portability changes.
- `tests/` — integration and regression tests.
- `tools/` — build configuration and test runners.
- `docs/` — technical documentation and test reports.
- `build-clean/`, `build-local/`, `artifacts/` — gitignored local build output.

## Building on Windows

Requires Windows x64, MinGW-w64 GCC, MSYS2 **as a build shell**, and Python.

```cmd
git clone --recurse-submodules https://github.com/rokkystudio/E2FSPROGS.git
cd E2FSPROGS
git -C upstream apply ../patches/windows-port.patch
```

In the MSYS2 shell with MinGW-w64 enabled:

```bash
export PATH=/mingw64/bin:/usr/bin:$PATH
mkdir build-clean
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

The unrestricted upstream `make` also builds extra tools that are not yet fully ported.

## Tests and limitations

Seven Windows-only automated suites passed, covering disposable ext4 creation, file read/write, binary round-trips, repair of selected corruption cases, multiple block sizes, independent ext4 structural reading and negative cases. The development-machine runner `tools\run_beta_tests.cmd` expects EXEs in `artifacts\beta-candidate\`.

Not all ext4 features, filesystem sizes and corruption patterns are covered. The independent Python reader is intentionally limited and rejects unsupported formats. See [test matrix](docs/TEST_MATRIX.en.md) and [Windows-only testing](docs/WINDOWS_ONLY.en.md).

## Licensing

Original e2fsprogs GPL/LGPL licenses and copyright notices apply. See `upstream/NOTICE` and source headers. Binary distributions must provide corresponding source and Windows port changes.
