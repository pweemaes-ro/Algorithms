"""Some matrix functionality"""
from typing import TypeAlias, TypeVar

T = TypeVar("T", int, float, complex)
Vector: TypeAlias = list[T]
Matrix: TypeAlias = list[Vector[T]]


def dot_product(v_1: Vector[T], v_2: Vector[T]) -> T:
	"""Return the dot-product of the two vectors."""
	
	if len(v_1) != len(v_2):
		raise ValueError(f"{v_1} and {v_2} are incompatible for dot product.")
	
	return sum(a * b for (a, b) in zip(v_1, v_2))


def matrix_product(m_1: Matrix[T], m_2: Matrix[T]) -> Matrix[T]:
	"""Return the product of the two matrices."""
	
	if len(m_1) == 0 or len(m_2) == 0 or len(m_1[0]) == 0 or len(m_2[0]) == 0:
		return []

	m = len(m_1)
	n_1 = len(m_1[0])
	n_2 = len(m_2)
	p = len(m_2[0])

	# Product only defined if nr cols of m_1 == nr_rows of m_2.
	if n_1 != n_2:
		raise ValueError(f"({m} x {n_1}) matrix and ({n_2} x {p}) matrix are "
		                 f"incompatible for matrix product.")
	
	if not all(len(row) == n_1 for row in m_1):
		raise ValueError(f"{m_1} is not a valid matrix")
	if not all(len(row) == p for row in m_2):
		raise ValueError(f"{m_2} is not a valid matrix")
	
	return [[dot_product(m_1[row_nr], [row[col_nr] for row in m_2])
	         for col_nr in range(p)]
	        for row_nr in range(m)]
