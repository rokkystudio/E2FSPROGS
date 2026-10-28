from pathlib import Path
r=Path(r"C:\FILES\PROJECTS\TOOLS\e2fsprogs-windows\source\e2fsck")
p=r/"util.c";s=p.read_text().replace('static void *win32_heap_position(void) { return NULL; }\n','').replace('(unsigned long long)0\n#else','(unsigned long long)0);\n#else').replace('#endif);','#endif');p.write_text(s)
for name in ["problem.c","message.c"]:
 p=r/name;s=p.read_text().replace('#include <termios.h>','#ifndef _WIN32\n#include <termios.h>\n#endif');p.write_text(s)
print('adjusted terminal includes and memory-log syntax')
