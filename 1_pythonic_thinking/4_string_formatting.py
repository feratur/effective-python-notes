# % formatting operator (The syntax for format specifiers comes from C’s printf function)
# The predefined text template is provided on the left side of the operator
# in a format string. The values to insert into the template are provided as
# a single value or tuple of multiple values on the right side of the format operator.
a = 0b10111011
b = 0xc5f
print('Binary is %d, hex is %d' % (a, b))
# Binary is 187, hex is 3167

# The first problem is that if you change the type or order of data values
# in the tuple on the right side of a formatting expression, you can
# get errors due to type conversion incompatibility.
key = 'my_var'
value = 1.234
formatted = '%-10s = %.2f' % (key, value)
print(formatted)
# my_var     = 1.23
# But if you swap key and value, you get an exception at runtime:
# reordered_tuple = '%-10s = %.2f' % (value, key)
# TypeError: must be real number, not str

# The second problem with C-style formatting expressions is that they become
# difficult to read when you need to make small modifications to values before
# formatting them into a string.

# The third problem with formatting expressions is that if you want to use the
# same value in a format string multiple times, you have to repeat it in the right
# side tuple.
template = '%s loves food. See %s cook.'
name = 'max'
formatted = template % (name.title(), name.title())
print(formatted)

# % operator in Python has the ability to also do formatting with a
# dictionary instead of a tuple. %(key)
key = 'my_var'
value = 1.234

old_way = '%-10s = %.2f' % (key, value)
new_way = '%(key)-10s = %(value).2f' % {
    'key': key, 'value': value}  # Original
reordered = '%(key)-10s = %(value).2f' % {
    'value': value, 'key': key}  # Swapped
assert old_way == new_way == reordered

name = 'Max'
template = '%s loves food. See %s cook.'
before = template % (name, name)   # Tuple
template = '%(name)s loves food. See %(name)s cook.'
after = template % {'name': name}  # Dictionary
assert before == after

# Verbosity becomes a problem (soup var repeated 3 times)
soup = 'lentil'
formatted = 'Today\'s soup is %(soup)s.' % {'soup': soup}
print(formatted)

# format Built-in and str.format
# new options (, for thousands separators and ^ for centering)
a = 1234.5678
formatted = format(a, ',.2f')
print(formatted)
# 1,234.57
b = 'my string'
formatted = format(b, '^20s')
print('*', formatted, '*')
# *      my string       *

# can specify placeholders with {}.
# By default the placeholders in the format string are replaced
# by the corresponding positional arguments passed to the format
# method in the order in which they appear
key = 'my_var'
value = 1.234
formatted = '{} = {}'.format(key, value)
print(formatted)
# my_var = 1.234

# Within each placeholder you can optionally provide a colon character
# followed by format specifiers to customize how values will be converted
# into strings (see help('FORMATTING') for the full range of options)
formatted = '{:<10} = {:.2f}'.format(key, value)
print(formatted)
# my_var     = 1.23
# format specifiers will be passed to the format built-in function
# along with the value (format(value, '.2f') in the example above)

# The formatting behavior can be customized per class using the __format__ special method.

# With C-style format strings, you need to escape the % character (by doubling it)
# so it’s not interpreted as a placeholder accidentally. With the str.format method
# you need to similarly escape braces
print('%.2f%%' % 12.5)
print('{} replaces {{}}'.format(1.23))
# 12.50%
# 1.23 replaces {}

# Within the braces you may also specify the positional index of an argument
formatted = '{1} = {0}'.format(key, value)
print(formatted)
# 1.234 = my_var
formatted = '{0} loves food. See {0} cook.'.format(name)
print(formatted)
# Max loves food. See Max cook.

# advanced options for the specifiers used with the str.format method,
# such as using combinations of dictionary keys and list indexes in placeholders,
# and coercing values to Unicode and repr strings
menu = {
    'soup': 'lentil',
    'oyster': 'kumamoto',
    'special': 'schnitzel',
}
formatted = 'First letter is {menu[oyster][0]!r}'.format(menu=menu)
print(formatted)
# First letter is 'k'

new_template = (
    'Today\'s soup is {soup}, '
    'buy one get two {oyster} oysters, '
    'and our special entrée is {special}.')
new_formatted = new_template.format(
    soup='lentil',
    oyster='kumamoto',
    special='schnitzel',
)

# interpolated format strings

key = 'my_var'
value = 1.234
formatted = f'{key} = {value}'
print(formatted)
# my_var = 1.234

# All of the same options from the new format built-in mini language are
# available after the colon in the placeholders within an f-string, as is
# the ability to coerce values to Unicode and repr strings similar to the
# str.format method:
formatted = f'{key!r:<10} = {value:.2f}'
print(formatted)
# 'my_var'   = 1.23

# can split an f-string over multiple lines by relying on adjacent-string concatenation
formatted = (
    f'{key!r:<10} = '
    f'{value:.2f}'
)
print(formatted)

# Python expressions may also appear within the format specifier options.

places = 3
number = 1.23456
print(f'My number is {number:.{places}f}')
# My number is 1.235

# ✦ C-style format strings that use the % operator suffer from a variety of gotchas
# and verbosity problems.
# ✦ The str.format method introduces some useful concepts in its formatting specifiers
# mini language, but it otherwise repeats the mistakes of C-style format strings and
# should be avoided.
# ✦ F-strings are a new syntax for formatting values into strings that solves the biggest
# problems with C-style format strings.
# ✦ F-strings are succinct yet powerful because they allow for arbitrary Python
# expressions to be directly embedded within format specifiers.
