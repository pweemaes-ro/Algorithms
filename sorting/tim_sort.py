"""Timsort is used internally for sorting in Python."""
from collections.abc import MutableSequence
from random import randint
from typing import Optional, Callable, Any

from common import SupportsLessThanT
from insertion_sort import insertion_sort
from merge_sort import merge


def tim_sort(sequence: MutableSequence[SupportsLessThanT],
             key: Optional[Callable[..., Any]] = None,
             reverse: bool = False) -> None:
	"""Split the sequence in segments of 32 (or 64?) bytes, sort these with
	insertion_sort (which is fast for such small segments), then merge with the
	same merge as used in merge_sort."""

	sequence_size = len(sequence)
	segment_size = 16

	for start in range(0, sequence_size, segment_size):
		insertion_sort(sequence,
		               start,
		               min(start + segment_size, sequence_size),
		               key,
		               reverse=reverse)

	while segment_size <= sequence_size:
		for start in range(0, sequence_size, segment_size * 2):
			merge(sequence,
			      start,
			      start + segment_size,
			      min(start + 2 * segment_size, sequence_size),
			      key,
			      reverse)
		segment_size *= 2


def test_tim_sort() -> None:

	def mod_3(n: int) -> int:
		"""Just a test key function """
		
		return n % 3
	
	for i in range(500):
		base_lst = [randint(-i, i) for _ in range(i)]
		for key in (None, abs, mod_3):
			for reverse in (False, True):
				lst = list(base_lst)
				tim_sort(lst, key=key, reverse=reverse)
				assert lst == sorted(list(base_lst), key=key, reverse=reverse)


if __name__ == "__main__":
 
	def _main() -> None:
		test_tim_sort()
	
	_main()
