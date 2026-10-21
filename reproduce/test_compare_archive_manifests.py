"""Synthetic archive-manifest tests; not a historical RAR/TGZ reproduction."""
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from compare_archive_manifests import compare,read_manifest

class ContainerTests(unittest.TestCase):
    def test_comparison(self):
        a={'one':{'size':4,'crc32':'12345678','timestamp':datetime(2009,1,10,10)},
           'two':{'size':6,'crc32':'abcdef12','timestamp':datetime(2009,1,10,10)}}
        b={'one':{'size':4,'crc32':'12345678','timestamp':datetime(2009,1,10,18)},
           'two':{'size':6,'crc32':'abcdef12','timestamp':datetime(2009,1,10,18)}}
        result=compare(a,b)
        self.assertTrue(result['all_paths_and_crc_equal'])
        self.assertEqual(result['matching_paths'],2)
        self.assertEqual(result['uniform_offset_seconds'],28800)

    def test_csv_and_mismatch(self):
        with tempfile.TemporaryDirectory() as td:
            a,b=Path(td)/'a.csv',Path(td)/'b.csv'
            a.write_text('path,size,crc32,timestamp_value\nfile.cpp,2,00000001,2009-01-01T00:00:00\n')
            b.write_text('path,size,crc32,timestamp_value\nfile.cpp,3,00000001,2009-01-01T08:00:00\n')
            parsed_a,parsed_b=read_manifest(a),read_manifest(b)
            self.assertFalse(compare(parsed_a,parsed_b)['all_paths_and_crc_equal'])

    def test_duplicate_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            f=Path(td)/'a.csv'
            f.write_text('path,size,crc32,timestamp_value\nx,1,ffffffff,2009-01-01T00:00:00\nx,1,ffffffff,2009-01-01T00:00:00\n')
            with self.assertRaises(ValueError):read_manifest(f)

if __name__=='__main__':
    unittest.main()
