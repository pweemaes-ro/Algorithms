"""merge_sorted (returns a NEW sorted list)."""
from random import shuffle
from typing import Sequence

from common import SupportsLessThanT


def merged(left: Sequence[SupportsLessThanT],
           right: Sequence[SupportsLessThanT]) -> list[SupportsLessThanT]:
	"""Return a list created by merging left and right to one sequence. Assume
	left and right are sorted ascending."""
	
	_merged = []
	left_offset = right_offset = 0

	while left_offset < len(left) and right_offset < len(right):
		left_value = left[left_offset]
		right_value = right[right_offset]
		
		if left_value < right_value:
			_merged.append(left_value)
			left_offset += 1
		else:
			_merged.append(right_value)
			right_offset += 1
	
	_merged.extend(left[left_offset:])
	_merged.extend(right[right_offset:])
	
	return _merged


def merge_sorted(unsorted: list[SupportsLessThanT]) -> list[SupportsLessThanT]:
	"""Return a sorted list with all elements from *unsorted* Sequence."""
	
	if len(unsorted) <= 1:
		return unsorted

	mid_point = len(unsorted) // 2
	left = merge_sorted(unsorted[:mid_point])
	right = merge_sorted(unsorted[mid_point:])
	
	return merged(left, right)


if __name__ == "__main__":
	def main() -> None:
		"""Run some basic tests"""
		print("Testing...")
		for i in (-1, 0, 1, 2, 10, 11):
			lst = list(range(i))
			shuffle(lst)
			py_sorted_lst = sorted(lst)
			print("BEFORE")
			print(f"{lst              = }")
			print(f"{py_sorted_lst    = }")
			merge_sorted_lst = merge_sorted(lst)
			print("AFTER merge_sorted_lst = merge_sorted(lst) (NOT IN PLACE) ")
			print(f"{lst              = }")
			print(f"{py_sorted_lst    = }")
			print(f"{merge_sorted_lst = }")
			
			assert merge_sorted_lst == py_sorted_lst
			
			print("*" * 10)
	
	
	main()
