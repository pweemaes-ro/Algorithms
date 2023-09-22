"""Tests for some special sort algorithms..."""
from special_algs import bit_array_sort


def test_special_sort() -> None:
	file_found = False
	
	# depending on starting location of tests, filename needs a different path
	filenames = ("_15k_ints.txt", "..\\tests\\sorting\\_15k_ints.txt")
	for _filename in filenames:
		if file_found:
			break
		try:
			with open(_filename):
				file_found = True
				filename = _filename
		except FileNotFoundError:
			pass
	
	assert filename
	
	nr_elements = 27000
	
	bit_array_sorted = list(bit_array_sort(0, nr_elements, filename))
	
	with open(filename) as f:
		python_sorted = sorted(int(i) for i in f)

	assert python_sorted == bit_array_sorted
