from slowapi import Limiter
from slowapi.util import get_remote_address
import time

limiter = Limiter(
    key_func=get_remote_address
)

start = time.time()

end = time.time()

print(end-start)