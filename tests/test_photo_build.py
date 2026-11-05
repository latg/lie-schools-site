import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from html.parser import HTMLParser


ROOT = Path(__file__).resolve().parents[1]
PHOTO_BASE = "https://photos.example.test/bucket"


class Links(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.urls = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        self.urls.extend((tag, key, value) for key, value in attrs
                         if key in ("href", "src") and value)


class PhotoBuildTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.site = Path(self.temp.name)
        for directory in ("content", "layouts"):
            shutil.copytree(ROOT / directory, self.site / directory)
        shutil.copyfile(ROOT / "config.toml", self.site / "config.toml")
        # Real asset paths with tiny contents keep this check fast and offline.
        for source in (ROOT / "static").rglob("*"):
            if source.is_file():
                target = self.site / source.relative_to(ROOT)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(b"fixture")

    def build(self, base="", wrapper=False):
        env = dict(os.environ, HUGO_PARAMS_PHOTOBASEURL=base,
                   HUGO_STATICDIR="static", HUGO_CANONIFYURLS="false",
                   HUGO_BASEURL="https://lie-school.ru/", HUGO_PUBLISHDIR="public")
        command = ["sh", str(ROOT / "build.sh")] if wrapper else ["hugo"]
        subprocess.run(command, cwd=self.site, env=env, check=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return {str(p.relative_to(self.site / "public")): Links(p.read_text()).urls
                for p in (self.site / "public").rglob("*.html")}

    def test_photo_urls_switch_without_changing_other_links(self):
        local = self.build()
        for base in (PHOTO_BASE, PHOTO_BASE + "/"):
            remote = self.build(base)
            self.assertEqual(local.keys(), remote.keys())
            changed = 0
            for page, links in local.items():
                parts = Path(page).parts
                expected = links
                if len(parts) == 3 and parts[1] == "photo":
                    expected = [(tag, key, PHOTO_BASE + "/" + parts[0] + "/" + url[3:]
                                 if url.startswith("../") else url)
                                for tag, key, url in links]
                    changed += sum(a != b for a, b in zip(links, expected))
                self.assertEqual(expected, remote[page], page)
            self.assertGreater(changed, 0)
        self.assertEqual(local, self.build())

    def test_external_build_excludes_photos_and_preserves_gallery_pages(self):
        local = self.build(wrapper=True)
        output = self.site / "public"
        photos = ["2009/Photos/1.jpg", "2009/Previews/1.jpg", "2017/Everyone.jpg",
                  "2018/photo/DSC02524.png", "2018/photo/small/DSC02524.png",
                  "2023/photos/1.jpg", "2023/previews/1.jpg"]
        for photo in photos:
            self.assertTrue((output / photo).is_file(), photo)
        remote = self.build(PHOTO_BASE, wrapper=True)
        for photo in photos:
            self.assertFalse((output / photo).exists(), photo)
        self.assertEqual(local.keys(), remote.keys())
        self.assertTrue((output / "2018/photo/index.html").is_file())
        for asset in ("main_files/main.css", "main_files/conf-logo.png", "2023/poster.jpg"):
            self.assertTrue((output / asset).is_file(), asset)
        self.assertEqual(local, self.build(wrapper=True))
        for photo in photos:
            self.assertTrue((output / photo).is_file(), photo)


if __name__ == "__main__":
    unittest.main()
