from pathlib import Path
r=Path(r"C:\FILES\PROJECTS\TOOLS\e2fsprogs-windows\source\lib\ext2fs")
f=r/"mkjournal.c";s=f.read_text()
s=s.replace("htonl(", "ext2fs_cpu_to_be32(").replace("ntohl(", "ext2fs_be32_to_cpu(")
f.write_text(s)
f=r/"mmp.c";s=f.read_text().replace("pid ^ getuid() ^ tv.tv_sec", "pid ^ tv.tv_sec")
f.write_text(s)
print("journal byte-order helpers and Windows MMP seed patched")
