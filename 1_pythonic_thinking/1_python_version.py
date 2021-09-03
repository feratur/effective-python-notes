# Item 1: Know Which Version of Python You’re Using

import sys
print(sys.version_info)
print(sys.version)

# >>>
# sys.version_info(major=3, minor=8, micro=0, 
# ➥releaselevel='final', serial=0)
# 3.8.0 (default, Oct 21 2019, 12:51:32) 
# [Clang 6.0 (clang-600.0.57)]

# ✦ Python 3 is the most up-to-date and well-supported version of 
# Python, and you should use it for your projects.
# ✦ Be sure that the command-line executable for running Python on 
# your system is the version you expect it to be.
# ✦ Avoid Python 2 because it will no longer be maintained after January 1, 
# 2020.
