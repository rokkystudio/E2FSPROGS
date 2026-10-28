from pathlib import Path
f=Path(r"C:\FILES\PROJECTS\TOOLS\e2fsprogs-windows\source\lib\ext2fs\jfs_compat.h")
t=f.read_text().replace('#include <arpa/inet.h>','#ifndef _WIN32\n#include <arpa/inet.h>\n#endif')
f.write_text(t)
print('Windows guard added to Unix network include')
