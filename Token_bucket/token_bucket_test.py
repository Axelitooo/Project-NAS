from .token_bucket import TokenBucket

if __name__ == "__main__":
	keys = ['1', '2', '3', '4', '5']

	storage = token_bucket.MemoryStorage()
	tokenBucket = token_bucket.TokenBucket(10, 100, storage)

	time = 0
	for _ in range(1000):
		time += randomInt(0, 10)
		tokenBucket.consume(randomChoice(keys), randomInt(0, 10), time)

