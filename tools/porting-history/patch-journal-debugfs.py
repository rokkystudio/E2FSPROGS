from pathlib import Path
r=Path(r"C:\FILES\PROJECTS\TOOLS\e2fsprogs-windows\source")
f=r/"misc/create_inode.c"
t=f.read_text().replace('#include <windows.h>','#include <windows.h>\n#include <sys/stat.h>')
f.write_text(t)
f=r/"debugfs/journal.c"
t=f.read_text().replace('unix_io_manager','default_io_manager').replace('htonl(','ext2fs_cpu_to_be32(').replace('ntohl(','ext2fs_be32_to_cpu(')
f.write_text(t)
print('fixed Windows IO and declaration order; journal endian uses ext2fs')
