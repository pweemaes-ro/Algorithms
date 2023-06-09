"""Some stuff I cannot dump anywhere else..."""
from collections.abc import Sequence
from random import randint, choice


def has_summing_pair(integers: set[int], target_sum: int) -> bool:
	"""Return boolean indiacting whether a pair (a, b) of integers exist in the
	integers argument that sum up to target_sum."""
	
	return bool(_summing_pairs(integers, target_sum, is_existence_check=True))


def get_summing_pairs(integers: set[int], target_sum: int) \
	-> set[tuple[int, int]]:
	"""Return a set of all tuples(a, b) with a < b from the integers argument
	s.t. a + b = target_sum."""
	
	return _summing_pairs(integers, target_sum)


def _summing_pairs(integers: set[int],
                   target_sum: int,
                   is_existence_check: bool = False) \
	-> set[tuple[int, int]]:
	"""If is_existence_check == False: return a set of ALL tuples(a, b) with
	a < b from the integers argument s.t. a + b = target_sum. If
	is_existence_check == True: Return a set with the FIRST FOUND such pair.
	Set membership testing and adding are both constant time O(1), due to the
	fact that sets in Python are basically dictionaries with keys but no values
	(this means that a set can only hold immutable objects!). Therefore
	this function is O(n)."""
	
	pairs = set()
	
	for integer in integers:
		complement = target_sum - integer
		if (complement != integer) and \
		   (complement in integers) and \
		   ((complement, integer) not in pairs):
			pairs.add((integer, complement))
			if is_existence_check:
				break

	return pairs


def _naive_sum_finder(integers: Sequence[int], target_sum: int) \
	-> set[tuple[int, int]]:
	"""Naive and slow algorithm (just here for testing purposes). Return a set
	of all tuples(a, b) from integers s.t. a + b = target_sum and also a < b
	(so if (a, b) is in the set, then for (b, a) also a + b = target_sum, but
	(b, a) is NOT in the set."""

	pairs = set()

	for i in range(len(integers)):
		complement = target_sum - integers[i]
		for j in range(i+1, len(integers)):
			if integers[j] == complement:
				pairs.add((integers[i], integers[j]))
	
	return pairs


def test_find_summing_pairs() -> None:
	"""Some basic tests..."""
	
	for i in range(500):
		set_of_ints = set((randint(-i, i) for _ in range(i)))
		target_sum = i // 2 * choice([-1, 1])
		sorted_pairs = \
			sorted(get_summing_pairs(set_of_ints, target_sum))
		sorted_naive_pairs = \
			sorted(_naive_sum_finder(list(set_of_ints), target_sum))
		assert sorted_pairs == sorted_naive_pairs


if __name__ == "__main__":
	test_find_summing_pairs()
