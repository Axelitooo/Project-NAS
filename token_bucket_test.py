# import token_bucket

import random
from storage import MemoryStorage  # NOQA
from storage_base import StorageBase  # NOQA
from token_bucket import TokenBucket  # NOQA

if __name__ == "__main__":
	keys = ['1', '2', '3', '4', '5']

	storage = MemoryStorage()
	tokenBucket = TokenBucket(10, 100, storage)

	time = 0
	for _ in range(1000):
		time += random.randint(1, 10)
		tokenBucket.consume(random.choice(keys), random.randint(1, 10), time)

