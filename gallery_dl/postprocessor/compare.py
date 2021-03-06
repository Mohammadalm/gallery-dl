# -*- coding: utf-8 -*-

# Copyright 2020 Mike Fährmann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Compare versions of the same file and replace/enumerate them on mismatch"""

from .common import PostProcessor
import os


class ComparePP(PostProcessor):

    def __init__(self, pathfmt, options):
        PostProcessor.__init__(self)
        if options.get("action") == "enumerate":
            self.run = self._run_enumerate
        if options.get("shallow"):
            self.compare = self._compare_size

    def run(self, pathfmt):
        try:
            if self.compare(pathfmt.realpath, pathfmt.temppath):
                pathfmt.delete = True
        except OSError:
            pass

    def _run_enumerate(self, pathfmt):
        num = 1
        try:
            while not self.compare(pathfmt.realpath, pathfmt.temppath):
                pathfmt.prefix = str(num) + "."
                pathfmt.set_extension(pathfmt.extension, False)
                num += 1
            pathfmt.delete = True
        except OSError:
            pass

    def compare(self, f1, f2):
        return self._compare_size(f1, f2) and self._compare_content(f1, f2)

    @staticmethod
    def _compare_size(f1, f2):
        return os.stat(f1).st_size == os.stat(f2).st_size

    @staticmethod
    def _compare_content(f1, f2):
        size = 16384
        with open(f1, "rb") as fp1, open(f2, "rb") as fp2:
            while True:
                buf1 = fp1.read(size)
                buf2 = fp2.read(size)
                if buf1 != buf2:
                    return False
                if not buf1:
                    return True


__postprocessor__ = ComparePP
