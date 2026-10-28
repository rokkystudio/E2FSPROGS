from pathlib import Path
r=Path(r"C:\FILES\PROJECTS\TOOLS\e2fsprogs-windows\source\lib\e2p")
for name in ["ls.c","ljs.c"]:
 f=r/name;t=f.read_text()
 t=t.replace('#include <grp.h>\n#include <pwd.h>','#ifndef _WIN32\n#include <grp.h>\n#include <pwd.h>\n#endif')
 if name=="ls.c":
  start=t.index('static void print_user')
  end=t.index('\n#define MONTH_INT',start)
  section=t[start:end]
  t=t[:start]+'''#ifdef _WIN32
static void print_user(unsigned short uid, FILE *f)
{
    fprintf(f, "%u (numeric uid)\\n", uid);
}
static void print_group(unsigned short gid, FILE *f)
{
    fprintf(f, "%u (numeric gid)\\n", gid);
}
#else
'''+section+'''
#endif
'''+t[end:]
 f.write_text(t)
 print("patched",f)
