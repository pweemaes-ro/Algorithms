"""Test of miscellaneous math funcs."""
from itertools import pairwise
from random import randint, choice

# noinspection PyProtectedMember
from miscellaneous import get_summing_pairs, _naive_sum_finder, has_summing_pair


def test_get_summing_pairs() -> None:
	"""Some basic tests..."""
	
	for i in range(500):
		set_of_ints = set((randint(-i, i) for _ in range(i)))
		target_sum = i // 2 * choice([-1, 1])
		sorted_pairs = sorted(get_summing_pairs(set_of_ints, target_sum))
		sorted_naive_pairs = \
			sorted(_naive_sum_finder(set_of_ints, target_sum))
		assert sorted_pairs == sorted_naive_pairs


def test_has_summing_pairs():
	test_sets = (set(), {randint(-10, 10) for _ in range(10)})
	for test_set in test_sets:
		assert not has_summing_pair(test_set, 100)
		for a, b in pairwise(test_set):
			s = set(test_set)
			c = a + b
			# a = c + (-b)
			# b = c + (-a)
			s.add(-a)
			s.add(-b)
			assert has_summing_pair(s, c)
			assert has_summing_pair(s, a)
			assert has_summing_pair(s, b)


if __name__ == "__main__":
	test_get_summing_pairs()
	test_has_summing_pairs()
