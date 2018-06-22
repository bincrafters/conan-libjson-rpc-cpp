#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from bincrafters import build_template_default

if __name__ == "__main__":

    build_policy = os.getenv("CONAN_BUILD_POLICY", "missing")
    os.environ["CONAN_BUILD_POLICY"] = build_policy
    builder = build_template_default.get_builder(pure_c=False)
    builder.run()
