# e2fsprogs 1.47.3 — native Windows MinGW-w64 port (ASHOT)

**2026-10-28 — All three native EXEs built and launched on Windows.**

- `dist/debugfs.exe`: built, launched, read-only `stat` on backed-up product ext4 image verified inode 324, length 9943 bytes, SELinux xattr, extents.
- `dist/dumpe2fs.exe`: built, launched, read-only superblock inspection of product ext4 image.
- `dist/e2fsck.exe`: built, launched, **read-only `-fn` verification successfully completed all five passes for both backups**, both processes exit code **0**.

All three EXEs have statically linked MinGW/C runtime support libraries; PE imports verified using objdump. `debugfs.exe` and `e2fsck.exe`: `bcrypt.dll`, `KERNEL32.dll`, `msvcrt.dll`; `dumpe2fs.exe`: `KERNEL32.dll`, `msvcrt.dll`. All are Windows-supplied DLLs, with **no MSYS2/Cygwin/libwinpthread runtime dependency**.

**Backup hashes reconfirmed after read-only tests:**
- `system_b_original.img`: SHA256 `f80543684bff4c90833dcac22f2a13a7dcbdb410cad3e0099e62016b8627332c`
- `product_b_original.img`: SHA256 `a39724232466f0561551c9bb5cfa97c27a70d4e1695ad05379699cab95f4e565`



Local source changes are in `source/`, original source tag 1.47.3. `build/` contains generated Makefiles with manual fixes (Win32 IO selection, correct `bcrypt` and static link flags). **Clean configure/rebuild has not been revalidated**; do not assume these generated changes are reproducible yet. Project path: `C:\FILES\PROJECTS\E2FSPROGS`.
