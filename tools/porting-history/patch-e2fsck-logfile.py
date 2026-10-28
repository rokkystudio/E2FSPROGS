from pathlib import Path
p=Path(r"C:\FILES\PROJECTS\TOOLS\e2fsprogs-windows\source\e2fsck\logfile.c")
s=p.read_text()
s=s.replace('#include <pwd.h>','#ifndef _WIN32\n#include <pwd.h>\n#endif',1)
s=s.replace('struct passwd\t*pw = NULL, pw_struct;','#ifndef _WIN32\n\tstruct passwd\t*pw = NULL, pw_struct;\n#endif',1)
s=s.replace("case 'u':\n#ifdef TEST_PROGRAM","case 'u':\n#ifdef _WIN32\n\t\tcp = getenv(\"USERNAME\");\n\t\tif (cp) append_string(s, cp, 0);\n\t\treturn;\n#elif defined(TEST_PROGRAM)",1)
p.write_text(s)
print('Windows logfile username from USERNAME (log naming only)')
