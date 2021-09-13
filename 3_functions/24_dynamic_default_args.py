# Item 24: Use None and Docstrings to Specify Dynamic Default Arguments

from time import sleep
from datetime import datetime

def log(message, when=datetime.now()):
    print(f'{when}: {message}')
log('Hi there!')
sleep(0.1)
log('Hello again!')
# 2019-07-06 14:06:15.120124: Hi there!
# 2019-07-06 14:06:15.120124: Hello again!

# The timestamps are the same because datetime.now is executed only a single time:
# when the function is defined. A default argument value is evaluated only once per
# module load, which usually happens when a program starts up. After the module
# containing this code is loaded, the datetime.now() default argument will never
# be evaluated again.

# The convention for achieving the desired result in Python is to provide a default
# value of None and to document the actual behavior in the docstring. When your code
# sees the argument value None, you allocate the default value accordingly
def log(message, when=None):
    """Log a message with a timestamp.

    Args:
        message: Message to print.
        when: datetime of when the message occurred.
            Defaults to the present time.
    """
    if when is None:
        when = datetime.now()
    print(f'{when}: {message}')
# Now the timestamps will be different:
log('Hi there!')
sleep(0.1)
log('Hello again!')
# 2019-07-06 14:06:15.222419: Hi there!
# 2019-07-06 14:06:15.322555: Hello again!

# Using None for default argument values is especially important when the
# arguments are mutable.
import json
def decode(data, default={}):
    try:
        return json.loads(data)
    except ValueError:
        return default
# The dictionary specified for default will be shared by all calls to
# decode because default argument values are evaluated only once
# (at module load time).
foo = decode('bad data')
foo['stuff'] = 5
bar = decode('also bad')
bar['meep'] = 1
print('Foo:', foo)
print('Bar:', bar)
# Foo: {'stuff': 5, 'meep': 1}
# Bar: {'stuff': 5, 'meep': 1}

# Modifying one seems to also modify the other. The culprit is that foo and
# bar are both equal to the default parameter. They are the same dictionary object:
assert foo is bar

# The fix is to set the keyword argument default value to None and then
# document the behavior in the function’s docstring:
def decode(data, default=None):
    """Load JSON data from a string.

    Args:
        data: JSON data to decode.
        default: Value to return if decoding fails.
            Defaults to an empty dictionary.
    """
    try:
        return json.loads(data)
    except ValueError:
        if default is None:
            default = {}
        return default

foo = decode('bad data')
foo['stuff'] = 5
bar = decode('also bad')
bar['meep'] = 1
print('Foo:', foo)
print('Bar:', bar)
assert foo is not bar
# Foo: {'stuff': 5}
# Bar: {'meep': 1}

# This approach also works with type annotations
from typing import Optional
def log_typed(message: str,
              when: Optional[datetime]=None) -> None:
    """Log a message with a timestamp.

    Args:
        message: Message to print.
        when: datetime of when the message occurred.
            Defaults to the present time.
    """
    if when is None:
        when = datetime.now()
    print(f'{when}: {message}')

# ✦ A default argument value is evaluated only once: during function definition
# at module load time. This can cause odd behaviors for dynamic values
# (like {}, [], or datetime.now()).
# ✦ Use None as the default value for any keyword argument that has a dynamic value.
# Document the actual default behavior in the function’s docstring.
# ✦ Using None to represent keyword argument default values also works correctly
# with type annotations.
