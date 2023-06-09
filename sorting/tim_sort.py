"""Timsort is used internally for sorting in Python."""
from collections.abc import MutableSequence
from typing import Optional, Callable

from common import SupportsLessThanT
from insertion_sort import _insertion_sort
from merge_sort import _merge


def tim_sort(sequence: MutableSequence[SupportsLessThanT],
             key: Optional[Callable[[SupportsLessThanT],
                           SupportsLessThanT]] = None,
             reverse: bool = False) -> None:
	"""Split the sequence in segments of 32 (or 64?) bytes, sort these with
	insertion_sort (which is fast for such small segments), then merge with the
	same merge as used in merge_sort."""

	if key:
		keys: MutableSequence[SupportsLessThanT] = [*map(key, sequence)]
	else:
		keys = sequence
	
	sequence_size = len(sequence)
	segment_size = 16
	
	for start in range(0, sequence_size, segment_size):
		_insertion_sort(sequence,
		               start,
		               min(start + segment_size, sequence_size),
		               keys,
		               reverse=reverse)

	while segment_size <= sequence_size:
		for start in range(0, sequence_size, segment_size * 2):
			_merge(sequence,
			      start,
			      start + segment_size,
			      min(start + 2 * segment_size, sequence_size),
			      keys,
			      reverse)
		segment_size <<= 1
