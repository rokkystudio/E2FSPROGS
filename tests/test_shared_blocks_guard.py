"""Safety regression: debugfs must reject writes to shared_blocks ext4."""
from pathlib import Path
import hashlib,os,subprocess,tempfile
ROOT=Path(__file__).resolve().parents[1]
BIN=Path(os.environ.get("E2FSPROGS_BIN",str(ROOT/"artifacts/beta-candidate")))
MKE=Path(os.environ.get("E2FSPROGS_MKE",str(BIN/"mke2fs.exe")))
def run(a):
 return subprocess.run([str(x) for x in a],capture_output=True,text=True,errors="replace",timeout=35)
def digest(path):
 h=hashlib.sha256()
 with path.open("rb") as f:
  for chunk in iter(lambda:f.read(1024*1024),b""):h.update(chunk)
 return h.hexdigest()
with tempfile.TemporaryDirectory(prefix="ext4-shared-guard-",dir=ROOT) as d:
 root=Path(d); img=root/"guard.img"; payload=root/"test.bin"
 with img.open("wb") as f:f.truncate(64*1048576)
 p=run([MKE,"-F","-t","ext4",img])
 assert p.returncode==0,p.stderr
 payload.write_bytes(b"SAFE_WRITES_MUST_BE_REJECTED")
 with img.open("r+b") as f:
  f.seek(1024+100)
  flags=int.from_bytes(f.read(4),"little")
  f.seek(1024+100)
  f.write((flags|0x4000).to_bytes(4,"little"))
 before=digest(img)
 p=run([BIN/"debugfs.exe","-w","-R",f"write {payload} /unsafe",img])
 combined=p.stdout+p.stderr
 assert "shared_blocks" in combined and "refusing" in combined,repr(combined)
 assert digest(img)==before,"file changed during rejected write"
 print("PASS shared_blocks write rejected before image is changed")
 p=run([BIN/"debugfs.exe","-w","-R",f"write {payload} /safe",root/"absent.img"])
 assert not (root/"absent.img").exists(),"tool unexpectedly created a missing image"
 print("PASS nonexistent image not created")
