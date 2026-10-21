#!/usr/bin/env python3
"""Download only two explicitly documented public S1/S9 archives, hash first.

No automatic extraction, no TLS downgrade, no unverified relocation.
This tool is opt-in: run manually on a network-connected system.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import os
import sys
import urllib.request
from pathlib import Path
from urllib.parse import urlsplit
from verify_archives import load_manifest

SOURCES = Path(__file__).resolve().parent.parent/'evidence'/'PUBLIC-ARCHIVE-SOURCES.csv'
MANIFEST = Path(__file__).resolve().parent.parent/'evidence'/'ARCHIVE-MANIFEST.csv'
ALLOWED_HOST = 'diyhpl.us'
MAX_MULTIPLIER = 2

def check_url(url: str) -> None:
    u = urlsplit(url)
    if u.scheme != 'https' or u.hostname != ALLOWED_HOST or u.port not in (None, 443):
        raise ValueError('only documented public HTTPS archives at diyhpl.us are permitted')
    if not u.path.startswith('/~bryan/irc/') or u.username or u.password or u.query or u.fragment:
        raise ValueError('untrusted archive URL')

def read_sources() -> dict[str, dict]:
    with SOURCES.open(encoding='utf-8', newline='') as stream:
        rows = list(csv.DictReader(stream))
    sources = {}
    for row in rows:
        check_url(row['url'])
        if row['id'] not in ('S1', 'S9') or row['id'] in sources:
            raise ValueError('unexpected source identifier')
        n = int(row['expected_bytes'])
        if n <= 0 or n > 100_000_000:
            raise ValueError('invalid size bound')
        sources[row['id']] = dict(url=row['url'], bytes=n)
    return sources

def download_file(url: str, output: Path, expected_sha256: str, expected_size: int) -> dict:
    check_url(url)
    if output.exists() or output.is_symlink():
        raise FileExistsError('destination already exists; do not overwrite an archive')
    output.parent.mkdir(parents=True, exist_ok=True)
    part = output.with_name(output.name + '.part')
    if part.exists() or part.is_symlink():
        raise FileExistsError('partial file already exists; inspect or delete it manually')
    h = hashlib.sha256()
    count = 0
    request = urllib.request.Request(url, headers={'User-Agent':'Bitcoin-Historical-Research-Archive-Verifier/1.0'})
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            check_url(response.geturl())
            with part.open('xb') as saved:
                while True:
                    chunk = response.read(1024 * 1024)
                    if not chunk:
                        break
                    count += len(chunk)
                    if count > expected_size * MAX_MULTIPLIER:
                        raise ValueError('download exceeds documented size bound')
                    h.update(chunk)
                    saved.write(chunk)
        digest = h.hexdigest()
        if digest != expected_sha256.lower():
            raise ValueError('SHA-256 mismatch; content not accepted')
        if count != expected_size:
            raise ValueError('byte count does not match historical recorded size')
        part.rename(output)
        return {'status':'MATCH', 'bytes':count, 'sha256':digest, 'filename':output.name}
    finally:
        if part.exists():
            part.unlink()

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--id', choices=('S1','S9'), required=True)
    parser.add_argument('--directory', type=Path, required=True)
    args = parser.parse_args()
    manifest = {row['id']:row for row in load_manifest(MANIFEST)}
    entry = read_sources()[args.id]
    print('Downloading an untrusted historical archive. No extraction or execution will occur.')
    try:
        result = download_file(entry['url'], args.directory/manifest[args.id]['filename'],
                               manifest[args.id]['sha256'], entry['bytes'])
    except (OSError, ValueError) as exc:
        print(f'NOT VERIFIED: {type(exc).__name__}: {exc}', file=sys.stderr)
        return 1
    print(f"VERIFIED {result['filename']} {result['bytes']} bytes SHA-256 {result['sha256']}")
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
