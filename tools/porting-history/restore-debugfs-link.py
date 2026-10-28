from pathlib import Path
p=Path(r"C:\FILES\PROJECTS\TOOLS\e2fsprogs-windows\build\debugfs\Makefile")
s=p.read_text().replace('LIBBLKID = $(LIBUUID)','LIBBLKID = $(LIB)/libblkid.a $(LIBUUID)').replace('DEPLIBBLKID = $(DEPLIBUUID)','DEPLIBBLKID = $(LIB)/libblkid.a $(DEPLIBUUID)').replace('STATIC_LIBBLKID = $(STATIC_LIBUUID)','STATIC_LIBBLKID = $(LIB)/libblkid.a $(STATIC_LIBUUID)').replace('DEPSTATIC_LIBBLKID = $(DEPSTATIC_LIBUUID)','DEPSTATIC_LIBBLKID = $(LIB)/libblkid.a $(DEPSTATIC_LIBUUID)')
s=s.replace('$(LIBUUID) $(LIBMAGIC) $(SYSLIBS) $(LIBARCHIVE)', '$(LIBUUID) $(LIBMAGIC) $(SYSLIBS) $(LIBARCHIVE) -lbcrypt')
p.write_text(s)
print('blkid restored and bcrypt linked')
