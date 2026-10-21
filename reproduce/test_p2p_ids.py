"""Unit tests for the index-comparison method only, NOT for the historic archive."""
import unittest
from p2p_ids import compare


class Comparisons(unittest.TestCase):
    def test_duplicate_html_pages_are_not_collapsed(self):
        result = compare(["A", "A", "B", "C", None], ["A", "B", "D", "D", None])
        self.assertEqual(result["html_page_rows"], 5)
        self.assertEqual(result["matching_html_page_rows"], 3)
        self.assertEqual(result["unmatched_html_page_rows_with_id"], 1)
        self.assertEqual(result["unmatched_mbox_unique_ids"], 1)
        self.assertEqual(result["html_duplicate_id_groups"], 1)
        self.assertEqual(result["mbox_duplicate_id_groups"], 1)

    def test_empty_inputs(self):
        result = compare([], [])
        self.assertEqual(result["matching_html_page_rows"], 0)
        self.assertEqual(result["unmatched_mbox_unique_ids"], 0)


if __name__ == "__main__":
    unittest.main()
