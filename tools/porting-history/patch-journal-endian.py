from pathlib import Path
f=Path(r"C:\FILES\PROJECTS\TOOLS\e2fsprogs-windows\source\lib\e2p\ljs.c")
s=f.read_text().replace('ntohl(', 'e2p_be32(')
f.write_text(s)
print('used existing ext4 endian helper instead of ntohl')
