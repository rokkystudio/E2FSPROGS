from pathlib import Path
r=Path(r"C:\FILES\PROJECTS\TOOLS\e2fsprogs-windows\source\e2fsck")
p=r/"pass5.c";s=p.read_text().replace('#include <sys/ioctl.h>','#ifndef _WIN32\n#include <sys/ioctl.h>\n#endif');p.write_text(s)
p=r/"journal.c";s=p.read_text().replace('unix_io_manager','default_io_manager').replace('ntohl(','ext2fs_be32_to_cpu(').replace('htonl(','ext2fs_cpu_to_be32(');p.write_text(s)
print('adjusted e2fsck Windows IO, endianness and unused Unix header')
