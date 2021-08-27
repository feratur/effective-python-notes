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
