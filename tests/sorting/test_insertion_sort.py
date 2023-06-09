"""Test(s) for insertion_sort and insertion_sort_recursive."""

from collections.abc import MutableSequence, Callable
from random import randint
from typing import Protocol, Optional, Any

from common import SupportsLessThanT
from insertion_sort import insertion_sort, insertion_sort_recursive


class InsertionSortProtocol(Protocol):
	"""Protocol for specifying the signature of insertion_sort function."""
	
	def __call__(self,
	             sequence: MutableSequence[SupportsLessThanT],
	             start: int = 0,
	             stop: Optional[int] = None,
	             key: Optional[Callable[..., Any]] = None,
	             reverse: bool = False
	             ) -> None:
		...


class InsertionSortRecursiveProtocol(Protocol):
	"""Protocol for specifying the signature of insertion_sort_recursive
	function."""
	
	def __call__(self,
	             sequence: MutableSequence[SupportsLessThanT],
	             key: Optional[Callable[..., Any]] = None,
	             reverse: bool = False) -> None:
		...


def _test_insertion_sort(sort_function: InsertionSortProtocol |
                                        InsertionSortRecursiveProtocol) -> None:
	"""Do some tests for the sort_function..."""
	
	def mod_3(x: int) -> int:
		"""Just a test key function """
		
		return x % 3
	
	for i in range(250):
		base_lst = [randint(-i, i) for _ in range(i)]
		for key in (None, abs, mod_3):
			for reverse in (True, False):
				lst = list(base_lst)
				sort_function(lst, key=key, reverse=reverse)
				# insertion_sort and insertion_sort_recursive are stable!
				assert lst == sorted(lst, key=key, reverse=reverse)


def test_insertion_sort() -> None:
	"""Calls the real tests in a loop, with functions to test as argument..."""

	# The signatures of the functions, and the protocols used to specify these
	# signratures:
	#
	# def insertion_sort_recursive(sequence: MutableSequence[SupportsLessThanT],
	#                              reverse: bool = False) -> None:
	#
	# def insertion_sort(sequence: MutableSequence[SupportsLessThanT],
	#                    start: int = 0,
	#                    stop: Optional[int] = None,
	#                    reverse: bool = False) -> None:
	#
	# def _test_insertion_sort(sort_function: InsertionSortProtocol |
	#                                         InsertionSortRecursiveProtocol) \
	#       -> None:
	#
	# class InsertionSortProtocol(Protocol):
	# 	"""Protocol for specifying the signature of insertion_sort function."""
	#
	# 	def __call__(self,
	# 	             sequence: MutableSequence[SupportsLessThanT],
	# 	             start: int = 0,
	# 	             stop: Optional[int] = None,
	# 	             reverse: bool = False
	# 	             ) -> None:
	# 		...
	#
	# class InsertionSortRecursiveProtocol(Protocol):
	# 	"""Protocol for specifying the signature of insertion_sort_recursive
	#      function."""
	#
	# 	def __call__(self,
	# 	             sequence: MutableSequence[SupportsLessThanT],
	# 	             reverse: bool = False) -> None:
	# 		...
	#

	# for sort_function in (insertion_sort_recursive, insertion_sort):
	# 	# Mypy reports in the next line:
	# 	# error: Argument 1 to "_test_insertion_sort" has incompatible type
	# 	# "function"; expected "Union[InsertionSortProtocol,
	# 	# InsertionSortRecursiveProtocol]"
	# 	_test_insertion_sort(sort_function)

	# The following two lines are fine with Mypy! They are functionally
	# equivalent with the for-loop above...
	_test_insertion_sort(insertion_sort)
	_test_insertion_sort(insertion_sort_recursive)
