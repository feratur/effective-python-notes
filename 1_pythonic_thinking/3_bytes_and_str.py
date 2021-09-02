a = b'h\x65llo'
print(list(a))
print(a)
# >>>
# [104, 101, 108, 108, 111]
# b'hello'

# Instances of bytes contain raw, unsigned 8-bit 
# values (often displayed in the ASCII encoding)

# Instances of str contain Unicode code points that represent textual 
# characters from human languages
a = 'a\u0300 propos'
print(list(a))
print(a)
# >>>
# ['a', '`', ' ', 'p', 'r', 'o', 'p', 'o', 's']
# à propos

# str instances do not have an associated binary encoding, and bytes instances
# do not have an associated text encoding. To convert Unicode data to binary data,
# you must call the encode method of str. To convert binary data to Unicode data,
# you must call the decode method of bytes.

# can add bytes to bytes and str to str, respectively
print(b'one' + b'two')
print('one' + 'two')
# can’t add str instances to bytes instances

# can compare bytes to bytes and str to str, respectively
assert b'red' > b'blue'
assert 'red' > 'blue'
# can’t compare a str instance to a bytes instance

# Comparing bytes and str instances for equality will always evaluate to False,
# even when they contain exactly the same characters
print(b'foo' == 'foo')

# The % operator works with format strings for each type, respectively
print(b'red %s' % b'blue')
print('red %s' % 'blue')

# You can pass a bytes instance to a str format string using the
# % operator, but it doesn’t do what you’d expect:
print('red %s' % b'blue')
# red b'blue'
# This code actually invokes the __repr__ method
# on the bytes instance and sub- stitutes that in place of the %s,
# which is why b'blue' remains escaped in the output.

# Operations involving file handles (returned by the open built-in function)
# default to requiring Unicode strings instead of raw bytes.
# with open('data.bin', 'w') as f:
#     f.write(b'\xf1\xf2\xf3\xf4\xf5')
# causes error write() argument must be str, not bytes
# instead use
# with open('data.bin', 'wb') as f:
#     f.write(b'\xf1\xf2\xf3\xf4\xf5')

# When a handle is in text mode, it uses the system’s default text encoding
# to interpret binary data
# with open('data.bin', 'r') as f:
#     data = f.read()
# if opened like this system’s default text encoding will be used to decode file
# unlike in mode 'rb' - which returns bytes
# or encoding can be set explicitly
# with open('data.bin', 'r', encoding='cp1252') as f:
#     data = f.read()
import locale
print(locale.getpreferredencoding())

# ✦ bytes contains sequences of 8-bit values, and str contains sequences of
# Unicode code points.
# ✦ Use helper functions to ensure that the inputs you operate on are the type of
# character sequence that you expect (8-bit values, UTF-8-encoded strings,
# Unicode code points, etc).
# ✦ bytes and str instances can’t be used together with operators (like >, ==, +, and %).
# ✦ If you want to read or write binary data to/from a file, always open the file using
# a binary mode (like 'rb' or 'wb').
# ✦ If you want to read or write Unicode data to/from a file, be care- ful about your
# system’s default text encoding. Explicitly pass the encoding parameter to open if
# you want to avoid surprises.
