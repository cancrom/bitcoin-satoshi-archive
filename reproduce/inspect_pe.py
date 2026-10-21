#!/usr/bin/env python3
"""Inspect a historical Windows PE file offline (stdlib only).

Does not execute the binary or contact a network. Emits no local path, embedded
string, wallet content or personally identifying metadata. A PE COFF timestamp
is an untrusted header field, not independent proof of compilation time.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import struct
from datetime import datetime, timezone
from pathlib import Path

def u16(buf: bytes, at: int) -> int:
    return struct.unpack_from('<H', buf, at)[0]

def u32(buf: bytes, at: int) -> int:
    return struct.unpack_from('<I', buf, at)[0]

def inspect(data: bytes) -> dict:
    if len(data) < 0x40 or data[:2] != b'MZ':
        raise ValueError('missing DOS header')
    pe = u32(data, 0x3c)
    if pe < 0x40 or pe + 24 > len(data) or data[pe:pe+4] != b'PE\x00\x00':
        raise ValueError('missing or truncated PE header')
    machine, sections, timestamp, _, _, opt_size, _ = struct.unpack_from('<HHIIIHH', data, pe + 4)
    opt = pe + 24
    if opt_size < 96 or opt + opt_size > len(data):
        raise ValueError('truncated PE optional header')
    magic = u16(data, opt)
    if magic not in (0x10b, 0x20b):
        raise ValueError('unsupported PE optional header format')
    is64 = magic == 0x20b
    if opt_size < (112 if is64 else 96):
        raise ValueError('incomplete PE optional header')
    image_base = struct.unpack_from('<Q', data, opt+24)[0] if is64 else u32(data, opt+28)
    subsys = u16(data, opt+(88 if is64 else 68))
    dll_chars = u16(data, opt+(90 if is64 else 70))
    dir_count = u32(data, opt+(108 if is64 else 92))
    cert_offset = opt+(112 if is64 else 96)+8*4
    cert_present = bool(dir_count > 4 and cert_offset+8 <= opt+opt_size and
                        (u32(data, cert_offset) or u32(data, cert_offset+4)))
    section_headers_at = opt+opt_size
    if sections > 96 or section_headers_at+40*sections > len(data):
        raise ValueError('truncated or implausible section table')
    section_rows = []
    for i in range(sections):
        at=section_headers_at+i*40
        name=data[at:at+8].split(b'\x00',1)[0].decode('ascii','replace')
        raw_size=u32(data,at+16)
        section_rows.append({'name':name,'raw_size':raw_size})
    return {
      'sha256':hashlib.sha256(data).hexdigest(),
      'size_bytes':len(data),
      'pe_valid':True,
      'machine':f'0x{machine:04x}',
      'coff_header_timestamp_utc':datetime.fromtimestamp(timestamp,timezone.utc).isoformat(),
      'coff_header_timestamp_untrusted':True,
      'linker_version':f'{data[opt+2]}.{data[opt+3]}',
      'entry_point_rva':u32(data,opt+16),
      'image_base':f'0x{image_base:08x}',
      'subsystem':subsys,
      'aslr_flag':bool(dll_chars & 0x40),
      'nx_flag':bool(dll_chars & 0x100),
      'authenticode_table_present':cert_present,
      'sections':section_rows,
    }

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file', type=Path)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    payload=json.dumps(inspect(args.file.read_bytes()),ensure_ascii=False,indent=2)
    print(payload)
    if args.output:args.output.write_text(payload+'\n',encoding='utf-8')

if __name__=='__main__':
    main()
