"""Some prime related functions."""
from collections.abc import Generator
from math import sqrt, floor

# Since we have no stub for the external package bitarry, we tell mypy to
# ignore typechecking on it.
from bitarray import bitarray   # type: ignore


def is_prime(n: int) -> bool:
	"""Return True if n is a prime, else return False."""
	
	if not isinstance(n, int):
		return False
	
	if n < 2:
		return False
	
	if n % 2 == 0:
		return n == 2
	
	for i in range(3, floor(sqrt(n)) + 1, 2):
		if n % i == 0:
			return False
	
	return True
	

def sieve_bit_array(n: int) -> bitarray:
	"""Return a bitarray, such that for i in range(n) bit i is 1 if i is a
	prime, else bit i = 0."""

	return _sieve(n, True)


def sieve_prime_list(n: int) -> list[int]:
	"""Return a list of all primes <= n."""
	
	return _sieve(n)


def _sieve(n: int, bit_array_flag: bool = False) -> list[int] | bitarray:
	"""If bit_array_flag, return a bitarry of n + 1 bits (0 .. n) where bit i
	is 1 if i is a prime, else bit i is composite. If bit_array_flag == False,
	return a list of all primes <= n + 1."""
	
	def _generator(_n: int) -> Generator[int, None, None]:
		yield 0  # 0 is not a prima
		yield 0  # 1 is not a prime
		
		# all integers >= 2 are prime until proven otherwise
		for i in range(_n + 1 - 2):
			yield 1
	
	prime_indices = bitarray(_generator(n))

	offset = 2
	while offset <= sqrt(n):
		if prime_indices[offset]:
			# any multiple k * offset with k < offset is already marked as
			# not prime, since the k * offset must be a multiple of a prime
			# < offset, and therefore already marked as composite.
			# Example: all multiples of prime 7 < 49 are 2 * 7 (multiple of
			# smaller prime 2), 3 * 7 (multiple of smaller prime 3), 4 * 7
			# (multiple of smaller prime 2), 5 * 7 (multipe of smaller
			# prime 5), 6 * 7 (multiple of smaller primes 2 and 3).
			composite_index = offset * offset
			while composite_index <= n:
				prime_indices[composite_index] = 0
				composite_index += offset
		offset += 1
	if bit_array_flag:
		return prime_indices
	else:
		return [i for i in range(n) if prime_indices[i]]
