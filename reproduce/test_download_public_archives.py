"""Offline tests for the opt-in S1/S9 downloader; no network traffic."""
from __future__ import annotations
import hashlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from download_public_archives import check_url, download_file

URL = 'https://diyhpl.us/~bryan/irc/bitcoin/bitcoin-logs.2010-2018.tar.bz2'

class FakeHTTP(io.BytesIO):
    def __enter__(self): return self
    def __exit__(self, *args): self.close()
    def geturl(self): return URL

class DownloadTests(unittest.TestCase):
    def test_reject_insecure_and_unrelated_hosts(self):
        for url in ('http://diyhpl.us/~bryan/irc/test',
                    'https://example.com/~bryan/irc/bitcoin/x',
                    'https://diyhpl.us.evil.example/~bryan/irc/x'):
            with self.assertRaises(ValueError):
                check_url(url)

    def test_matching_bytes_saved(self):
        body = b'synthetic-not-bitcoin-history'
        with tempfile.TemporaryDirectory() as td:
            output = Path(td) / 'synthetic.tar.bz2'
            with patch('download_public_archives.urllib.request.urlopen',
                       return_value=FakeHTTP(body)):
                actual = download_file(URL, output, hashlib.sha256(body).hexdigest(), len(body))
            self.assertEqual(actual['status'], 'MATCH')
            self.assertEqual(output.read_bytes(), body)

    def test_mismatching_hash_does_not_publish(self):
        body = b'not-the-expected-hash'
        with tempfile.TemporaryDirectory() as td:
            output = Path(td) / 'synthetic.tar.bz2'
            with patch('download_public_archives.urllib.request.urlopen',
                       return_value=FakeHTTP(body)):
                with self.assertRaises(ValueError):
                    download_file(URL, output, '0'*64, len(body))
            self.assertFalse(output.exists())
            self.assertFalse(output.with_suffix(output.suffix+'.part').exists())

    def test_size_mismatch_does_not_publish(self):
        body = b'hello'
        with tempfile.TemporaryDirectory() as td:
            output = Path(td) / 'synthetic.tar.bz2'
            with patch('download_public_archives.urllib.request.urlopen',
                       return_value=FakeHTTP(body)):
                with self.assertRaises(ValueError):
                    download_file(URL, output, hashlib.sha256(body).hexdigest(), len(body)+1)
            self.assertFalse(output.exists())

if __name__ == '__main__':
    unittest.main()
