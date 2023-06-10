"""Linear search algorithm,"""
from collections.abc import Sequence
from typing import Optional

from common import SupportsLessThanT


def linear_search(data: Sequence[SupportsLessThanT],
                  target: SupportsLessThanT) -> Optional[int]:
	"""Return the 0-based index of *target* in *data* if *target* found in
	*data*, else return *None*."""
	
	for i in range(len(data)):
		if data[i] == target:
			return i
	
	return None
