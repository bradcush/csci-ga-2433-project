import hashlib
import time


# Create time-based hash for now but
# better could be to hash the contents
def hash_time():
    now = str(time.time()).encode()
    m = hashlib.sha1()
    m.update(now)
    return m.hexdigest()
