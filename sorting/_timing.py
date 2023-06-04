"""Time a (sorting) function"""
import random
from random import shuffle
from timeit import repeat


def get_minimum_exec_time(setup_code: str, stmt: str) -> float:
	"""Execute the stetement and return the minimum execution time."""
	
	return min(repeat(setup=setup_code, stmt=stmt, repeat=3, number=10))


def time_all() -> None:
	"""Run and report minimum execution times for all sorting algoriths."""
	
	sorting_algorithms = (("quicksort", "quicksort", False),
	                      ("quicksort_lomuto", "quicksort", True),
	                      ("quicksort_hoare", "quicksort", True),
	                      ("merge_sort", "merge_sort", True),
	                      ("insertion_sort", "insertion_sort", True),
	                      ("bubble_sort", "bubble_sort", True),
	                      ("selection_sort", "selection_sort", True),
	                      ("tim_sort", "tim_sort", True))
	i = 2000
	lst = [random.randint(-i, i) for _ in range(i)]
	shuffle(lst)
	
	for sorting_algorithm, import_file, is_in_place in sorting_algorithms:
		unsorted = list(lst)
		setup = f"from {import_file} import {sorting_algorithm}"
		stmt = f"result = {sorting_algorithm}({unsorted})"
		print(f"{sorting_algorithm:20s}: {get_minimum_exec_time(setup, stmt):.5f}")


time_all()

# lst = list(range(1000))
# sorted_lst = list(range(1000))
# shuffle(lst)
# print(lst)
# print(quicksort_lomuto(lst))
# print(lst)
