"""Tests for matrix functions"""
from matrices import matrix_product, dot_product


def test_matrix_product() -> None:
	"""matrix product tests..."""

	m, n, p = 2, 3, 4
	m_1 = [[(c + 1) * (i + 1) for c in range(n)] for i in range(m)]
	m_2 = [[(c + 1) * ((i + 1) * 2) for c in range(p)] for i in range(n)]
	pro = matrix_product(m_1, m_2)
	assert m_1 == [[1, 2, 3], [2, 4, 6]]
	assert m_2 == [[2, 4, 6, 8], [4, 8, 12, 16], [6, 12, 18, 24]]
	assert pro == [[28, 56, 84, 112], [56, 112, 168, 224]]

	assert matrix_product([], []) == []
	assert matrix_product([[1]], [[1]]) == [[1]]
	assert matrix_product([[1], [2]], [[2, 1]]) == [[2, 1],[4, 2]]
	try:
		# incompatible: (2 x 1) x (2 x 3)
		_ = matrix_product([[1], [2]], [[0, 1, 2], [2, 1, 0]])
		assert False
	except ValueError:
		pass
	
	try:
		# second 'matrix' not a matrix (rows of different sizes)
		_ = matrix_product([[1, 2], [3, 4]], [[0, 1], [2, 1, 0]])
		assert False
	except ValueError:
		pass

	try:
		# first 'matrix' not a matrix (rows of different sizes)
		_ = matrix_product([[1, 2], [3, 4, 5]], [[0, 1], [2, 1]])
		assert False
	except ValueError:
		pass


def test_dot_product() -> None:
	assert dot_product([1, 2, 3], [4, 5, 6]) == 32
	assert dot_product([0, 0, 0], [4, 5, 6]) == 0
	assert dot_product([1 + 1j, 2 + 2j, 3 + 3j], [4, 5, 6]) == 32 + 32j
	try:
		_ = dot_product([1, 2, 3], [4, 5])
		assert False
	except ValueError:
		pass
