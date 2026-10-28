"""Windows-only independent ext4 roundtrip verifier; no Unix or WSL."""
from pathlib import Path
import os, subprocess, tempfile
from ext4_independent_reader import inspect
ROOT=Path(__file__).resolve().parents[1]
BIN=Path(os.environ.get("E2FSPROGS_BIN", str(ROOT/"artifacts/beta-candidate")))
def run(args):
 p=subprocess.run([str(a) for a in args],capture_output=True,text=True,errors="replace",timeout=60)
 if p.returncode: raise RuntimeError((p.stderr+p.stdout)[-1000:])
 return p
with tempfile.TemporaryDirectory(prefix="ext4-independent-",dir=ROOT) as d:
 base=Path(d)
 for block in (1024,2048,4096):
  img=base/f"{block}.img"
  with img.open("wb") as f:f.truncate(64*1024*1024)
  run([BIN/"mke2fs.exe","-F","-t","ext4","-b",block,img])
  for name,payload in (("payload.bin",bytes(range(256))*16+b"\x00\r\n\xff"),("second.bin",b"\x00"*919+b"ABC")):
   expected=base/(str(block)+"_"+name)
   expected.write_bytes(payload)
   run([BIN/"debugfs.exe","-w","-R",f"write {expected} /{name}",img])
   result=inspect(img,name,expected)
   assert result["block_size"]==block
   print("PASS independent ext4 parser",block,name,result["sha256"],flush=True)
print("PASS Windows-only independent ext4 verification")
