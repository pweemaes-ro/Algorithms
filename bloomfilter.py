"""A simple bloomfilter class implementation."""
from array import array
from math import log
from hashlib import sha256
from typing import Hashable

from bitarray import BitArray


class BloomFilter:
	"""A simple bloom filter."""
	
	hash_func = sha256
	
	def __init__(self, false_positive_rate: float, nr_items: int):
		self.__false_positive_rate = false_positive_rate
		self.__nr_items = nr_items
		self._size = self.__optimal_size()
		self._nr_hash = self.__optimal_nr_of_hash()
		self._bit_array = BitArray(self._size)

	def __optimal_size(self) -> int:
		"""Return the optimal size (in bits) of the filter given an acceptable
		false positive rate and the (expected) nr of items to store."""
		return int(-(self.__nr_items * log(self.__false_positive_rate)) /
		           (log(2) ** 2))
	
	def __optimal_nr_of_hash(self) -> int:
		return int(self.__optimal_size() * log(2) / self.__nr_items)
	
	def __str__(self) -> str:
		return (f"fpr     = {self.__false_positive_rate},\n"
		        f"nr_hash = {self.__optimal_nr_of_hash()},\n"
		        f"bytes   = {(self.__optimal_size() + 7) // 8}")
	
	def _hash(self, item: str) -> int:
		return (int(BloomFilter.hash_func(item.encode("utf-8")).hexdigest(), 16)
		        % self._size)
		
	def add(self, item: Hashable) -> None:
		"""'Adds' an item to the filter."""
		
		for i in range(self._nr_hash):
			self._bit_array[self._hash(str((item, i)))] = True
	
	def query(self, item: Hashable) -> bool:
		"""Return True if item 'found', else False. Note that False means that
		the item is 100% certain not in the filter, but True means there's a 1
		in self.__false_positive_rate probability that the item is NOT in the
		filter!"""
		
		for i in range(self._nr_hash):
			if not self._bit_array[self._hash(str((item, i)))]:
				return False
		return True


class CountingBloomFilter(BloomFilter):
	"""A simple counting bloom filter (which allows for deleting items)."""

	def __init__(self, false_positive_rate: float, nr_items: int,
	             counter_type: str):
		super().__init__(false_positive_rate, nr_items)
		self.__counters = array(counter_type, (0 for _ in range(self._size)))
	
	def decrement_counter(self, bit_offset: int) -> int:
		"""Decrement the counter at bit_offset, return new counter value."""
		
		new_counter = self.__counters[bit_offset] - 1
		self.__counters[bit_offset] = new_counter
		return new_counter
	
	def increment_counter(self, bit_offset: int) -> int:
		"""Increment the counter at bit_offset, return new counter value."""

		new_counter = self.__counters[bit_offset] + 1
		self.__counters[bit_offset] = new_counter
		return new_counter
	
	def add(self, item: Hashable) -> None:
		"""'Adds' an item to the filter."""
		
		for i in range(self._nr_hash):
			bit_offset = self._hash(str((item, i)))
			if self.increment_counter(bit_offset) == 1:
				self._bit_array[bit_offset] = True

	def query(self, item: Hashable) -> bool:
		"""Return True if item 'found', else False. Note that False means that
		the item is 100% certain not in the filter, but True means there's a 1
		in self.__false_positive_rate probability that the item is NOT in the
		filter!"""

		for i in range(self._nr_hash):
			if not self.__counters[self._hash(str((item, i)))]:
				return False
		return True

	def delete(self, item: Hashable) -> bool:
		"""Return True if item is in the filter and was deleted, or False if
		item not in the filter (and therefore not deleted)."""
		
		if self.query(item):
			for i in range(self._nr_hash):
				bit_offset = self._hash(str((item, i)))
				if self.decrement_counter(bit_offset) == 0:
					self._bit_array[bit_offset] = False
			return True
		
		return False


# if __name__ == "__main__":
# 	from random import choice
# 	from tests._common_funcs import create_random_strings
#
# 	def _test_bloom_filter() -> None:
#
# 		nr_strings = 2000
# 		bf = BloomFilter(10 ** -10, nr_strings)
# 		strings = create_random_strings(nr_strings, min_length=100)
# 		add_count = 0
# 		for i, s in enumerate(strings):
# 			if choice((True, False)):
# 				bf.add(s)
# 				add_count += 1
# 				assert bf.query(s)
# 			else:
# 				assert not bf.query(s)
#
# 		print(f"_test_bloom_filter: "
# 		      f"added {add_count} strings, "
# 		      f"querying added strings: all found, "
# 		      f"querying {nr_strings - add_count} other strings: none found: OK.")
#
# 	def _test_counting_bloom_filter() -> None:
#
# 		nr_strings = 2000
# 		bf = CountingBloomFilter(10 ** -10, nr_strings, 'B')
# 		strings = create_random_strings(nr_strings, min_length=100)
# 		add_count = 0
# 		for i, s in enumerate(strings):
# 			if choice((True, False)):
# 				bf.add(s)
# 				add_count += 1
# 				assert bf.query(s)
# 				assert bf.delete(s)
# 				assert not bf.query(s)
# 			else:
# 				assert not bf.query(s)
#
# 		print(f"_test_bloom_filter: "
# 		      f"added {add_count} strings, "
# 		      f"queryed added strings: all found, "
# 		      f"deleted added strings: all deleted, queried deleted: none found, "
# 		      f"querying {nr_strings - add_count} other strings: none found: OK.")
#
# 	_test_bloom_filter()
# 	_test_counting_bloom_filter()
