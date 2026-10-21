#!/usr/bin/env python3
"""Check acquired S1-S9 source archives against historic SHA-256 values.

Missing artifacts stay MISSING, never PASS. Optionally inspect ZIP/TAR
member names and types without extracting or executing files. Prior reported
hashes are references, not newly verified evidence.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import re
import stat
import tarfile
import zipfile
from pathlib import Path, PurePosixPath

def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()

def safe_name(name: str) -> bool:
    if not name or '\\' in name or '\0' in name or name.startswith('/'):
        return False
    parts = PurePosixPath(name).parts
    return bool(parts) and '..' not in parts and ':' not in parts[0]

def inspect_archive(path: Path, max_members: int = 500000) -> dict:
    n = 0
    if zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as archive:
            for item in archive.infolist():
                n += 1
                if n > max_members: return {'safe': False, 'reason': 'too many members'}
                mode = (item.external_attr >> 16) & 0xffff
                if not safe_name(item.filename) or stat.S_ISLNK(mode):
                    return {'safe': False, 'reason': 'unsafe member or symlink'}
    elif tarfile.is_tarfile(path):
        with tarfile.open(path, 'r:*') as archive:
            for item in archive:
                n += 1
                if n > max_members: return {'safe': False, 'reason': 'too many members'}
                if not safe_name(item.name) or not (item.isfile() or item.isdir()):
                    return {'safe': False, 'reason': 'unsafe member or type'}
    else:
        return {'safe': None, 'reason': 'not recognized as ZIP or TAR'}
    return {'safe': True, 'members': n, 'reason': 'listing only; no extraction'}

def load_manifest(path: Path) -> list[dict[str, str]]:
    with path.open(encoding='utf-8-sig', newline='') as stream:
        rows = list(csv.DictReader(stream))
    if not rows or not {'id', 'filename', 'sha256'} <= rows[0].keys():
        raise ValueError('manifest requires id, filename, sha256')
    ids, names = set(), set()
    for row in rows:
        key, name, expected = row['id'], row['filename'], row['sha256']
        if key in ids or name in names or not key or not safe_name(name) or '/' in name:
            raise ValueError('duplicate identifier or unsafe filename')
        if not re.fullmatch(r'[A-Fa-f0-9]{64}', expected):
            raise ValueError('invalid expected SHA-256')
        ids.add(key)
        names.add(name)
    return rows

def audit(folder: Path, manifest: list[dict[str, str]], inspect: bool=False) -> list[dict]:
    root = folder.resolve()
    report = []
    for row in manifest:
        filename = row['filename']
        file = root / filename
        item = {'id': row['id'], 'filename': filename, 'status': 'MISSING',
                'expected_sha256': row['sha256'].lower()}
        if file.is_symlink():
            item['status'] = 'UNSAFE_FILE'
        elif file.is_file() and file.resolve().parent == root:
            item['size_bytes'] = file.stat().st_size
            item['actual_sha256'] = sha256(file)
            item['status'] = 'MATCH' if item['actual_sha256'] == item['expected_sha256'] else 'MISMATCH'
            if inspect:
                try:
                    item['member_audit'] = inspect_archive(file)
                    if item['member_audit']['safe'] is False:
                        item['status'] = 'UNSAFE_ARCHIVE'
                except (OSError, ValueError, tarfile.TarError, zipfile.BadZipFile) as exc:
                    item['status'] = 'ARCHIVE_ERROR'
                    item['error_type'] = type(exc).__name__
        report.append(item)
    return report

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory', type=Path, required=True)
    parser.add_argument('--manifest', type=Path,
                        default=Path(__file__).resolve().parent.parent/'evidence'/'ARCHIVE-MANIFEST.csv')
    parser.add_argument('--inspect-members', action='store_true')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    rows = audit(args.directory, load_manifest(args.manifest), args.inspect_members)
    result = {'results': rows, 'totals': {s: sum(r['status']==s for r in rows)
             for s in sorted({r['status'] for r in rows})}}
    output = json.dumps(result, ensure_ascii=False, indent=2)
    print(output)
    if args.output: args.output.write_text(output+'\n', encoding='utf-8')
    return 0 if all(r['status']=='MATCH' for r in rows) else 1

if __name__ == '__main__':
    raise SystemExit(main())
