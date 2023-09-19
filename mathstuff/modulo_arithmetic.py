"""Functions related to modulo arithmetic."""
from typing import Optional

# For any given base (int), exponent (int >= 0), modulo (int >= 1) we have:
# __fast_mod_memo is dict of (key_1, value_1) pairs where
#   key_1 = (base, modulo), and
#   value_1 = dict of (key_2, value_2) pairs where
#       key_2 = exponent, and
#       value = (base ** exponent) % modulo if exponent > 0, 1 if exponent = 0
# base ** 0 % modulo = 0, since we use the value to multiply...
# Example: if __fast_mod_memo[(7, 13)][356] exists then
# __fast_mod_memo[(7, 13)][356] = 3 since (7 ** 356) % 13 = 3.
__fast_mod_memo: dict[tuple[int, int], dict[int, int]] = dict()


def _fast_mod_memo_nr_bm_keys() -> int:
	return len(__fast_mod_memo)


def _fast_mod_memo_nr_exp_mod_values() -> int:
	return sum(len(m) for m in __fast_mod_memo.values())


def fast_mod_exp(base: int, exponent: int, modulo: int) -> int:
	"""Fast way to calculate (base ** exponent) % modulo. This is at least
	twice as fast as calculating it simply as (base ** exponent) % modulo."""
	
	def _mod_exp(_exponent: int) -> int:
		if _exponent in memo:
			return memo[_exponent]
		
		power_of_two = 1 << (_exponent.bit_length() - 1)
		remainder = _exponent - power_of_two
		
		if power_of_two not in memo:
			memo[power_of_two] = (_mod_exp(power_of_two >> 1) ** 2) % modulo
		
		if remainder not in memo:
			memo[remainder] = _mod_exp(remainder)
		
		memo[_exponent] = (memo[remainder] * memo[power_of_two]) % modulo
		return memo[_exponent]
	
	if (base, modulo) not in __fast_mod_memo:
		__fast_mod_memo[(base, modulo)] = {0: 1, 1: base % modulo}
	
	if exponent == 0:
		return 1 % modulo
	
	memo = __fast_mod_memo[(base, modulo)]
	return _mod_exp(exponent)


def extended_euclid(a: int, b: int) -> tuple[int, int, int, int, Optional[int]]:
	"""Returns a tuple containing - in order:
	
	- the signed greatest common divisor of a and b (will be negative iif one
	  or both of a and b is/are negative).
	- the absolute value of the greatest common divisor of a and b.
	- the x-coefficient and
	- the y-coefficient of the Bézout identity ax + by = gcd(a, b) (with x and y
	  guaranteed the smallest possible coefficients satisfying this identity).
	- the modular multiplicative inverse of b modulo a (NOT a modulo b!) if it
	  exists (that is, if a and b are coprime and a is a positive integer), or
	  None if such an inverse does not exist."""
	
	r_i, r_i_plus_one = a, b
	x_i, x_i_plus_one = 1, 0
	y_i, y_i_plus_one = 0, 1

	while r_i_plus_one:
		q_i = r_i // r_i_plus_one
		r_i, r_i_plus_one = r_i_plus_one, r_i - q_i * r_i_plus_one
		x_i, x_i_plus_one = x_i_plus_one, x_i - q_i * x_i_plus_one
		y_i, y_i_plus_one = y_i_plus_one, y_i - q_i * y_i_plus_one

		assert a * x_i + b * y_i == r_i
	
	# inverses only apply if a and b are coprime and if a is a positive integer.
	if abs(r_i) > 1 or a < 1:
		inv = None
	else:
		inv = y_i
		if inv < 0:
			inv += a
	return r_i, abs(r_i), x_i, y_i, inv


def inverse(a: int, n: int) -> Optional[int]:
	"""Return the mutiplicative inverse of a modulo n, or None if no such
	inverse exists. (An inverse exists only if a and n are coprime, that is, if
	gcd(a, n) == 1, and n is a positive integer."""
	
	*_,  inv = extended_euclid(n, a)
	
	return inv


def bezout_coefficients(a: int, b: int) -> tuple[int, int]:
	"""Return the smallest possible coefficients x and y such that
	the Bézout identity ax + by == gcd(a, b)."""
	
	*_, x, y, inv = extended_euclid(a, b)
	
	return x, y
