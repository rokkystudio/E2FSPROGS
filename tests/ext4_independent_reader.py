#!/usr/bin/env python3
"""Independent read-only ext4 checker on Windows, stdlib only.
Deliberately limited to regular files with depth-0 extents and root directory;
unsupported metadata causes explicit failure, not a false PASS.
"""
from pathlib import Path
import argparse, hashlib, struct

def u16(b, i): return struct.unpack_from("<H", b, i)[0]
def u32(b, i): return struct.unpack_from("<I", b, i)[0]

class Ext4Reader:
    def __init__(self, path):
        self.f = open(path, "rb")
        self.f.seek(0, 2)
        self.length = self.f.tell()
        s = self.read(1024, 1024)
        if u16(s, 0x38) != 0xEF53:
            raise ValueError("not ext2/3/4 magic")
        self.block_size = 1024 << u32(s, 0x18)
        self.blocks_lo = u32(s, 0x04)
        self.blocks = self.blocks_lo | (u32(s, 0x150) << 32 if u32(s, 0x60) & 0x80 else 0)
        self.blocks_per_group = u32(s, 0x20)
        self.inodes_per_group = u32(s, 0x28)
        self.inode_size = u16(s, 0x58) if u32(s, 0x4C) > 0 else 128
        self.descriptor_size = max(32, u16(s, 0xFE)) if (u32(s, 0x60) & 0x80) else 32
        self.compat = u32(s, 0x5C)
        self.incompat = u32(s, 0x60)
        self.rocompat = u32(s, 0x64)
        if self.blocks * self.block_size > self.length:
            raise ValueError("filesystem larger than image")
        if not (self.incompat & 0x40):
            raise ValueError("extents unsupported/disabled")
        if self.inode_size < 128 or not self.inodes_per_group or not self.blocks_per_group:
            raise ValueError("invalid ext4 layout")
    def __enter__(self): return self
    def __exit__(self, *x): self.f.close()
    def read(self, off, n):
        if off < 0 or n < 0 or off + n > self.length: raise ValueError("out-of-range image read")
        self.f.seek(off)
        data = self.f.read(n)
        if len(data) != n: raise IOError("short read")
        return data
    def inode(self, ino):
        if ino < 1: raise ValueError("invalid inode")
        group, pos = divmod(ino - 1, self.inodes_per_group)
        gdt = 2 * self.block_size if self.block_size == 1024 else self.block_size
        gd = self.read(gdt + group * self.descriptor_size, self.descriptor_size)
        table = u32(gd, 0x8)
        if self.descriptor_size >= 64: table |= u32(gd, 0x28) << 32
        node = self.read(table * self.block_size + pos * self.inode_size, self.inode_size)
        if not u16(node, 0): raise ValueError("missing inode")
        size = u32(node, 4) | (u32(node, 0x6C) << 32 if u16(node, 0) & 0xF000 == 0x8000 else 0)
        return node, size
    def payload(self, ino):
        inode, size = self.inode(ino)
        if not u32(inode, 0x20) & 0x80000: raise ValueError("inode has no extents")
        ext = inode[0x28:0x64]
        if u16(ext, 0) != 0xF30A: raise ValueError("invalid extent header")
        count, depth = u16(ext, 2), u16(ext, 6)
        if depth != 0: raise ValueError("extent tree depth > 0: unsupported")
        chunks = []
        for k in range(count):
            off = 12 + k*12
            logical = u32(ext, off)
            count_blocks = u16(ext, off+4)
            physical = (u16(ext, off+6)<<32) | u32(ext, off+8)
            if count_blocks == 0 or count_blocks > 32768: raise ValueError("invalid extent length")
            if count_blocks & 0x8000: raise ValueError("uninitialized extent unsupported")
            chunks.append((logical, count_blocks, physical))
        chunks.sort()
        result = bytearray(size)
        if size > 32*1024*1024: raise ValueError("size over test reader limit")
        for logical, length, physical in chunks:
            pos = logical * self.block_size
            if pos >= size: continue
            n = min(length * self.block_size, size-pos)
            result[pos:pos+n] = self.read(physical * self.block_size, n)
        return bytes(result)
    def root_files(self):
        raw = self.payload(2)
        entries = {}
        off = 0
        while off + 8 <= len(raw):
            inode = u32(raw,off)
            rec = u16(raw,off+4)
            name_length = raw[off+6]
            if rec < 8 or off+rec > len(raw): raise ValueError("bad directory record")
            if inode and name_length and name_length <= rec-8:
                name = raw[off+8:off+8+name_length].decode("utf-8","strict")
                entries[name] = inode
            off += rec
        return entries

def inspect(image, filename, expected):
    with Ext4Reader(image) as e:
        entries=e.root_files()
        if filename not in entries: raise ValueError("missing "+filename)
        content=e.payload(entries[filename])
        digest=hashlib.sha256(content).hexdigest()
        if digest != hashlib.sha256(Path(expected).read_bytes()).hexdigest():
            raise ValueError("independent ext4 payload SHA256 differs: "+filename)
        return {"image":str(image),"filename":filename,"inode":entries[filename],
                "size":len(content),"sha256":digest,"block_size":e.block_size,
                "shared_blocks":bool(e.rocompat & 0x4000)}
if __name__ == "__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("image",type=Path)
    ap.add_argument("filename")
    ap.add_argument("expected",type=Path)
    a=ap.parse_args()
    print(inspect(a.image,a.filename,a.expected))
