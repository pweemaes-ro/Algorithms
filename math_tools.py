"""Some math stuff"""
from collections.abc import Sequence
from functools import partial, lru_cache
from math import copysign, sqrt
from random import shuffle
from time import perf_counter_ns
from typing import Optional


def horner_polynomial(coefficients: Sequence[float], x: float) -> float:
	"""Calculates the value of a polynomial
	P(x) = a_n x^n + a_{n-1} x^{n-1} + ... + a_2 x^2 + a_1 x + a_0
	     = a_0 + a_1 x + a_2 x^2 + ... + a_{n-1} x^{n-1} + a_n x^n
	     = a_0 + x(a_1 + x(a_2 + ... + x(a_{n_1} + x * a_n)...)).
	Coefficients must be in order: a_n, a_{n-1}, ..., a_1, a_0, that is, if the
	polynomial is P_2(x) = 3x^2 + 2x + 1, coefficients must be [3, 2, 1].
	
	This algorithm is O(n) and much faster than naive calculation (even when
	caching)."""
	
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
def _power_pos_exp(base: complex, exponent: complex) -> complex:
	"""Cached power functon for POSITIVE or ZERO exponents only! Is much faster
	than math.pow() function, but much slower than horner() function."""

	if sign(exponent) == -1.0:
		raise ValueError(f"exponent must be >= 0, not {exponent}")

	if abs(exponent) <= 1.0:
		return base ** exponent
		
	return base * _power_pos_exp(base, exponent - 1)


def _power(base: complex, exponent: complex) -> complex:
	"""(Indirectly cached) power function. Delegates to _power_pos_exp function
	(which is a cached power function) by modifying base and exponent if
	exponent is negative, using base^(-exponent) = (1/base)^exponent."""

	if base == 0:
		if sign(exponent) == -1.0:
			raise ValueError(f"Negative powers of 0 are undefined.")
		elif exponent == 0:
			return 1.0
		else:
			return 0.0

	if sign(exponent) == -1.0:
		base = 1 / base
		exponent = -exponent
	
	return _power_pos_exp(base, exponent)
	

def _naive_polynomial(coefficients: Sequence[int], x: float) -> complex:
	"""Naive way of calculating a polynomial...
	P_n(x) = a_n x^n + a_{n-1} x^{n-1} + ... + a_2 x^2 + a_1 x + a_0
	Coefficients must be in order: a_n, a_{n-1}, ..., a_0, that is, if the
	polynomial is P_2(x) = 3x^2 + 2x + 1, coefficients must be [3, 2, 1].
	Although this is - like Horner - O(n), it is much slower, since the cost
	of coefficient * (x ** i) is much higher than coeeficient + (x * p)."""
	
	return sum(coefficient * _power(base=x, exponent=i)
	           for (i, coefficient) in enumerate(reversed(coefficients)))


def get_real_roots(a: float, b: float, c: float) \
	-> tuple[Optional[float], Optional[float]]:
	"""Return the real roots of ax^2 + bx + c. If the discriminant is 0,
	the two roots are the same. If the discriminant is negative, no real roots
	exist (both are set to None)."""
	
	discriminant = b ** 2 - (4 * a * c)
	if discriminant < 0:
		return None, None
	
	denominator = 2 * a
	
	if discriminant == 0:
		# Both roots are equal.
		root = -b / denominator
		return root, root
	else:
		root_d = sqrt(discriminant)
		return (-b + root_d) / denominator, (-b - root_d) / denominator


if __name__ == "__main__":
	def timing() -> None:
		"""Do some timing..."""
		
		h_total = n_total = 0
		abs_extreme = 500
		for x in range(-abs_extreme, abs_extreme):
			coefficients = list(range(x))
			shuffle(coefficients)
			
			h_start = perf_counter_ns()
			_ = horner_polynomial(coefficients, x)
			h_stop = perf_counter_ns()
			h_total += h_stop - h_start
		
			n_start = perf_counter_ns()
			_ = _naive_polynomial(coefficients, x)
			n_stop = perf_counter_ns()
			n_total += n_stop - n_start

		print(f"{h_total = :12d}")
		print(f"{n_total = :12d}")
		print(_power_pos_exp.cache_info())

	timing()
