
import os, fnmatch

def all_files(root, patterns = '*', single_level = False, yield_folders=False):
    patterns = patterns.split(';')
    for path, subdirs, files in os.walk(root):
        if yield_folders:
            files.extend(subdirs)
        files.sort()
        for name in files:
            for pattern in patterns:
                if fnmatch.fnmatch(name, pattern):
                    yield os.path.join(path,name)
                    break
        if single_level:
            break

if __name__ == '__main__':
    for path in all_files('/home/dan/ownCloud/Multimedia/GPU/new/GPU','*.py;*html;*pdf'):
        print path