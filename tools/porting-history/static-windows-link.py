from pathlib import Path
root=Path(r"C:\FILES\PROJECTS\TOOLS\e2fsprogs-windows")
p=root/"build/debugfs/Makefile"
s=p.read_text().replace('LDFLAGS = $(SANITIZER_LDFLAGS) $(PTHREAD_CFLAGS)', 'LDFLAGS = -static -static-libgcc $(SANITIZER_LDFLAGS) $(PTHREAD_CFLAGS)')
p.write_text(s)
p=root/"source/misc/dumpe2fs.c"
s=p.read_text().replace('unix_io_manager','default_io_manager').replace('ntohl(','ext2fs_be32_to_cpu(').replace('htonl(','ext2fs_cpu_to_be32(')
p.write_text(s)
print('static link flags and dumpe2fs Windows io/endian adjusted')
