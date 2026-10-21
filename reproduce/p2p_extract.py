#!/usr/bin/env python3
"""Read S1 P2P ZIP and aggregate seven HTML/mbox structural metrics.

Standard library only; no remote access and no published message bodies,
Message-IDs, addresses, or local paths. This does NOT solve three historical
body/thread normalization discrepancies.
"""
from __future__ import annotations
import argparse, gzip, hashlib, html, io, json, mailbox, re, tempfile, urllib.parse, zipfile
from collections import Counter
from email import policy
from email.parser import BytesParser
from html.parser import HTMLParser
from pathlib import Path

HTML_FILE = re.compile(r'(?:^|/)(\d{6})\.html$', re.I)
MBOX_FILE = re.compile(r'(?:^|/)\d{4}-[A-Za-z]+\.txt(?:\.gz)?$', re.I)
MID = re.compile(r'<[^<>\s]+@[^<>\s]+>')
LIMIT_MEMBER = 64 * 1024 * 1024

def mid(value: str | None) -> str:
    match = MID.search(html.unescape(value or ''))
    return match.group(0) if match else ''

def subject(value: str | None) -> str:
    return re.sub(r'\s+', ' ', html.unescape(value or '').replace('\xa0', ' ')).strip()

class HTMLFields(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.message_id = ''
        self.inside_h1 = False
        self.subject_parts = []

    def handle_starttag(self, tag, attrs):
        attrs = {k.lower(): v or '' for k, v in attrs}
        if tag.lower() == 'link' and attrs.get('rel', '').lower() == 'made':
            href = html.unescape(attrs.get('href', ''))
            match = re.search(r'(?i)(?:\?|&)In-Reply-To=([^&#]*)', href)
            if match: self.message_id = mid(urllib.parse.unquote(match.group(1)))
        if tag.lower() == 'h1': self.inside_h1 = True

    def handle_endtag(self, tag):
        if tag.lower() == 'h1': self.inside_h1 = False

    def handle_data(self, content):
        if self.inside_h1: self.subject_parts.append(content)

def html_record(content: bytes) -> tuple[str, str]:
    parser = HTMLFields()
    parser.feed(content.decode('utf-8', 'replace'))
    return parser.message_id, subject(' '.join(parser.subject_parts))

def mbox_records(content: bytes) -> list[tuple[str, str]]:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / 'month.mbox'
        path.write_bytes(content)
        mbox = mailbox.mbox(path, factory=lambda file: BytesParser(policy=policy.default).parse(file),
                            create=False)
        try:
            return [(mid(str(msg.get('Message-ID', '') or '')),
                     subject(str(msg.get('Subject', '') or ''))) for msg in mbox]
        finally:
            mbox.close()

def summary(path: Path) -> dict:
    digest = hashlib.sha256()
    with path.open('rb') as inp:
        for chunk in iter(lambda: inp.read(1024 * 1024), b''):
            digest.update(chunk)
    html_rows, mbox_rows, months = [], [], 0
    with zipfile.ZipFile(path) as archive:
        for info in archive.infolist():
            if info.is_dir(): continue
            is_html = bool(HTML_FILE.search(info.filename))
            is_month = bool(MBOX_FILE.search(info.filename))
            if not (is_html or is_month): continue
            if info.file_size > LIMIT_MEMBER: raise ValueError('member size exceeds limit')
            content = archive.read(info)
            if len(content) > LIMIT_MEMBER: raise ValueError('member exceeds limit')
            if is_html:
                html_rows.append(html_record(content))
            else:
                months += 1
                if info.filename.lower().endswith('.gz'):
                    with gzip.GzipFile(fileobj=io.BytesIO(content)) as stream:
                        content = stream.read(LIMIT_MEMBER + 1)
                    if len(content) > LIMIT_MEMBER: raise ValueError('mbox too large')
                mbox_rows.extend(mbox_records(content))
    counts = Counter(key for key, _ in mbox_rows if key)
    all_mbox = set(counts)
    all_html = {key for key, _ in html_rows if key}
    mbox_subjects = {}
    for key, value in mbox_rows:
        if key and key not in mbox_subjects: mbox_subjects[key] = value
    return {
        'archive_sha256': digest.hexdigest(),
        'html_message_pages': len(html_rows),
        'monthly_archives': months,
        'monthly_messages': len(mbox_rows),
        'html_pages_matching_monthly_id': sum(bool(k and k in all_mbox) for k, _ in html_rows),
        'html_pages_without_monthly_match': sum(not k or k not in all_mbox for k, _ in html_rows),
        'unique_monthly_ids_without_html': len(all_mbox - all_html),
        'equal_subject_rows': sum(bool(k and mbox_subjects.get(k) == subj)
                                  for k, subj in html_rows),
        'monthly_messages_without_id': sum(not key for key, _ in mbox_rows),
        'duplicate_monthly_id_groups': sum(count > 1 for count in counts.values()),
        'method': 'strict HTML rel=made In-Reply-To, case-sensitive Message-ID, page-wise counting',
        'limits': 'no bodies or author identities exported; 3 historical body/thread metrics omitted'
    }

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = json.dumps(summary(args.archive), ensure_ascii=False, indent=2)
    print(result)
    if args.output: args.output.write_text(result + '\n', encoding='utf-8')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
