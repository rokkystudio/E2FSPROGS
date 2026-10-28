import os
"""Beta qualification on disposable images. No Android device writes."""
import hashlib,json,pathlib,subprocess,tempfile,time
ROOT=pathlib.Path(__file__).resolve().parents[1]
D=pathlib.Path(os.environ.get("E2FSPROGS_BIN",str(ROOT/"artifacts")))
M=pathlib.Path(os.environ.get("E2FSPROGS_MKE",str(ROOT/"build-local/misc/mke2fs.exe")))
def run(args, ok=(0,), timeout=180):
 p=subprocess.run([str(x) for x in args],capture_output=True,text=True,errors="replace",timeout=timeout)
 if p.returncode not in ok: raise AssertionError(f"exit {p.returncode}: {' '.join(map(str,args))}\n{(p.stdout+p.stderr)[-1000:]}")
 return p
def sha(p):
 h=hashlib.sha256()
 with p.open("rb") as f:
  for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
 return h.hexdigest()
def check(img):
 before=sha(img)
 p=run([D/"e2fsck.exe","-fn",img])
 assert "Pass 5" in p.stdout
 assert sha(img)==before
def main():
 results=[]
 with tempfile.TemporaryDirectory(prefix="ext4-beta-full-",dir=ROOT) as td:
  t=pathlib.Path(td)
  for size,block in [(16,1024),(64,2048),(64,4096),(256,4096)]:
   img=t/f"{size}_{block}.img"
   with img.open("wb") as f:f.truncate(size*1048576)
   run([M,"-F","-t","ext4","-b",block,img])
   assert img.stat().st_size==size*1048576
   check(img)
   for n, data in (("one",b"\x00"),("binary",bytes(range(256))*256+b"\r\n\x00\xff"),("large",bytes(range(256))*16384)):
    src=t/f"{size}_{block}_{n}.bin";src.write_bytes(data)
    cmd=run([D/"debugfs.exe","-w","-R",f"write {src} /{n}",img])
    assert "Allocated inode" in cmd.stdout
    out=t/f"{size}_{block}_{n}_out.bin"
    run([D/"debugfs.exe","-R",f"dump /{n} {out}",img])
    assert sha(src)==sha(out),f"mismatch: {n}"
    assert img.stat().st_size==size*1048576,"size unexpectedly changed"
   check(img)
   results.append({"size_mib":size,"block":block,"payloads":["one","binary","large"],"result":"PASS"})
   print("PASS",size,block,flush=True)
  # Explicitly test damage detection, then repair only the disposable image.
  original=t/"repair.img"
  with original.open("wb") as f:f.truncate(64*1048576)
  run([M,"-F","-t","ext4",original])
  assert original.stat().st_size==64*1048576
  check(original)
  before=sha(original)
  with original.open("r+b") as f:
   f.seek(1024+12); f.write((1).to_bytes(4,"little"))
  damaged=run([D/"e2fsck.exe","-fn",original],ok=(0,1,2,4,8))
  assert damaged.returncode!=0, "corruption was not detected"
  fix=run([D/"e2fsck.exe","-fy",original],ok=(0,1,2,3))
  check(original)
  assert sha(original)!=before,"repair produced no change"
  results.append({"repair_test":"free_blocks_count","detection_code":damaged.returncode,"repair_code":fix.returncode,"post_repair":"PASS"})
  print("REPAIR PASS",flush=True)
 report={"status":"PASS","cases":results,"date_utc":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()),"scope":"disposable images only","flashing_qualified":False}
 out=D/"beta-qualification.json";out.write_text(json.dumps(report,indent=2),encoding="utf-8")
 print("REPORT",out)
if __name__=="__main__":main()
