# v0.1.0-alpha.1 — native Windows x64 preview

This is an **experimental preview**, not a stable e2fsprogs distribution.

Includes statically linked native Windows builds of `debugfs.exe`, `dumpe2fs.exe`, and `e2fsck.exe` from e2fsprogs 1.47.3, ported with MinGW-w64 GCC 16.1.0. Requires only Windows-provided DLLs (`KERNEL32.dll`, `msvcrt.dll`, and for some programs `bcrypt.dll`). MSYS2/Cygwin runtimes are **not** needed to run the executables.

Tests: read-only `e2fsck -fn` succeeded on backed-up system/product images, and disposable ext4 integration tests passed read, write, binary dump round-trip, fsck verification, and deliberate corruption detection.

**Known limitations:** no validated write/repair testing on Android ext4 `shared_blocks`; `e2fsck -y` and AVB/dm-verity workflows unverified. Experimental native `mke2fs` is deliberately excluded due to a file-size truncation bug. Build is not yet reproducible from a clean checkout because some generated Makefiles were manually patched. DO NOT use on irreplaceable data, Android system partitions, or for flashing devices.

Corresponding upstream source and Windows changes: https://github.com/rokkystudio/E2FSPROGS (clone with `--recurse-submodules` and see `patches/windows-port.patch`). See upstream NOTICE and individual source file GPL/LGPL notices.
