# This file is licensed under CC0 (http://creativecommons.org/publicdomain/zero/1.0/)

files = []
import os, fnmatch
dir = os.listdir('.')
for file in dir:
    if fnmatch.fnmatch(file,'*.py'):
        files.append(file)

__all__ = files