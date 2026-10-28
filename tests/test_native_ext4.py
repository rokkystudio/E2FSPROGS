import hashlib, pathlib, subprocess, tempfile, shutil, sys, re
ROOT=pathlib.Path(r"C:\FILES\PROJECTS\E2FSPROGS")
BIN=ROOT/"artifacts"
MKE=ROOT/"build-local"/"misc"/"mke2fs.exe"
def cmd(args,expected=None):
 p=subprocess.run([str(x) for x in args],capture_output=True,text=True,errors="replace",timeout=35)
 print("RUN:", " ".join(str(x) for x in args[:3]), "| code",p.returncode)
 print((p.stdout+"\n"+p.stderr)[:700])
 if expected is not None and p.returncode not in expected: raise AssertionError("unexpected exit code")
 return p
def sha(path):
 h=hashlib.sha256()
 with open(path,"rb") as f:
  for b in iter(lambda:f.read(1048576),b""):h.update(b)
 return h.hexdigest()
def test():
 assert all((BIN/n).is_file() for n in ("debugfs.exe","dumpe2fs.exe","e2fsck.exe"))
 with tempfile.TemporaryDirectory(prefix="ext4-safety-",dir=ROOT) as t:
  tmp=pathlib.Path(t)
  img=tmp/"clean.img"
  with img.open("wb") as f:f.truncate(64*1024*1024)
  p=cmd([MKE,"-F","-t","ext4","-O","^resize_inode","-E","nodiscard","-b","4096",img],None)
  if p.returncode: raise AssertionError("mke2fs failed to create disposable image")
  actual_size=img.stat().st_size
  print("MKE2FS_SIZE",actual_size,"EXPECTED",64*1024*1024)
  if actual_size != 64*1024*1024:
   with img.open("r+b") as f:f.truncate(64*1024*1024)
  before=sha(img)
  p=cmd([BIN/"e2fsck.exe","-fn",img],{0})
  assert before==sha(img),"read-only fsck changed image!"
  p=cmd([BIN/"dumpe2fs.exe","-h",img],{0})
  assert "0xEF53" in p.stdout
  sample=tmp/"sample.txt"; sample.write_text("NATIVE_EXT4_TEST_2026\n",encoding="utf-8")
  p=cmd([BIN/"debugfs.exe","-w","-R",f"write {sample} /test.txt",img],{0})
  if "Allocated inode" not in p.stdout+p.stderr: raise AssertionError("debugfs write did not confirm inode")
  p=cmd([BIN/"debugfs.exe","-R","stat /test.txt",img],{0})
  assert f"Size: {len(sample.read_bytes())}" in p.stdout
  dumped=tmp/"extracted.txt"
  p=cmd([BIN/"debugfs.exe","-R",f"dump /test.txt {dumped}",img],{0})
  print("DUMP_BYTES",repr(dumped.read_bytes()),"SOURCE_BYTES",repr(sample.read_bytes()))
  assert dumped.read_bytes()==sample.read_bytes(),"dump content differs"
  p=cmd([BIN/"e2fsck.exe","-fn",img],{0})
  assert "Pass 5" in p.stdout
  clean=tmp/"clean-copy.img";shutil.copy2(img,clean)
  changed=tmp/"bad.img";shutil.copy2(clean,changed)
  with changed.open("r+b") as f:
   f.seek(1024+56);f.write(b"\x00\x00")
  p=cmd([BIN/"e2fsck.exe","-fn",changed],None)
  assert p.returncode != 0,"corrupt ext4 returned success"
  assert sha(clean)==sha(img),"corruption test unexpectedly changed healthy original"
  print("PASS: disposable ext4 create/write/read/dump/fsck/corruption detection")
if __name__=="__main__":test()





