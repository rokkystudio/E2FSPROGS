from pathlib import Path
f=Path(r"C:\FILES\PROJECTS\TOOLS\e2fsprogs-windows\source\lib\ext2fs\getenv.c")
s=f.read_text()
s=s.replace('if ((getuid() != geteuid()) || (getgid() != getegid()))','#ifndef _WIN32\n\tif ((getuid() != geteuid()) || (getgid() != getegid()))')
s=s.replace('\t\treturn NULL;\n#ifdef HAVE_PRCTL','\t\treturn NULL;\n#endif\n#ifdef HAVE_PRCTL',1)
f.write_text(s)
print('port guarded Unix suid environment check')
