"""Linked list (and more?)"""
from __future__ import annotations

import time
from collections.abc import Iterator
from random import shuffle
from typing import Optional, Generic, Reversible, Any, Callable, Self, TypeAlias

from Sorting.merge_sort import merge_sorted
from Sorting.merge_sort_in_place import merge_sort_in_place
from common import SupportsLessThanT


class Node(Generic[SupportsLessThanT]):
	"""A node is data plus a reference to the next node."""
	
	def __init__(self, value: SupportsLessThanT) -> None:
		self._data = value
		self.next_node: Optional[Node[SupportsLessThanT]] = None
		
	def __repr__(self) -> str:
		"""Return string representation of the node"""
		
		return f"Node({self._data})"
	
	@property
	def data(self) -> SupportsLessThanT:
		"""Return the data of the node."""
		
		return self._data

	def __lt__(self, other: Self) -> bool:
		"""Return True if this node compares less than other node, else return
		False."""
		
		return bool(self._data < other._data)


class LinkedList(Generic[SupportsLessThanT]):
	"""A linked list is a list of nodes, starting with a head."""

	def __init__(self,
	             initial_data: Optional[Reversible[SupportsLessThanT]] = None) \
		-> None:
		"""If *initial_data* is not *None*, the data is added to the linked
		list, with the first item in *initial_data* the head of the linked
		list."""
		
		self._head: Optional[Node[SupportsLessThanT]] = None
		if initial_data:
			for data in reversed(initial_data):
				self.add(data)
	
	def __eq__(self, other: Any) -> bool:
		"""Return True if all nodes have the same value as their corresponding
		node in other, else return False."""
		
		return all(self_node.data == other_node.data
		           for self_node, other_node in zip(self, other))

	def __getitem__(self, index: int) -> Node[SupportsLessThanT]:
		"""Return the item at given index (valid negative indices are
		supported), or None if invalid index."""

		if index < 0:
			index += self.size

		if index < 0:
			raise IndexError

		for i, node in enumerate(self):
			if i == index:
				return node

		raise IndexError

	def __iter__(self) -> Iterator[Node[SupportsLessThanT]]:
		"""Yields all nodes from head to last."""
		
		current_node = self._head
		while current_node:
			yield current_node
			current_node = current_node.next_node

	def __str__(self) -> str:
		"""Return string representation of the linked list."""

		if self.size == 0:
			return "Empty Linked List"

		return ' -> '.join(str(node) for node in self)

	def __repr__(self) -> str:
		return self.__str__()
	
	def add(self, data: SupportsLessThanT) -> Node[SupportsLessThanT]:
		"""Insert a node at the beginning of the linked list. Return the new
		node."""
		
		new_node = Node(data)
		new_node.next_node = self._head
		self._head = new_node
		return new_node
	
	def append(self, data: SupportsLessThanT) -> Node[SupportsLessThanT]:
		"""Append a new node at the end. Return the appended node."""

		if self._head is None:
			return self.add(data)

		current = self._head

		while current.next_node:
			current = current.next_node

		current.next_node = Node(data)
		return current.next_node

	def insert(self, data: SupportsLessThanT, index: int) \
		-> Optional[Node[SupportsLessThanT]]:
		"""Insert a new node containing *data* at position *index*. If the
		index is out of bounds (> linked list size), no node is inserted.
		Return the inserted node or None if index out of bounds."""

		if index == 0:
			return self.add(data)

		position = index - 1
		current = self._head

		while current and position:
			current = current.next_node
			position -= 1

		if current:
			new_node = Node(data)
			new_node.next_node = current.next_node
			current.next_node = new_node
			return new_node
		else:
			return None

	def remove(self, key: SupportsLessThanT) \
		-> Optional[Node[SupportsLessThanT]]:
		"""Delete the first node in the linked list containing *data*. Return
		the deleted node, or None if *data* not found."""

		if self._head and self._head.data == key:
			removed_node = self._head
			self._head = self._head.next_node
			return removed_node

		current = self._head
		while current and current.next_node:
			if current.next_node.data == key:
				removed_node = current.next_node
				current.next_node = current.next_node.next_node
				return removed_node
			current = current.next_node

		return None

	def remove_at_index(self, index: int) -> Optional[Node[SupportsLessThanT]]:
		"""Delete the node at position *index*. Return the removed node's
		*data* if a node was removed, or None if no node removed due to index
		out of bounds."""

		if index < 0 or not self._head:
			return None

		if index == 0:
			removed_node = self._head
			self._head = self._head.next_node
			return removed_node

		position = index - 1
		current: Optional[Node[SupportsLessThanT]] = self._head

		while current and position:
			current = current.next_node
			position -= 1

		if current and current.next_node:
			removed_node = current.next_node
			current.next_node = current.next_node.next_node
			return removed_node

		return None

	def search(self, target: SupportsLessThanT) \
		-> Optional[Node[SupportsLessThanT]]:
		"""Return the first node in the linked list containing *target*, or
		None of no such node found."""

		for node in self:
			if node.data == target:
				return node
		
		return None

	@property
	def size(self) -> int:
		"""Return the number of nodes in the linked list."""
		
		size = 0

		current = self._head
		while current:
			size += 1
			current = current.next_node
		return size

	def _split(self) -> tuple[LinkedList[SupportsLessThanT],
							  LinkedList[SupportsLessThanT]]:
		"""Return two 'halves' of self (if nr of nodes is odd, the second
		'halve' will have one more item than the first 'halve'."""

		mid_point = self.size // 2

		left: LinkedList[SupportsLessThanT] \
			= LinkedList([self[i].data for i in range(mid_point)])
		left[mid_point - 1].next_node = None
		right: LinkedList[SupportsLessThanT] = LinkedList()
		right._head = self[mid_point]

		return left, right

	@staticmethod
	def _merge(left: "LinkedList"[SupportsLessThanT],
	           right: "LinkedList"[SupportsLessThanT]) \
		-> "LinkedList"[SupportsLessThanT]:

		_merged: LinkedList[SupportsLessThanT] = LinkedList()
		left_index = right_index = 0

		while left_index < left.size and right_index < right.size:
			left_value = left[left_index].data
			right_value = right[right_index].data

			if left_value < right_value:
				_merged.append(left_value)
				left_index += 1
			else:
				_merged.append(right_value)
				right_index += 1

		while left_index < left.size:
			_merged.append(left[left_index].data)
			left_index += 1

		while right_index < right.size:
			_merged.append(right[right_index].data)
			right_index += 1

		return _merged

	def merge_sort(self) -> LinkedList[SupportsLessThanT]:
		"""Special Linked List Merge Sort (performs bad!)"""
		
		if self.size <= 1:
			return self

		left_part, right_part = self._split()
		left = left_part.merge_sort()
		right = right_part.merge_sort()

		return self._merge(left, right)

	def sort(self) -> None:
		"""In place sorts the linked list's nodes ascending on the node data."""

		merge_sort_in_place(nodes := list(self))

		self._head = None
		for node in reversed(nodes):
			self.add(node.data)

	def sorted(self) -> LinkedList[SupportsLessThanT]:
		"""Return a new linked list with the same nodes as self, but sorted
		ascending on the node data."""

		return LinkedList([node.data
		                   for node in merge_sorted(list(self))])

	def py_sorted(self) -> LinkedList[SupportsLessThanT]:
		"""The fastest way to sort a linked list... Using Python sorted."""
		
		return LinkedList([node.data
		                   for node in sorted(list(self))])


