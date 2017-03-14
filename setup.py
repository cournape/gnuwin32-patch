import hashlib
import os.path
import shutil
import tempfile
import zipfile

from setuptools import setup

import requests


URL = "http://gnuwin32.sourceforge.net/downlinks/patch-bin-zip.php"
URL_SHA256 = "fabd6517e7bd88e067db9bf630d69bb3a38a08e044fa73d13a704ab5f8dd110b"

HERE = os.path.dirname(__file__)
PATCH_EXE = os.path.join(HERE, "patch.exe")

MAJOR = 2
MINOR = 5
MICRO = 9

VERSION = '%d.%d.%d' % (MAJOR, MINOR, MICRO)


def fetch_gnuwin32_patch(target):
    tempdir = tempfile.mkdtemp()
    try:
        archive_target = os.path.join(tempdir, "patch.zip")

        resp = requests.get(URL)
        with open(archive_target, "wb") as fp:
            fp.write(resp.content)

        with open(archive_target, "rb") as fp:
            h = hashlib.sha256()
            h.update(fp.read())

            assert h.hexdigest() == URL_SHA256, "sha256 mismatch"

        with zipfile.ZipFile(archive_target) as zp:
            a = zp.open("bin/patch.exe")
            with open(target, "wb") as fp:
                fp.write(a.read())

    finally:
        shutil.rmtree(tempdir)


def main():
    fetch_gnuwin32_patch(PATCH_EXE)

    setup(
        author="David Cournapeau",
        author_email="cournape@gmail.com",
        name="gnuwin32-patch",
        version=VERSION,
        scripts=[PATCH_EXE],
        description='Wheel containing patch.exe',
        license="GPL",
    )


if __name__ == "__main__":
    main()
