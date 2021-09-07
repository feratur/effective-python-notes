# Item 18: Know How to Construct Key-Dependent Default Values with __missing__

# there are times when neither setdefault nor defaultdict is the right fit.
pictures = {}
path = 'profile_1234.png'
if (handle := pictures.get(path)) is None:
    try:
        handle = open(path, 'a+b')
    except OSError:
        print(f'Failed to open path {path}')
        raise
    else:
        pictures[path] = handle
handle.seek(0)
image_data = handle.read()

# or
try:
    handle = pictures.setdefault(path, open(path, 'a+b'))
except OSError:
    print(f'Failed to open path {path}')
    raise
else:
    handle.seek(0)
    image_data = handle.read()
# This code has many problems.
# This results in an additional file handle that may conflict with
# existing open handles in the same program. Exceptions may be raised
# by the open call and need to be handled

from collections import defaultdict
def open_picture(profile_path):
    try:
        return open(profile_path, 'a+b')
    except OSError:
        print(f'Failed to open path {profile_path}')
        raise
# But the code below raises exception
# defaultdict expects that the function passed to its constructor
# doesn’t require any arguments
#
# pictures = defaultdict(open_picture)
# handle = pictures[path]
# handle.seek(0)
# image_data = handle.read()

# You can subclass the dict type and imple- ment the __missing__ special
# method to add custom logic for handling missing keys.
class Pictures(dict):
    def __missing__(self, key):
        value = open_picture(key)
        self[key] = value
        return value
pictures = Pictures()
handle = pictures[path]
handle.seek(0)
image_data = handle.read()

# When the pictures[path] dictionary access finds that the path key
# isn’t present in the dictionary, the __missing__ method is called.
# This method must create the new default value for the key, insert
# it into the dictionary, and return it to the caller. Subsequent
# accesses of the same path will not call __missing__ since the
# corresponding item is already present.

# ✦ The setdefault method of dict is a bad fit when creating the default
# value has high computational cost or may raise exceptions.
# ✦ The function passed to defaultdict must not require any arguments,
# which makes it impossible to have the default value depend on the key
# being accessed.
# ✦ You can define your own dict subclass with a __missing__ method in
# order to construct default values that must know which key was being accessed.
