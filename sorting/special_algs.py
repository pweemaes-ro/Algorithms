"""A few special sorting algorthms..."""
import time
from collections.abc import Iterable
from random import sample


# Suppose you must sort and output a subset of unsorted integers in the range
# [a, a + n] (a total of n + 1 integers) from a file, with
# - each integer in the subset being unique in (as implied by 'set')
# - there is no additional data attached to any of the integers in the subset
# and you don't have enough memory to store all integers in the file. Then this
# algorithm is suitable (requires little memory):
# - create a bitarray of n + 1 bits, all initialized to 0. Requires
#   (n + 8) // 8 bytes.
# - while not all integers were read from file:
#   - read next integer (say a + i) (with 0 <= i <= n) from file,
#   - set bit at position a + i in the bitarray to 1.
# - for bit position m from 0 to n: if bit at position m in bitarray is set to
#   1, output a + m (if not set to 1, skip it).
#
# 	Considering this is supposed to be a solution for a system with very little
# 	memory, a BitArray class is perhaps a luxury, so the implementation uses
# 	simple functions.

def set_bit(bit_array: bytearray, offset: int) -> None:
	"""Set bit in bit_array at 0-based offset. Raises IndexError if offset out
	of bounds."""
	
	bit_array[offset // 8] |= 1 << (offset % 8)


def clear_bit(bit_array: bytearray, offset: int) -> None:
	"""Clear bit in bit_array at 0-based offset. Raises IndexError if offset
	out of bounds."""
	
	bit_array[offset // 8] ^= (1 << (offset % 8))


def test_bit(bit_array: bytearray, offset: int) -> bool:
	"""Return True if bit in bit_array at offset is set, else False. Raises
	IndexError if offset out of bounds."""

	return bit_array[offset // 8] & (1 << (offset % 8)) != 0


def bit_array_sort(start: int, stop: int, filename: str) -> Iterable[int]:
	"""Return a generator that yields sorted integers from data_file. The
	integers in the file must all expected to be in the range(start, stop)."""
	
	bit_array = bytearray((stop - start + 7) // 8)   # zero-filled by default

	with open(filename) as data_file:
		for s in data_file:
			value = int(s)
			if value < start or value >= stop:
				raise ValueError(f"Illegal value {value} "
				                 f"(must be in range({start}, {stop}))")
			set_bit(bit_array, value - start)

	yield from (bit_nr + start
	            for bit_nr in range(stop - start)
	            if test_bit(bit_array, bit_nr))


if __name__ == "__main__":
	def write_ints(start: int, stop: int, nr_ints: int, filename: str) -> None:
		"""Write nr_ints UNIQUE integers in range(start, stop) to filename."""
		
		with open(filename, "w") as f:
			for i in sample(range(start, stop, 1), nr_ints):
				f.write(str(i) + "\n")

	
	def main() -> None:
		"""Driver code..."""

		filename = "..\\sorting\\_15000.ints"
		a = 0
		n = 27000
		subset_size = 15000
		write_ints(a, a + n, subset_size, filename)
		
		time_start = time.perf_counter_ns()
		# with open(filename) as f:
		b_sorted = list(bit_array_sort(a, a + n, filename))
		time_stop = time.perf_counter_ns()

		print(f"Read and converted to bit array sorted list: "
		      f"{len(b_sorted)} integers "
		      f"in {int((time_stop - time_start) * 10 ** -9)} seconds, "
		      f"{int((time_stop - time_start) * 10 ** -6)} milliseconds.")
		print(b_sorted)

		time_start = time.perf_counter_ns()
		with open(filename) as f:
			p_sorted = sorted([int(i) for i in f])
		time_stop = time.perf_counter_ns()
		print(f"Read and converted to Python sorted list: "
		      f"{len(p_sorted)} integers from file in "
		      f"in {int((time_stop - time_start) * 10 ** -9)} seconds, "
		      f"{int((time_stop - time_start) * 10 ** -6)} milliseconds.")
		print(p_sorted)
		
		assert b_sorted == p_sorted
		assert len(b_sorted) == subset_size
		print("OK!")
	main()
