"""In place merge sort based on 'Introduction to Algorithms'. """
from collections.abc import MutableSequence, Callable
from operator import lt, gt
from typing import Optional, Any

from common import SupportsLessThanT


def merge(sequence: MutableSequence[SupportsLessThanT],
          start: int,
          middle: int,
          stop: int,
          keys: MutableSequence[SupportsLessThanT],
          reverse: bool = False) -> int:
	"""In place merge based on 'Introduction to Algorithms' Returns the nr of
	inversions detected."""

	# Instead of directly copying data to sequence (see merge_ita) we create a
	# new sorted list, which we put in the unsorted sequence when all data is
	# in sorted list.

	left = start
	right = middle

	if reverse:
		operator = gt
	else:
		operator = lt
	
	_sorted, _sorted_keys = [], []
	inversions = 0
	
	while left < middle and right < stop:
		if operator(keys[right], keys[left]):
			inversions += middle - left
			_sorted.append(sequence[right])
			# We could test here: if keys is not sequence
			_sorted_keys.append(keys[right])
			right += 1
		else:
			_sorted.append(sequence[left])
			# We could test here: if keys is not sequence
			_sorted_keys.append(keys[left])
			left += 1

	if middle > left:
		_sorted.extend(sequence[left:middle])
		# We could test here: if keys is not sequence
		_sorted_keys.extend(keys[left:middle])
	if stop > right:
		_sorted.extend(sequence[right:stop])
		# We could test here: if keys is not sequence
		_sorted_keys.extend(keys[right:stop])

	sequence[start:stop] = _sorted
	# We could test here: if keys is not sequence
	keys[start:stop] = _sorted_keys

	return inversions


# def merge(sequence: MutableSequence[SupportsLessThanT],
#           start: int,
#           middle: int,
#           stop: int,
#           key: Optional[Callable[..., Any]] = None,
#           reverse: bool = False) -> int:
# 	"""In place merge based on 'Introduction to Algorithms' Returns the nr of
# 	inversions detected."""
#
# 	# Instead of directly copying data to sequence (see merge_ita) we create a
# 	# new sorted list, which we put in the unsorted sequence when all data is
# 	# in sorted list.
#
# 	left = start
# 	right = middle
#
# 	if reverse:
# 		operator = gt
# 	else:
# 		operator = lt
#
# 	key = key or identity_key
#
# 	_sorted = []
# 	inversions = 0
#
# 	while left < middle and right < stop:
# 		if operator(key(sequence[right]), key(sequence[left])):
# 			inversions += middle - left
# 			_sorted.append(sequence[right])
# 			right += 1
# 		else:
# 			_sorted.append(sequence[left])
# 			left += 1
#
# 	_sorted.extend(sequence[left:middle])
# 	_sorted.extend(sequence[right:stop])
#
# 	sequence[start:stop] = _sorted
#
# 	return inversions
#
#
def _merge_sort(sequence: MutableSequence[SupportsLessThanT],
                start: int,
                stop: int,
                keys: MutableSequence[SupportsLessThanT],
                reverse: bool) -> int:
	
	inversions = 0
	
	if stop is None:
		stop = len(sequence)
	
	if stop - start <= 1:
		return 0
	
	middle = (stop + start) // 2
	
	inversions += _merge_sort(sequence, start, middle, keys, reverse)
	inversions += _merge_sort(sequence, middle, stop, keys, reverse)
	
	inversions += merge(sequence, start, middle, stop, keys, reverse)
	
	return inversions


def merge_sort(sequence: MutableSequence[SupportsLessThanT],
               key: Optional[Callable[..., Any]] = None,
               reverse: bool = False) -> int:
	"""The IN PLACE merge sort based upon 'Introduction to Algorithms'. THIS
	algorithm now returns the nr of inversions in the sequence."""

	keys: MutableSequence[SupportsLessThanT]

	if key:
		keys = [*map(key, sequence)]
	else:
		keys = sequence
		
	return _merge_sort(sequence,
	                   0,
	                   len(sequence),
	                   keys,
	                   reverse=reverse)
