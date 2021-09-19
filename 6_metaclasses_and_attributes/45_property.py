# Item 45: Consider @property Instead of Refactoring Attributes

# One advanced but
# common use of @property is transitioning what was once a simple
# numerical attribute into an on-the-fly calculation.

from datetime import datetime, timedelta
class Bucket:
    def __init__(self, period):
        self.period_delta = timedelta(seconds=period)
        self.reset_time = datetime.now()
        self.quota = 0
    def __repr__(self):
        return f'Bucket(quota={self.quota})'

def fill(bucket, amount):
    now = datetime.now()
    if (now - bucket.reset_time) > bucket.period_delta:
        bucket.quota = 0
        bucket.reset_time = now
    bucket.quota += amount
def deduct(bucket, amount):
    now = datetime.now()
    if (now - bucket.reset_time) > bucket.period_delta:
        return False # Bucket hasn't been filled this period
    if bucket.quota - amount < 0:
        return False # Bucket was filled, but not enough
    bucket.quota -= amount
    return True # Bucket had enough, quota consumed

bucket = Bucket(60)
fill(bucket, 100)
print(bucket)
# Bucket(quota=100)

if deduct(bucket, 99):
    print('Had 99 quota')
else:
    print('Not enough for 99 quota')
print(bucket)
# Had 99 quota
# Bucket(quota=1)

if deduct(bucket, 3):
    print('Had 3 quota')
else:
    print('Not enough for 3 quota')
print(bucket)
# Not enough for 3 quota
# Bucket(quota=1)

# I never know what quota level the bucket started with. Fixing:
class NewBucket:
    def __init__(self, period):
        self.period_delta = timedelta(seconds=period)
        self.reset_time = datetime.now()
        self.max_quota = 0
        self.quota_consumed = 0
    def __repr__(self):
        return (f'NewBucket(max_quota={self.max_quota}, '
                f'quota_consumed={self.quota_consumed})')
    @property
    def quota(self):
        return self.max_quota - self.quota_consumed
    @quota.setter
    def quota(self, amount):
        delta = self.max_quota - amount
        if amount == 0:
            # Quota being reset for a new period
            self.quota_consumed = 0
            self.max_quota = 0
        elif delta < 0:
            # Quota being filled for the new period
            assert self.quota_consumed == 0
            self.max_quota = amount
        else:
            # Quota being consumed during the period
            assert self.max_quota >= self.quota_consumed
            self.quota_consumed += delta
bucket = NewBucket(60)
print('Initial', bucket)
fill(bucket, 100)
print('Filled', bucket)
if deduct(bucket, 99):
    print('Had 99 quota')
else:
    print('Not enough for 99 quota')
print('Now', bucket)
if deduct(bucket, 3):
    print('Had 3 quota')
else:
    print('Not enough for 3 quota')
print('Still', bucket)
# Initial NewBucket(max_quota=0, quota_consumed=0)
# Filled NewBucket(max_quota=100, quota_consumed=0)
# Had 99 quota
# Now NewBucket(max_quota=100, quota_consumed=99)
# Not enough for 3 quota
# Still NewBucket(max_quota=100, quota_consumed=99)

# The best part is that the code using Bucket.quota doesn’t have to
# change or know that the class has changed. New usage of Bucket can
# do the right thing and access max_quota and quota_consumed directly.

# ✦ Use @property to give existing instance attributes new functionality.
# ✦ Make incremental progress toward better data models by using
# @property.
# ✦ Consider refactoring a class and all call sites when you find yourself
# using @property too heavily.
