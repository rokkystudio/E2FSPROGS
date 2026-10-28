from pathlib import Path
p=Path(r"C:\FILES\PROJECTS\TOOLS\e2fsprogs-windows\source\lib\blkid\save.c")
s=p.read_text()
s=s.replace('#include "config.h"', '#include "config.h"\n#ifdef _WIN32\n#define WIN32_LEAN_AND_MEAN\n#include <windows.h>\n#endif')
s=s.replace('(void) link(filename, backup);','#ifdef _WIN32\n\t\t\t\t(void) CopyFileA(filename, backup, FALSE);\n#else\n\t\t\t\t(void) link(filename, backup);\n#endif')
p.write_text(s)
print('Windows-safe cache backup')
