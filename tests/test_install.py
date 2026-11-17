import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from ba_core import BAError
from install_skills import install


class InstallTests(unittest.TestCase):
    def test_portable_resources_idempotence_and_local_conflict(self):
        with tempfile.TemporaryDirectory() as temp:
            dest = Path(temp) / ".agents" / "skills"
            plan = install(dest)
            self.assertEqual(len(plan), 9)
            self.assertFalse(dest.exists())
            install(dest, apply=True)
            self.assertTrue(all(i["action"] == "skip" for i in install(dest)))
            for item in plan:
                folder = Path(item["target"])
                self.assertTrue((folder / "references/kit/scripts/validate_ba_document.py").is_file())
                self.assertIn("references/kit/contracts/", (folder / "SKILL.md").read_text(encoding="utf-8"))
            skill = dest / "ba-spec/SKILL.md"
            skill.write_text(skill.read_text(encoding="utf-8") + "\nLocal customization\n", encoding="utf-8")
            before = skill.read_bytes()
            with self.assertRaises(BAError):
                install(dest, apply=True, update=True)
            self.assertEqual(skill.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
