# Copyright (c) 2011 Kevin Skusek
# The full copyright notice can be found in the file LICENSE

files = []
import os, fnmatch
dir = os.listdir('.')
for file in dir:
	if fnmatch.fnmatch(file,'*.py'):
		files.append(file)

__all__ = files