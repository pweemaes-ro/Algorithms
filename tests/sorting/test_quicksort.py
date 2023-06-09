"""Test(s) for all quicksort variants (quicksort, quicksort_hoare and
quicksort_lomuto."""

from random import randint

from quicksort import quicksort, quicksort_hoare, quicksort_lomuto
from tools import is_sorted


def test_quicksort_in_place_versions() -> None:
	
	def mod_3(n: int) -> int:
		"""Just a test key function """
		
		return n % 3
	
	keys = (None, abs, mod_3)
	
	for i in range(250):
		base_lst = [randint(-i, i) for _ in range(i)]
		
		for qs_in_place_func in (quicksort_hoare, quicksort_lomuto):
			# stable_info[qs_in_place_func] = True
			for reverse in (False, True):
				for key in keys:
					print(f"{qs_in_place_func.__name__}, {reverse=}, {key=}")
					lst = list(base_lst)
					qs_in_place_func(lst, key=key, reverse=reverse)
					# quicksort_hoare and quicksort_lomuto are NOT stable sorts.
					assert is_sorted(lst, key=key, reverse=reverse), \
						f"{base_lst = }, {qs_in_place_func.__name__}"


def test_quicksort_not_in_place_versions() -> None:
	
	def mod_3(n: int) -> int:
		"""Just a test key function """
		
		return n % 3
	
	keys = (None, abs, mod_3)
	
	for i in range(250):
		base_lst = [randint(-i, i) for _ in range(i)]
	
		for qs_not_in_place_func in (quicksort,):
			for reverse in (False, True):
				for key in keys:
					# quicksort is stable sorts.
					assert qs_not_in_place_func(list(base_lst),
					                            key=key,
					                            reverse=reverse) == \
					       sorted(base_lst, key=key, reverse=reverse)


# def test_quicksort() -> None:
# 	"""Test all quicksort variants (in place and not in place)."""
#
# 	def mod_3(n: int) -> int:
# 		"""Just a test key function """
#
# 		return n % 3
#
# 	keys = (None, abs, mod_3)
#
# 	_test_quicksort_in_place_versions(keys)
# 	_test_quicksort_not_in_place_versions(keys)
# 	# for i in range(250):
# 	# 	base_lst = [randint(-i, i) for _ in range(i)]
# 	#
# 	# 	for qs_in_place_func in (quicksort_hoare, quicksort_lomuto):
# 	# 		# stable_info[qs_in_place_func] = True
# 	# 		for reverse in (False, True):
# 	# 			for key in keys:
# 	# 				lst = list(base_lst)
# 	# 				qs_in_place_func(lst, key=key, reverse=reverse)
# 	# 				# quicksort_hoare and quicksort_lomuto are NOT stable sorts.
# 	# 				assert is_sorted(lst, key=key, reverse=reverse)
# 	#
# 	# 	for qs_not_in_place_func in (quicksort,):
# 	# 		# stable_info[qs_not_in_place_func] = True
# 	# 		for reverse in (False, True):
# 	# 			for key in keys:
# 	# 				# quicksort is stable sorts.
# 	# 				assert qs_not_in_place_func(list(base_lst),
# 	# 				                            key=key,
# 	# 				                            reverse=reverse) == \
# 	# 				       sorted(base_lst, key=key, reverse=reverse)
