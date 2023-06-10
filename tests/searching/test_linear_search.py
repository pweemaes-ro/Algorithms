"""Test(s) for linear_search."""

from linear_search import linear_search


def test_linear_search() -> None:
	"""Test binary_search function."""
	
	for i in range(100):
		data = list(range(i))
		for target in data:
			assert linear_search(data, target) == target
		
		assert linear_search([], 1) is None
		assert linear_search([], 0) is None
		
		not_in_data = (-1, i)
		for target in not_in_data:
			assert linear_search(data, target) is None
