"""merge_sort function (in place sort)."""
from random import shuffle
from sorting.merge_sort import merge_sorted
from common import SupportsLessThanT


def merge_sort_in_place(unsorted: list[SupportsLessThanT]) -> None:
	"""Merge sorts the data in *sequence* in place."""

	_sorted = merge_sorted(unsorted)
	for i, data in enumerate(_sorted):
		unsorted[i] = data


if __name__ == "__main__":
	def main() -> None:
		"""Run some basic tests"""
		print("Testing...")
		for i in (-1, 0, 1, 2, 3, 4, 10, 11):
			lst = list(range(i))
			shuffle(lst)
			py_sorted_lst = sorted(lst)
			if len(lst) > 1:
				while lst == py_sorted_lst:
					shuffle(lst)
			
			print("BEFORE")
			print(f"{lst            = }")
			print(f"{py_sorted_lst  = }")

			merge_sort_in_place(lst)
			print("AFTER merge_sort(lst) (IN PLACE) ")
			print(f"{lst            = }")
			print(f"{py_sorted_lst  = }")
			assert lst == py_sorted_lst

			print("*" * 10)
	
	main()
