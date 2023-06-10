"""In place merge sort based on 'Introduction to Algorithms'. """
from collections.abc import MutableSequence, Callable
from operator import lt, gt
from typing import Optional

from common import SupportsLessThanT


def _merge(sequence: MutableSequence[SupportsLessThanT],
           start: int,
           middle: int,
           stop: int,
           keys: MutableSequence[SupportsLessThanT],
           reverse: bool = False) -> int:
	"""In place merge based on 'Introduction to Algorithms' Returns the nr of
	inversions detected."""

	left = start
	right = middle

	if reverse:
		compare_operator = gt
	else:
		compare_operator = lt
	
	_sorted, _sorted_keys = [], []
	inversions = 0
	
	while left < middle and right < stop:
		if compare_operator(keys[right], keys[left]):
			inversions += middle - left
			append_offset = right
			right += 1
		else:
			append_offset = left
			left += 1
		
		_sorted.append(sequence[append_offset])
		if keys is not sequence:
			_sorted_keys.append(keys[append_offset])

	_sorted.extend(sequence[left:middle])
	_sorted.extend(sequence[right:stop])
	sequence[start:stop] = _sorted
	
	if keys is not sequence:
		_sorted_keys.extend(keys[left:middle])
		_sorted_keys.extend(keys[right:stop])
		keys[start:stop] = _sorted_keys
	
	return inversions


def _merge_sort(sequence: MutableSequence[SupportsLessThanT],
                start: int,
                stop: int,
                keys: MutableSequence[SupportsLessThanT],
                reverse: bool) -> int:
	
	inversions = 0
	
	if stop - start <= 1:
		return 0
	
	middle = (stop + start) // 2
	
	inversions += _merge_sort(sequence, start, middle, keys, reverse)
	inversions += _merge_sort(sequence, middle, stop, keys, reverse)
	
	inversions += _merge(sequence, start, middle, stop, keys, reverse)
	
	return inversions


def merge_sort(sequence: list[SupportsLessThanT],
               key: Optional[Callable[[SupportsLessThanT],
                             SupportsLessThanT]] = None,
               reverse: bool = False) -> int:
	"""The IN PLACE merge sort based upon 'Introduction to Algorithms'. THIS
	algorithm now returns the nr of inversions in the sequence."""

	if key:
		keys = [*map(key, sequence)]
	else:
		keys = sequence
		
	return _merge_sort(sequence, 0, len(sequence), keys, reverse=reverse)
