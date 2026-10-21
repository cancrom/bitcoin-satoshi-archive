"""Synthetic PE structural tests, not historic bitcoin.exe verification."""
import struct
import unittest
from inspect_pe import inspect

def make_pe():
    buf=bytearray(1024)
    buf[:2]=b'MZ'
    struct.pack_into('<I',buf,0x3c,0x80)
    buf[0x80:0x84]=b'PE\x00\x00'
    struct.pack_into('<HHIIIHH',buf,0x84,0x14c,1,1231629360,0,0,224,0)
    opt=0x98
    struct.pack_into('<H',buf,opt,0x10b)
    buf[opt+2]=2
    buf[opt+3]=56
    struct.pack_into('<I',buf,opt+16,4768)
    struct.pack_into('<I',buf,opt+28,0x400000)
    struct.pack_into('<H',buf,opt+68,2)
    struct.pack_into('<H',buf,opt+70,0)
    struct.pack_into('<I',buf,opt+92,16)
    sec=opt+224
    buf[sec:sec+5]=b'.text'
    struct.pack_into('<I',buf,sec+16,512)
    return bytes(buf)

class PETests(unittest.TestCase):
    def test_header_values(self):
        out=inspect(make_pe())
        self.assertEqual(out['machine'],'0x014c')
        self.assertEqual(out['linker_version'],'2.56')
        self.assertEqual(out['entry_point_rva'],4768)
        self.assertEqual(out['image_base'],'0x00400000')
        self.assertEqual(out['subsystem'],2)
        self.assertFalse(out['aslr_flag'])
        self.assertFalse(out['nx_flag'])
        self.assertFalse(out['authenticode_table_present'])
        self.assertEqual(out['sections'],[{'name':'.text','raw_size':512}])
        self.assertTrue(out['coff_header_timestamp_untrusted'])

    def test_reject_empty(self):
        with self.assertRaises(ValueError):inspect(b'')

    def test_reject_bad_signature(self):
        payload=bytearray(make_pe())
        payload[0x80:0x84]=b'NOPE'
        with self.assertRaises(ValueError):inspect(bytes(payload))

    def test_reject_truncated_sections(self):
        payload=bytearray(make_pe())
        struct.pack_into('<H',payload,0x86,90)
        with self.assertRaises(ValueError):inspect(bytes(payload))

if __name__=='__main__':
    unittest.main()
