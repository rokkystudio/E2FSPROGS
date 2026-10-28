from pathlib import Path
p=Path(r"C:\FILES\PROJECTS\TOOLS\e2fsprogs-windows\build\misc\Makefile")
s=p.read_text()
s=s.replace('LDFLAGS = $(SANITIZER_LDFLAGS) $(PTHREAD_CFLAGS)','LDFLAGS = -static -static-libgcc $(SANITIZER_LDFLAGS) $(PTHREAD_CFLAGS)')
p.write_text(s)
print('misc static link enabled')
