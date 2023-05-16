"""Linked list (and more?)"""
from __future__ import annotations
from random import shuffle
from typing import Optional, Iterator, Generic, Reversible, Union

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

	def __lt__(self, other: Node[SupportsLessThanT]) -> bool:
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
		self._size = 0
		if initial_data:
			for data in reversed(initial_data):
				self.add(data)
	
	def __eq__(self, other: LinkedList) -> bool:
		return all(self_node.data == other_node.data
		           for self_node, other_node in zip(self, other))

	def __getitem__(self, index: Union[int, slice]) \
		-> Optional[list[Node[SupportsLessThanT]], Node[SupportsLessThanT]]:
		"""Return the item at given index (valid negative indices are
		supported), or None if invalid index."""
		
		if isinstance(index, int):
			if index < 0:
				index += self._size
			
			if index < 0:
				return None
			
			for i, node in enumerate(self):
				if i == index:
					return node
		elif isinstance(index, slice):
			print(f"{index = }")
			return [self[i] for i in range(index.start, index.stop, index.step)]
		
		return None
	
	def __iter__(self) -> Iterator[Node[SupportsLessThanT]]:
		current_node = self._head
		while current_node:
			yield current_node
			current_node = current_node.next_node
	
	def __str__(self) -> str:
		"""Return string representation of the linked list."""
		
		if self.size() == 0:
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
		self._size += 1
		return new_node
	
	def insert(self,
	           data: SupportsLessThanT,
	           index: int) -> Optional[Node[SupportsLessThanT]]:
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
			self._size += 1
			return new_node
		else:
			return None
	
	def remove(self, key: SupportsLessThanT) -> Optional[Node[SupportsLessThanT]]:
		"""Delete the first node in the linked list containing *data*. Return
		the deleted node, or None if *data* not found."""
		
		if self._head and self._head.data == key:
			removed_node = self._head
			self._head = self._head.next_node
			self._size -= 1
			return removed_node
		
		current = self._head
		while current and current.next_node:
			if current.next_node.data == key:
				removed_node = current.next_node
				current.next_node = current.next_node.next_node
				self._size -= 1
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
			self._size -= 1
			return removed_node
		
		position = index - 1
		current: Optional[Node[SupportsLessThanT]] = self._head
		
		while current and position:
			current = current.next_node
			position -= 1
		
		if current and current.next_node:
			removed_node = current.next_node
			current.next_node = current.next_node.next_node
			self._size -= 1
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
	
	def size(self) -> int:
		"""Return the number of nodes in the linked list."""
		
		return self._size
	
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


if __name__ == "__main__":
	
	def main() -> None:
		"""A few basci tests"""
		for i in range(10):
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
	
			linked_list.sort()
			print(f"AFTER linked_list.sort() (IN PLACE):")
			print(f"{linked_list           = }")
			print(f"{py_sorted_linked_list = }")
			assert linked_list == py_sorted_linked_list

	main()
