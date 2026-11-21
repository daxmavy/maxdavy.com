import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import sync_gdoc

EXPORT = "My title\n\n*Intro\\!*\n\n1. One  \n   1. Sub\n"
PAGE = '---\ntitle: Old\ndescription: Kept\ndate: 2026-11-21\ngdoc: abc123\n---\nold body\n'


class SplitExport(unittest.TestCase):
    def test_first_line_is_title_and_rest_is_body_unchanged(self):
        title, body = sync_gdoc.split_export(EXPORT)
        self.assertEqual(title, "My title")
        self.assertEqual(body, "*Intro\\!*\n\n1. One  \n   1. Sub\n")

    def test_empty_body_is_an_error(self):
        with self.assertRaises(ValueError):
            sync_gdoc.split_export("Only a title\n\n")


class RenderPage(unittest.TestCase):
    def test_replaces_title_and_body_and_keeps_other_front_matter(self):
        out = sync_gdoc.render_page(PAGE, EXPORT)
        self.assertEqual(
            out,
            '---\ntitle: "My title"\ndescription: Kept\ndate: 2026-11-21\ngdoc: abc123\n---\n'
            "*Intro\\!*\n\n1. One  \n   1. Sub\n",
        )

    def test_doc_id_read_from_front_matter(self):
        self.assertEqual(sync_gdoc.doc_id(PAGE), "abc123")
        self.assertIsNone(sync_gdoc.doc_id("---\ntitle: x\n---\nbody\n"))


class SyncAll(unittest.TestCase):
    def test_only_pages_with_a_gdoc_key_are_rewritten_and_failures_keep_the_old_copy(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            linked, plain, broken = root / "a.md", root / "b.md", root / "c.md"
            linked.write_text(PAGE)
            plain.write_text("---\ntitle: x\n---\nbody\n")
            broken.write_text(PAGE.replace("abc123", "bad"))

            def fetch(doc):
                if doc == "bad":
                    raise OSError("boom")
                return EXPORT

            failed = sync_gdoc.sync_all(root, fetch)
            self.assertIn("My title", linked.read_text())
            self.assertEqual(plain.read_text(), "---\ntitle: x\n---\nbody\n")
            self.assertIn("old body", broken.read_text())
            self.assertEqual(failed, [broken])


if __name__ == "__main__":
    unittest.main()
