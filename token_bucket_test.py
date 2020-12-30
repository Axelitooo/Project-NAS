# import token_bucket

import random
import time
from storage import MemoryStorage  # NOQA
from storage_base import StorageBase  # NOQA
from token_bucket import TokenBucket  # NOQA

if __name__ == "__main__":
	keys = ['1', '2', '3', '4', '5']

	storage = MemoryStorage()
	tokenBucket = TokenBucket(10, 100, storage)

	for i in range(1000):
		time.sleep(random.randint(1, 10) / 1000)
		consumed_key = random.choice(keys)
		tokenBucket.consume(consumed_key, time.time(), random.randint(1, 10))
		if i % 100 == 0:
			print(time.time())
			for key in keys:
				print(key, tokenBucket._storage.get_token_count(key))

