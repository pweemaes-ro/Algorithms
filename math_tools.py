"""Some math stuff"""
from collections.abc import Sequence
from functools import partial, lru_cache
from math import copysign
from numbers import Complex
from random import shuffle
from time import perf_counter_ns
from typing import Union


def horner(coefficients: Sequence[float], x: float) -> float:
	"""Calculates the value of a polynomial
	P(x) = a_n x^n + a_{n-1} x^{n-1} + ... + a_2 x^2 + a_1 x + a_0
	     = a_0 + a_1 x + a_2 x^2 + ... + a_{n-1} x^{n-1} + a_n x^n
	     = a_0 + x(a_1 + x(a_2 + ... + x(a_{n_1} + x * a_n)...)).
	Coefficients must be in order: a_n, a_{n-1}, ..., a_1, a_0, that is, if the
	polynomial is P_2(x) = 3x^2 + 2x + 1, coefficients must be [3, 2, 1].
	
	This algorithm is much faster than naive calculation (even when caching)."""
	
	p = 0.0
	for coefficient in coefficients:
		p = coefficient + x * p
	return p


"""Python has no sign function of its own. Since math.copysign(x, y) returns a
float with the magnitude (absolute value) of x but the sign of y, we have:
a) if y < 0 then sign(y) = math.copysign(1, y) == -1.0,
b) if y >= 0 then sign(y) = math.copysign(1, y) == 1.0.
On platforms that support signed zeros, copysign(1.0, -0.0) returns -1.0."""
sign = partial(copysign, 1)


@lru_cache(maxsize=None)
def _power_pos_exp(base: float, exponent: float) -> Union[Complex, float]:
	"""Cached power functon for POSITIVE or ZERO exponents only! Is much faster
	than math.pow() function, but much slower than horner() function."""

	if exponent < 0.0:
		raise ValueError(f"exponent must be >= 0, not {exponent}")

	if exponent <= 1.0:
		return base ** exponent

	return base * _power_pos_exp(base, exponent - 1)


def _power(base: float, exponent: float) -> Union[Complex, float]:
	"""(Indirectly cached) power function. Delegates to _power_pos_exp function
	(which is a cached power function) by modifying base and exponent if
	exponent is negative, using base^(-exponent) = (1/base)^exponent."""

	if base == 0:
		if exponent < 0:
			raise ValueError(f"Negative powers of 0 are undefined.")
		elif exponent == 0:
			return 1.0
		else:
			return 0.0

	if exponent < 0:
		base = 1 / base
		exponent = -exponent
	
	return _power_pos_exp(base, exponent)
	

def naive(coefficients: Sequence[float], x: float) -> float:
	"""Naive way of calculating a polynomial...
	P_n(x) = a_n x^n + a_{n-1} x^{n-1} + ... + a_2 x^2 + a_1 x + a_0
	Coefficients must be in order: a_n, a_{n-1}, ..., a_0, that is, if the
	polynomial is P_2(x) = 3x^2 + 2x + 1, coefficients must be [3, 2, 1]."""
	
	return sum(coefficient * _power(base=x, exponent=i)
	           for (i, coefficient) in enumerate(reversed(coefficients)))


if __name__ == "__main__":
	def timing() -> None:
		"""Do some timing..."""
		
		h_total = n_total = 0
		abs_extreme = 500
		for x in range(-abs_extreme, abs_extreme):
			coefficients = list(range(x))
			shuffle(coefficients)
			
			h_start = perf_counter_ns()
			_ = horner(coefficients, x)
			h_stop = perf_counter_ns()
			h_total += h_stop - h_start
		
			n_start = perf_counter_ns()
			_ = naive(coefficients, x)
			n_stop = perf_counter_ns()
			n_total += n_stop - n_start

		print(f"{h_total = :12d}")
		print(f"{n_total = :12d}")
		print(_power_pos_exp.cache_info())

	timing()
