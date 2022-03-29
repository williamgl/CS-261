import sys

cur_version = sys.version_info

if cur_version >= (3,6):
    print("This is an acceptable version of Python, version " + str(cur_version[0]) + '.' + str(cur_version[1]) + '.')
else:
    print("Your Python version is too low, it needs to be 3.6 or greater and this is " + str(cur_version[0]) + '.' + str(cur_version[1]) + '.')


