"""Functions that are (potentially) (re)used by multiple test routines."""


from random import choice, randrange, sample
from string import ascii_letters, digits, punctuation, whitespace
from typing import Any

from lists import flatten


syms = ascii_letters + digits + punctuation + whitespace


def create_random_string(length: int) -> str:
	"""Create and return a random string of given length. The string is build
	from chars in global var syms (see above)."""
	
	return ''.join(choice(syms) for _ in range(length))


def create_random_strings(nr_strings: int,
                          min_length: int = 0,
                          max_length: int = 100) -> tuple[str, ...]:
	"""Return a tuple of nr_strings strings, each with length between
	min_length and max_length (both inclusive)."""

	return tuple(create_random_string(randrange(min_length, max_length + 1))
	             for _ in range(nr_strings))


def test_create_random_strings() -> None:
	"""Test the test-support-function that creates random strings (Even the
	functions used in writing tests need testing ;-) """

	test_values = [(randrange(50), randrange(25), randrange(25))
	               for _ in range(10)] + [(0, 0, 0), (10, 10, 10)]
	for (nr_strings, min_size, max_size) in test_values:
		if min_size > max_size:
			min_size, max_size = max_size, min_size
		strings = create_random_strings(nr_strings, min_size, max_size)
		assert len(strings) == nr_strings
		for s in strings:
			assert min_size <= len(s) <= max_size


def generate_nested_collection(data: list[Any],
                               sublist_size: int,
                               nr_sublists: int,
                               max_per_container: int = 6) \
	-> list[Any]:
	"""Return a list containing nr_sublist lists, each containing at most
	max_per_container items. Possible items are: list or tuples (each with
	at most max_per_container (sub)items, or ints."""
	
	def _generate_collection(start: int, stop: int) \
		-> list[Any]:
		n = stop - start
		
		root: list[Any] = list()
		container: list[Any] = root
		
		nr_created = 0
		while nr_created < n:
			randrange_stop = min(n + 1 - nr_created, max_per_container)
			batch_size = randrange(randrange_stop)
			nesting_type = choice((list, tuple, int))
			
			if nesting_type is int:
				for i in range(batch_size):
					container.append(data[start + nr_created])
					nr_created += 1
			else:
				item_slice = data[start + nr_created:
				                  start + nr_created + batch_size]
				next_container = nesting_type(item_slice)
				container.append(next_container)
				nr_created += batch_size
				if nesting_type is list:
					container = next_container
		return root

	return [_generate_collection(sublist_size * i, sublist_size * (i + 1))
	        for i in range(nr_sublists)]
	

def create_random_dict(items_per_dict: int,
                       key_length: int,
                       value_range: int) -> dict[str, int]:
	"""Create and return a random dictionary with random strings of key_length
	chars as keys and random ints from range(value_range) as values."""
	
	return {create_random_string(key_length): randrange(value_range)
	        for _ in range(items_per_dict)}


def create_random_dicts(nr_dicts: int,
                        items_per_dict: int,
                        key_length: int,
                        value_range: int) \
	-> tuple[dict[str, int], ...]:
	"""Create and return a tuple of nr_dicts random dicts each with
	items_per_dict items, where each item has a random string of key_length
	chars as key, and a random int in range(value_range) as value."""
	
	return tuple(create_random_dict(items_per_dict, key_length, value_range)
	             for _ in range(nr_dicts))
	

def test_flatten() -> None:
	"""Test the flatten function."""
	
	sublist_size = 15
	nr_sublists = 4
	nr_items = sublist_size * nr_sublists
	sample_strings = create_random_strings(nr_strings=100,
	                                       max_length=15)
	sample_ints = tuple(range(100))
	sample_dicts = create_random_dicts(nr_dicts=5,
	                                   items_per_dict=5,
	                                   key_length=5,
	                                   value_range=10)
	
	all_samples = sample_ints + sample_strings + sample_dicts
	
	for i in range(1):
		data = sample(all_samples, nr_items)
		lst = generate_nested_collection(data,
		                                 sublist_size=sublist_size,
		                                 nr_sublists=nr_sublists)
		assert len(lst) <= len(data)
		print()
		print(lst)
		flattened_lst = flatten(lst)
		assert flattened_lst == data
		print(flattened_lst)
