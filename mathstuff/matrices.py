"""Some matrix functionality"""
import time
from collections import defaultdict
from numbers import Number
from typing import TypeAlias, TypeVar

T = TypeVar("T", bound=Number)
Matrix: TypeAlias = list[list[T]]


def dot_product(v_1: list[T], v_2: list[T]) -> T:
	"""Return the dot-product of the two vectors."""
	
	assert len(v_1) == len(v_2), f"vectors {v_1} and {v_2} incompatible."
	
	return sum(a * b for (a, b) in zip(v_1, v_2))


def matrix_product(m_1: Matrix, m_2: Matrix) -> Matrix:
	"""Return the product of the two matrices."""
	
	if len(m_1) == 0 or len(m_2) == 0 or len(m_1[0]) == 0 or len(m_2[0]) == 0:
		return []

	m_1_nr_rows = len(m_1)
	m_1_nr_cols = len(m_1[0])
	m_2_nr_rows = len(m_2)
	m_2_nr_cols = len(m_2[0])

	# Product only defined if nr cols of m_1 == nr_rows of m_2.
	assert m_1_nr_cols == m_2_nr_rows, f"({m_1_nr_rows} x {m_1_nr_cols}) " \
	                                   f"matrix and ({m_2_nr_rows} x " \
	                                   f"{m_2_nr_cols}) matrix are " \
	                                   f"incompatible for product."
	
	return [[dot_product(m_1[row_nr], [row[col_nr] for row in m_2])
	         for col_nr in range(m_2_nr_cols)]
	        for row_nr in range(m_1_nr_rows)]

	
if __name__ == "__main__":
	
	def main() -> None:
		"""ONE test..."""
		m, n, p = 100, 150, 200
		# m_1 = [[randint(0, 100) for _ in range(n)] for i in range(m)]
		# m_2 = [[randint(0, 100) for _ in range(p)] for i in range(n)]
		m_1 = [[(c + 1) * (i + 1) for c in range(n)] for i in range(m)]
		m_2 = [[(c + 1) * ((i + 1) * 2) for c in range(p)] for i in range(n)]
		pro = matrix_product(m_1, m_2)
		if (m, n, p) == (2, 3, 4):
			assert m_1 == [[1, 2, 3], [2, 4, 6]]
			assert m_2 == [[2, 4, 6, 8], [4, 8, 12, 16], [6, 12, 18, 24]]
			assert pro == [[28, 56, 84, 112], [56, 112, 168, 224]]
		
		print(m_1)
		print(m_2)
		print(pro)

	
	def timing_tests() -> None:
		"""Do some timing..."""
		
		dim_start, dim_stop = 5, 16
		nr_tests_per_dims = 50
		timing_data: dict[int, int] = defaultdict(int)
		for m in range(dim_start, dim_stop):
			for n in range(dim_start, dim_stop):
				m_1 = [[(c + 1) * (i + 1) for c in range(n)] for i in
				       range(m)]
				for p in range(dim_start, dim_stop):
					m_2 = [[(c + 1) * ((i + 1) * 2) for c in range(p)] for i in
					       range(n)]
					key = m * n * p
					for tests in range(nr_tests_per_dims):
						start = time.perf_counter_ns()
						_ = matrix_product(m_1, m_2)
						stop = time.perf_counter_ns()
						timing_data[key] += stop - start
		print(timing_data)
		print(tuple(sorted(timing_data.items())))
	
	main()
	# timing_tests()
