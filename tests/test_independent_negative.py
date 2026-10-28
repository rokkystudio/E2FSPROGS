"""Negative Windows-only tests for independent ext4 reader.
These do not use Android backups or any Unix tools.
"""
from pathlib import Path
import os, subprocess, tempfile
from ext4_independent_reader import Ext4Reader, inspect
ROOT=Path(__file__).resolve().parents[1]
BIN=Path(os.environ.get("E2FSPROGS_BIN",str(ROOT/"artifacts/beta-candidate")))
def run(argv):
 p=subprocess.run([str(x) for x in argv],capture_output=True,text=True,errors="replace",timeout=50)
 assert p.returncode == 0, (p.returncode,p.stderr[-600:])
with tempfile.TemporaryDirectory(prefix="ext4-negative-",dir=ROOT) as td:
 t=Path(td)
 base=t/"valid.img"
 with base.open("wb") as f:f.truncate(64*1024*1024)
 run([BIN/"mke2fs.exe","-F","-t","ext4",base])
 payload=t/"content.bin";payload.write_bytes(bytes(range(256))*16)
 run([BIN/"debugfs.exe","-w","-R",f"write {payload} /content.bin",base])
 valid=inspect(base,"content.bin",payload)
 assert valid["size"]==4096
 def altered(name,offset,data,expected):
  image=t/name
  image.write_bytes(base.read_bytes())
  with image.open("r+b") as f:
   f.seek(offset);f.write(data)
  try:
   with Ext4Reader(image) as ext:
    ext.root_files()
   raise AssertionError(f"{name}: damage was accepted")
  except ValueError as ex:
   assert expected in str(ex),f"{name}: wrong error: {ex}"
  print("PASS fail-closed:",name,flush=True)
 altered("bad_magic.img",1024+56,b"\x00\x00","magic")
 altered("bad_blocksize.img",1024+24,(30).to_bytes(4,"little"),"larger than image")
 # For a valid image, the root inode extents field is 0x28 relative to inode.
 with Ext4Reader(base) as ex:
  gd_off=2*ex.block_size if ex.block_size==1024 else ex.block_size
  gd=ex.read(gd_off, ex.descriptor_size)
  table=int.from_bytes(gd[8:12],"little")
  root_ino_offset=table*ex.block_size+(2-1)*ex.inode_size
 altered("bad_extent_header.img",root_ino_offset+0x28,b"\x00\x00","extent header")
 try:
  inspect(base,"absent.bin",payload)
  raise AssertionError("missing file accepted")
 except ValueError as ex:
  assert "missing" in str(ex)
 print("PASS missing file rejected")
print("PASS 4 negative independent ext4 scenarios")
