import os
from pathlib import Path
import subprocess,tempfile
R=Path(__file__).resolve().parents[1]; D=Path(os.environ.get('E2FSPROGS_BIN',str(R/'artifacts'))); M=Path(os.environ.get('E2FSPROGS_MKE',str(R/'build-local/misc/mke2fs.exe')))
def cmd(a,ok=(0,)):
 p=subprocess.run([str(x) for x in a],capture_output=True,text=True,errors='replace',timeout=60)
 print('EXIT',p.returncode,'CMD',a[0],(p.stdout+p.stderr)[-420:],flush=True)
 if p.returncode not in ok:raise AssertionError('unexpected return')
 return p
with tempfile.TemporaryDirectory(prefix='repair-inode-',dir=R) as t:
 t=Path(t); f=t/'test.img'
 with f.open('wb') as z:z.truncate(64*1048576)
 cmd([M,'-F','-t','ext4',f]); s=t/'payload';s.write_bytes(b'sample'*800)
 cmd([D/'debugfs.exe','-w','-R',f'write {s} /sample',f])
 cmd([D/'debugfs.exe','-w','-R','set_inode_field /sample links_count 3',f])
 before=cmd([D/'e2fsck.exe','-fn',f],ok=(0,1,2,4,8))
 if before.returncode==0:raise AssertionError('inode corruption undetected')
 repair=cmd([D/'e2fsck.exe','-fy',f],ok=(0,1,2,3,4,8))
 after=cmd([D/'e2fsck.exe','-fn',f],ok=(0,1,2,4,8))
 if after.returncode!=0:raise AssertionError('repair did not restore clean fs')
 print('PASS: inode repair, code',repair.returncode)
