#!/usr/bin/env python3
"""After native MinGW configure: set static linking, Windows crypto and unsupported -rdynamic.
Only generated Makefiles; no source edits. Run after configure in a fresh build directory.
"""
from pathlib import Path
import sys
root=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parents[1]/"build-clean"
if not (root/"Makefile").exists():
    raise SystemExit("Missing generated Makefile: run upstream configure first")
for name in ["debugfs/Makefile","misc/Makefile","e2fsck/Makefile"]:
    path=root/name
    text=path.read_text()
    text=text.replace("LDFLAGS = $(SANITIZER_LDFLAGS) $(PTHREAD_CFLAGS)",
        "LDFLAGS = -static -static-libgcc $(SANITIZER_LDFLAGS) $(PTHREAD_CFLAGS)")
    text=text.replace("RDYNAMIC = -rdynamic","RDYNAMIC =")
    text=text.replace("$(SYSLIBS)", "$(SYSLIBS) -lbcrypt")
    path.write_text(text)
    print("Patching",name)
io=(root/"lib/ext2fs/Makefile").read_text()
assert "windows_io.o \\" in io,"Configure did not select native Win32 I/O; aborting"
print("Verified native Windows I/O manager in lib/ext2fs")

path=root/"lib/uuid/Makefile"
text=path.read_text().replace("tst_uuid.o $(STATIC_LIBUUID)","tst_uuid.o $(STATIC_LIBUUID) -lbcrypt")
path.write_text(text)
print("Patching lib/uuid/Makefile")
