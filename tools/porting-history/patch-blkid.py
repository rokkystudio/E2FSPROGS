from pathlib import Path
r=Path(r"C:\FILES\PROJECTS\TOOLS\e2fsprogs-windows\source\lib\blkid")
p=r/"cache.c"
s=p.read_text().replace('if ((getuid() != geteuid()) || (getgid() != getegid()))', '#ifndef _WIN32\n\tif ((getuid() != geteuid()) || (getgid() != getegid()))')
s=s.replace('\t\treturn NULL;\n#if HAVE_PRCTL','\t\treturn NULL;\n#endif\n#if HAVE_PRCTL',1);p.write_text(s)
p=r/"devno.c";s=p.read_text().replace('lstat(path, &st)', 'stat(path, &st)');p.write_text(s)
p=r/"devname.c";s=p.read_text();s='#ifdef _WIN32\n#ifndef makedev\n#define makedev(major,minor) (((unsigned long long)(major)<<32)|(minor))\n#endif\n#endif\n'+s;p.write_text(s)
print("blkid compilation Win32 guards applied")
