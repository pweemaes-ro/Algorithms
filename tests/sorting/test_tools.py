"""Tests for tools functions (is_sorted, inversion_count)."""
from random import randint

# noinspection PyProtectedMember
from tools import _naive_inversion_count, inversion_count, is_sorted


def test_is_sorted() -> None:
	"""Test is_sorted function (with keys and reverse)."""
	
	def mod_3(n: int) -> int:
		"""Just a test key function """
		
		return n % 3
	
	for i in range(100):
		for reverse in (False, True):
			for key in (None, abs, mod_3):
				base_list = [randint(-i, i) for _ in range(i)]
				sorted_list = sorted(base_list, key=key, reverse=reverse)
				assert is_sorted(sorted_list, key=key, reverse=reverse)


def test_inversion_count() -> None:
	"""Test inversion count by comparing results with those of a naive count."""
	
	for i in range(100):
		for reverse in (False, True):
			lst = [randint(-i, i) for _ in range(i)]
			naive_count = _naive_inversion_count(lst, reverse)
			normal_count = inversion_count(lst, reverse)
			assert naive_count == normal_count
