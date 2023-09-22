"""Test BloomFilter and CountingBloomFilter classes."""
from random import choice

from _common_funcs import create_random_strings
from bloomfilter import BloomFilter, CountingBloomFilter


def test_bloom_filter() -> None:

	nr_strings = 2000
	bf = BloomFilter(10 ** -10, nr_strings)
	strings = create_random_strings(nr_strings, min_length=100)
	add_count = 0
	for i, s in enumerate(strings):
		if choice((True, False)):
			bf.add(s)
			add_count += 1
			assert bf.query(s)
		else:
			assert not bf.query(s)

	print(f"_test_bloom_filter: "
	      f"added {add_count} strings, "
	      f"querying added strings: all found, "
	      f"querying {nr_strings - add_count} other strings: none found: OK.")


def test_counting_bloom_filter() -> None:

	nr_strings = 2000
	bf = CountingBloomFilter(10 ** -10, nr_strings, 'B')
	strings = create_random_strings(nr_strings, min_length=100)
	add_count = 0
	for i, s in enumerate(strings):
		if choice((True, False)):
			bf.add(s)
			add_count += 1
			assert bf.query(s)
			assert bf.delete(s)
			assert not bf.query(s)
		else:
			assert not bf.query(s)

	# print(f"_test_bloom_filter: "
	#       f"added {add_count} strings, "
	#       f"queryed added strings: all found, "
	#       f"deleted added strings: all deleted, queried deleted: none found, "
	#       f"querying {nr_strings - add_count} other strings: none found: OK.")
