#!/usr/bin/env python3
"""Compare pre-exported RAR and TGZ member manifests offline.

CSV columns: path,size,crc32,timestamp_value; timestamps must be naive
YYYY-MM-DDTHH:MM:SS values as reported by their respective archive tools.
The method cannot infer where a person lived or when a file was authored.
Does not read, extract or execute either archive.
"""
from __future__ import annotations
import argparse
import csv
import json
import re
from datetime import datetime
from pathlib import Path

def read_manifest(path: Path) -> dict[str, dict]:
    with path.open(encoding='utf-8-sig', newline='') as stream:
        reader=csv.DictReader(stream)
        required={'path','size','crc32','timestamp_value'}
        if not reader.fieldnames or not required <= set(reader.fieldnames):
            raise ValueError('missing path,size,crc32,timestamp_value columns')
        result={}
        for row in reader:
            name=row['path'].strip()
            if (not name or name.startswith('/') or '\\' in name
                or '..' in name.split('/') or name in result):
                raise ValueError('duplicate or unsafe relative path')
            size=int(row['size'])
            if size < 0: raise ValueError('negative file size')
            crc=row['crc32'].lower().removeprefix('0x')
            if not re.fullmatch(r'[0-9a-f]{8}',crc):
                raise ValueError('CRC32 must be 8 hex characters')
            stamp=datetime.fromisoformat(row['timestamp_value'])
            if stamp.tzinfo is not None:raise ValueError('use naive archive timestamp fields')
            result[name]={'size':size,'crc32':crc,'timestamp':stamp}
        return result

def compare(rar: dict[str,dict], tgz: dict[str,dict]) -> dict:
    common=set(rar)&set(tgz)
    identical_size_crc=sum(rar[k]['size']==tgz[k]['size'] and
                           rar[k]['crc32']==tgz[k]['crc32'] for k in common)
    offsets=[int((tgz[k]['timestamp']-rar[k]['timestamp']).total_seconds())
             for k in common]
    unique=sorted(set(offsets))
    return {
      'rar_files':len(rar),
      'tgz_files':len(tgz),
      'matching_paths':len(common),
      'rar_only':len(set(rar)-set(tgz)),
      'tgz_only':len(set(tgz)-set(rar)),
      'size_crc32_matches':identical_size_crc,
      'timestamp_offsets_seconds':unique,
      'uniform_offset_seconds':unique[0] if len(unique)==1 else None,
      'all_paths_and_crc_equal':len(common)==len(rar)==len(tgz)==identical_size_crc,
      'interpretation':'CRC32 is not a cryptographic hash; offsets do not reveal location',
    }

def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rar',type=Path,required=True)
    parser.add_argument('--tgz',type=Path,required=True)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    result=json.dumps(compare(read_manifest(args.rar),read_manifest(args.tgz)),
                      ensure_ascii=False,indent=2,sort_keys=True)
    print(result)
    if args.output: args.output.write_text(result+'\n',encoding='utf-8')

if __name__=='__main__':
    main()
