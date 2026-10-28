from pathlib import Path
f=Path(r"C:\FILES\PROJECTS\TOOLS\e2fsprogs-windows\build\debugfs\Makefile")
s=f.read_text()
s=s.replace('LIBBLKID = $(LIB)/libblkid.a  $(LIBUUID)','LIBBLKID = $(LIBUUID)')
s=s.replace('DEPLIBBLKID = $(LIB)/libblkid.a  $(DEPLIBUUID)','DEPLIBBLKID = $(DEPLIBUUID)')
s=s.replace('STATIC_LIBBLKID = $(LIB)/libblkid.a $(STATIC_LIBUUID)','STATIC_LIBBLKID = $(STATIC_LIBUUID)')
s=s.replace('DEPSTATIC_LIBBLKID = $(LIB)/libblkid.a $(DEPSTATIC_LIBUUID)','DEPSTATIC_LIBBLKID = $(DEPSTATIC_LIBUUID)')
f.write_text(s)
print('test link without blkid: no placeholder library created')
