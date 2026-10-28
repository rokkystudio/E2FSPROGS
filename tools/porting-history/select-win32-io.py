from pathlib import Path
root=Path(r"C:\FILES\PROJECTS\TOOLS\e2fsprogs-windows")
f=root/"build/lib/ext2fs/Makefile"
t=f.read_text()
needle="\tunix_io.o \\\n"
assert needle in t
t=t.replace(needle,"\twindows_io.o \\\n",1)
needle="\t$(srcdir)/unix_io.c \\\n"
assert needle in t
t=t.replace(needle,"\t$(srcdir)/windows_io.c \\\n",1)
f.write_text(t)
print("native Windows IO manager selected in generated makefile")
