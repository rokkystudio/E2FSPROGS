# E2FSPROGS — native Windows x64

Experimental port of e2fsprogs 1.47.3. Contains `debugfs.exe`, `dumpe2fs.exe`, `e2fsck.exe` and `mke2fs.exe`.

Tools run on Windows without MSYS2/Cygwin runtime DLLs. Test on disposable ext2/3/4 images before use on important filesystems. Write access to `shared_blocks` is not supported.

Upstream source and modifications: https://github.com/rokkystudio/E2FSPROGS. GPL/LGPL source licenses and notices remain applicable.