if __name__ == "__main__":
	
	def main() -> None:
		"""A few basci tests"""
		# for i in range(10):
		for i in (10,):
			lst = list(range(i))
			shuffle(lst)
			linked_list: LinkedList[int] = LinkedList(lst)
			py_sorted_linked_list = LinkedList(sorted(lst))
			print(f"BEFORE:")
			print(f"{linked_list           = }")
			print(f"{py_sorted_linked_list = }")
			sorted_linked_list = LinkedList(sorted(lst))
			print(f"AFTER sorted_linked_list = linked_list.sorted():")
			print(f"{linked_list           = }")
			print(f"{py_sorted_linked_list = }")
			print(f"{sorted_linked_list    = }")
			assert sorted_linked_list == py_sorted_linked_list

			ms_linked_list = linked_list.merge_sort()
			print(f"AFTER ms_linked_list = linked_list.merge_sort():")
			print(f"{linked_list           = }")
			print(f"{ms_linked_list        = }")
			print(f"{py_sorted_linked_list = }")
			assert ms_linked_list == py_sorted_linked_list

			linked_list.sort()
			print(f"AFTER linked_list.sort() (IN PLACE):")
			print(f"{linked_list           = }")
			print(f"{py_sorted_linked_list = }")
			assert linked_list == py_sorted_linked_list

	main()
	
	OptionalLinkedList: TypeAlias = Optional[LinkedList]
	SortFunc = Callable[[LinkedList], OptionalLinkedList]
	Functions = tuple[SortFunc, str]
	
	
	def timing(n: int) -> None:
		"""Do some timing..."""
	
		functions: tuple[Functions, ...] = \
			((lambda l: l.merge_sort(), "merge_sort"),
			(lambda l: l.sorted(), "sorted"),
			(lambda l: l.sort(), "sort"),
			(lambda l: l.py_sorted(), "py_sort"))
		for (f, name) in functions:
			t = 0
			for i in range(n):
				
				lst = list(range(i))
				sorted_linked_list: LinkedList[int] = LinkedList(lst)
				shuffle(lst)
				unsorted_linked_list: LinkedList[int] = LinkedList(lst)
				start = time.perf_counter_ns()
				result = f(unsorted_linked_list)
				stop = time.perf_counter_ns()
				if result:
					# print(result)
					assert result == sorted_linked_list
				else:
					# print(sorted_linked_list)
					assert unsorted_linked_list == sorted_linked_list
				t += stop - start
			print(f"{name = :10s}: {t:15d}")

	timing(100)
	