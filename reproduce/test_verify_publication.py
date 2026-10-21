"""Synthetic HTML pages for local/cross-page anchor validator."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import verify_publication as pv

def page(href: str, anchor: str = 'target') -> str:
    return ('<!doctype html><html lang="fr"><body>'
            f'<div id="{anchor}" data-fr="Bonjour" data-en="Hello">Bonjour</div>'
            f'<a href="{href}">Read</a></body></html>')

class PublicationTests(unittest.TestCase):
    def test_valid_cross_page_anchor(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            (root/'index.html').write_text(page('proofs.html#target'))
            (root/'proofs.html').write_text(page('#target'))
            with patch.object(pv,'ROOT',root):
                self.assertEqual(pv.check_page(root/'index.html'), [])

    def test_missing_cross_page_anchor(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            (root/'index.html').write_text(page('proofs.html#missing'))
            (root/'proofs.html').write_text(page('#target'))
            with patch.object(pv,'ROOT',root):
                self.assertTrue(any('cross-page anchor' in err for err in pv.check_page(root/'index.html')))

    def test_missing_file_and_duplicate_id(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            (root/'index.html').write_text(page('missing.html')+'<div id="target"></div>')
            with patch.object(pv,'ROOT',root):
                errors=pv.check_page(root/'index.html')
                self.assertTrue(any('missing local file' in err for err in errors))
                self.assertTrue(any('duplicate HTML id' in err for err in errors))

if __name__=='__main__':
    unittest.main()
