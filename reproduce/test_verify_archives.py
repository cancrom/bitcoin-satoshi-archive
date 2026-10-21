"""Synthetic tests only; these do NOT validate the historical archive hashes."""
import hashlib
import io
import tarfile
import tempfile
import unittest
import zipfile
from pathlib import Path
from verify_archives import audit, inspect_archive, load_manifest

class TestArchiveVerification(unittest.TestCase):
    def test_missing_matching_and_mismatched(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            mf = root / 'manifest.csv'
            mf.write_text('id,filename,sha256\nS0,demo.zip,'+hashlib.sha256(b'abc').hexdigest()+'\n')
            rows = load_manifest(mf)
            self.assertEqual(audit(root, rows)[0]['status'], 'MISSING')
            (root/'demo.zip').write_bytes(b'abc')
            self.assertEqual(audit(root, rows)[0]['status'], 'MATCH')
            (root/'demo.zip').write_bytes(b'xyz')
            self.assertEqual(audit(root, rows)[0]['status'], 'MISMATCH')

    def test_invalid_manifest_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td)/'manifest.csv'
            path.write_text('id,filename,sha256\nS0,../out.zip,'+'0'*64+'\n')
            with self.assertRaises(ValueError): load_manifest(path)

    def test_zip_traversal_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td)/'bad.zip'
            with zipfile.ZipFile(path, 'w') as archive:
                archive.writestr('../escape.txt', 'unsafe')
            self.assertFalse(inspect_archive(path)['safe'])

    def test_tar_symlink_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td)/'bad.tar'
            with tarfile.open(path, 'w') as archive:
                link = tarfile.TarInfo('link')
                link.type = tarfile.SYMTYPE
                link.linkname = '../../outside'
                archive.addfile(link)
            self.assertFalse(inspect_archive(path)['safe'])

    def test_valid_member_listings(self):
        with tempfile.TemporaryDirectory() as td:
            zip_path, tar_path = Path(td)/'ok.zip', Path(td)/'ok.tar'
            with zipfile.ZipFile(zip_path, 'w') as archive:
                archive.writestr('sub/file', 'value')
            with tarfile.open(tar_path, 'w') as archive:
                item = tarfile.TarInfo('sub/file')
                item.size = 3
                archive.addfile(item, io.BytesIO(b'abc'))
            self.assertTrue(inspect_archive(zip_path)['safe'])
            self.assertTrue(inspect_archive(tar_path)['safe'])

if __name__ == '__main__':
    unittest.main()
