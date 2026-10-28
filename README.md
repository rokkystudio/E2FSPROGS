# E2FSPROGS — native ext2/ext3/ext4 tools for Windows

**[Русский](README.ru.md) | [English](README.en.md)**

Windows x64 port of [e2fsprogs 1.47.3](https://github.com/tytso/e2fsprogs) built with MinGW-w64. Executables require no MSYS2 or Cygwin runtime DLLs.

Included: **debugfs.exe**, **dumpe2fs.exe**, **e2fsck.exe**, **mke2fs.exe**.

Documentation: [Windows-only testing (RU)](docs/WINDOWS_ONLY.ru.md) · [Windows-only testing (EN)](docs/WINDOWS_ONLY.en.md) · [Test matrix (RU)](docs/TEST_MATRIX.ru.md) · [Test matrix (EN)](docs/TEST_MATRIX.en.md).

[Releases](https://github.com/rokkystudio/E2FSPROGS/releases) · [Port patch](patches/windows-port.patch)

**Beta preview:** use copies of filesystem images when testing write or repair operations. Special feature `shared_blocks` write handling is not supported.
