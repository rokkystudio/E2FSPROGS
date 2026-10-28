# E2FSPROGS — experimental native Windows port

Windows x64 port of [e2fsprogs 1.47.3](https://github.com/tytso/e2fsprogs), built with MinGW-w64. Original source is an upstream Git submodule at `upstream/`; Windows changes are stored in `patches/windows-port.patch`.

## Layout

- `upstream/`: git submodule pinned to upstream e2fsprogs; modified local working tree on ASHOT
- `patches/`: port changes relative to the upstream commit
- `tests/`: tests using disposable ext4 images, plus a local-only read-only regression script
- `tools/porting-history/`: historical helper scripts
- `build-local/`: ignored compiler output; includes manually modified generated Makefiles
- `artifacts/`: ignored local Windows EXEs; release binaries should be attached to GitHub Releases

## Usage and status

The locally built `debugfs.exe`, `e2fsck.exe`, and `dumpe2fs.exe` are native Windows binaries with no non-system runtime DLL dependencies. A disposable ext4 test passed file write/dump round-trip, read-only fsck, and corruption detection. This is **experimental**, not production-ready: `mke2fs` shrinks a newly created image; shared-block safety, e2fsck write/repair behavior and clean rebuild are not fully tested. Do not use on irreplaceable data or flash Android partitions.

Clone with `git clone --recurse-submodules`, then apply the port using `git -C upstream apply ../patches/windows-port.patch` before building. The current local `build-local` generated Makefiles were manually patched, so rebuilding from a clean checkout is not yet reproducible.

Source licensing remains as in upstream GPL/LGPL notices. Distributions must make corresponding source and changes available.
