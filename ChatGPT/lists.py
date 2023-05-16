"""The code below was generated by ChatGPT with the following prompt:

Please write the fastest possible Python code implementing a singly linked
list, supporting the following operations: add (adds a node at the head of the
list), insert (inserts a node at a specified index), get (retrieves the data of
the node at a specified index), delete (deletes a node at a specified index).
Be as much PEP 8 compliant as you can, and also use type annotations.

[ChatGPT also generated a brief expanation of each method, which I added as doc
strings to the respective methods]."""

# Added by pw to fix  stringified type annotations.
from __future__ import annotations

from typing import Any, Optional


class Node:
	"""A node holds data and a reference to its successor (if any)."""
	
	def __init__(self, data: Any, next_node: Optional[Node] = None):
		self.data = data
		self.next = next_node


class SinglyLinkedList:
	"""pw: ChatGPT GENERATED"""
	def __init__(self) -> None:
		"""Initializes an empty singly linked list with a null head."""
		
		self.head = None

	def add(self, data: Any) -> None:
		"""Adds a new node with the given data at the head of the list.
		The previous head becomes the next node of the new head."""
		
		self.head = Node(data, next_node=self.head)

	def insert(self, data: Any, index: int) -> None:
		"""Inserts a new node with the given data at the specified index. If
		the index is 0, the new node is added at the head of the list.
		Otherwise, the method iterates through the list to find the node before
		the desired index and inserts the new node between that node and the
		next one."""
		
		if index == 0:
			self.add(data)
			return

		current = self.head
		for i in range(index - 1):
			if current.next is None:
				raise IndexError("Index out of range")
			current = current.next

		current.next = Node(data, next_node=current.next)

	def get(self, index: int) -> Any:
		"""Retrieves the data of the node at the specified index. The method
		iterates through the list until it reaches the desired index, then
		returns the data of the corresponding node. Raises an IndexError if the
		index is out of range."""
		
		current = self.head
		for i in range(index):
			if current is None:
				raise IndexError("Index out of range")
			current = current.next

		return current.data

	def delete(self, index: int) -> None:
		"""Deletes the node at the specified index. If the index is 0, the head
		of the list is updated to point to the next node. Otherwise, the method
		iterates through the list to find the node before the desired index and
		updates its next pointer to skip over the node to be deleted."""
		
		if self.head is None:
			raise IndexError("Index out of range")

		if index == 0:
			self.head = self.head.next
			return

		current = self.head
		for i in range(index - 1):
			if current.next is None:
				raise IndexError("Index out of range")
			current = current.next

		current.next = current.next.next
