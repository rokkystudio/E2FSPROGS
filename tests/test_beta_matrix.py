import os
"""Disposable extended Windows ext4 validation. Never accesses Android backups."""
from pathlib import Path
import hashlib, json, os, subprocess, tempfile, time
ROOT=Path(__file__).resolve().parents[1]
BIN=Path(os.environ.get("E2FSPROGS_BIN",str(ROOT/"artifacts")))
MKE=Path(os.environ.get("E2FSPROGS_MKE",str(ROOT/"build-local/misc/mke2fs.exe")))
REPORT=BIN/"beta-test-results.json"
def run(args, accepted=(0,), timeout=120):
    p=subprocess.run(list(map(str,args)),capture_output=True,text=True,errors="replace",timeout=timeout)
    if p.returncode not in accepted:
        raise AssertionError(f"{args[0]} code={p.returncode}: {(p.stdout+p.stderr)[-1000:]}")
    return p
def hash_file(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""):h.update(chunk)
    return h.hexdigest()
def verify_fs(img):
    before=hash_file(img)
    output=run([BIN/"e2fsck.exe","-fn",img]).stdout
    assert "Pass 5" in output
    assert before==hash_file(img), "read-only fsck altered filesystem"
def scenario(temp, size_mb, block):
    img=temp/f"test_{size_mb}_{block}.img"
    with open(img,"wb") as out:out.truncate(size_mb*1024*1024)
    run([MKE,"-F","-t","ext4","-b",str(block),img])
    assert img.stat().st_size==size_mb*1024*1024, "mke2fs truncated image"
    assert "0xEF53" in run([BIN/"dumpe2fs.exe","-h",img]).stdout
    verify_fs(img)
    data=bytes(range(256))*24 + b"\x00\r\n\r\n\xff"*13
    src=temp/f"payload_{size_mb}_{block}.bin"; src.write_bytes(data)
    written=run([BIN/"debugfs.exe","-w","-R",f"write {src} /payload.bin",img])
    assert "Allocated inode" in written.stdout
    check=run([BIN/"debugfs.exe","-R","stat /payload.bin",img])
    assert f"Size: {len(data)}" in check.stdout
    dst=temp/f"out_{size_mb}_{block}.bin"
    run([BIN/"debugfs.exe","-R",f"dump /payload.bin {dst}",img])
    assert dst.read_bytes()==data, "binary file differs"
    verify_fs(img)
    return {"size_mib":size_mb,"block_bytes":block,"result":"PASS","size_bytes":img.stat().st_size,"payload_sha256":hash_file(dst)}
def deps():
    obj=Path(r"C:\msys64\mingw64\bin\objdump.exe")
    allowed={"KERNEL32.dll","msvcrt.dll","bcrypt.dll"}
    report={}
    for filename in ("debugfs.exe","dumpe2fs.exe","e2fsck.exe"):
        f=BIN/filename
        out=run([obj,"-p",f]).stdout
        names=[line.split("DLL Name:",1)[1].strip() for line in out.splitlines() if "DLL Name:" in line]
        assert set(names)<=allowed,(filename,names)
        report[filename]={"dlls":names,"sha256":hash_file(f)}
    return report
def main():
    report={"started_utc":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()),"scenarios":[],"dependencies":{},"status":"FAIL"}
    try:
        assert MKE.exists(), "Native mke2fs not built"
        report["dependencies"]=deps()
        with tempfile.TemporaryDirectory(prefix="ext4-beta-",dir=ROOT) as tmp:
            temp=Path(tmp)
            for size_mb,block in [(16,1024),(64,4096),(64,2048),(128,4096)]:
                report["scenarios"].append(scenario(temp,size_mb,block))
                print("PASS",size_mb,"MiB",block,"byte blocks",flush=True)
        report["status"]="PASS"
    except Exception as e:
        report["error"]=repr(e)
        raise
    finally:
        REPORT.parent.mkdir(exist_ok=True)
        REPORT.write_text(json.dumps(report,indent=2),encoding="utf-8")
        print("Report:",REPORT)
if __name__=="__main__": main()
