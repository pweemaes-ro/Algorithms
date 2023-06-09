"""Time a (sorting) function"""
import random
from dataclasses import dataclass
from operator import attrgetter
from random import shuffle
from timeit import repeat


def get_minimum_exec_time(setup_code: str, stmt: str) -> float:
	"""Execute the stetement and return the minimum execution time in seconds
	as a float."""
	
	return min(repeat(setup=setup_code, stmt=stmt, repeat=3, number=10))


def time_all() -> None:
	"""Run and report minimum execution times for all sorting algoriths."""
	
	sorting_algorithms = (("sorted", "", False),
	                      ("bubble_sort", "bubble_sort", True),
	                      ("insertion_sort", "insertion_sort", True),
	                      ("insertion_sort_recursive", "insertion_sort", True),
	                      ("merge_sort", "merge_sort", True),
	                      ("quicksort", "quicksort", False),
	                      ("quicksort_lomuto", "quicksort", True),
	                      ("quicksort_hoare", "quicksort", True),
	                      ("selection_sort", "selection_sort", True),
	                      ("tim_sort", "tim_sort", True),)
	i = 600
	lst = [random.randint(-i, i) for _ in range(i)]
	shuffle(lst)
	print(f"Sorting a list of {i} random (unsorted) integers in interval [{-i},"
	      f" {i}].")
	print(f"NO key, NO reverse.")
	
	@dataclass
	class TimingResults:
		"""Store results per function, so we can sort before displaying!"""
		seconds: float
		function_name: str
		
	results: list[TimingResults] = []
	for sorting_algorithm, import_file, is_in_place in sorting_algorithms:
		unsorted = list(lst)
		setup = ""
		if import_file:
			setup = f"from {import_file} import {sorting_algorithm}"
		stmt = f"result = {sorting_algorithm}({unsorted})"
		seconds = get_minimum_exec_time(setup, stmt)
		results.append(TimingResults(seconds=seconds,
		                             function_name=sorting_algorithm))

	results = sorted(results, key=attrgetter('seconds'))
	for result in results:
		print(f"{result.function_name:24s}: "
		      f"{result.seconds:.5f}")


time_all()
