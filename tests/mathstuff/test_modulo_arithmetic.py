"""Tests for functions in modulo_arithmetic."""
from itertools import chain
from math import gcd
from random import randrange

from modulo_arithmetic import extended_euclid, bezout_coefficients, \
	fast_mod_exp, _fast_mod_memo_nr_bm_keys, _fast_mod_memo_nr_exp_mod_values

rand_base = 100000
nr_pairs = 30000
t = [(randrange(-rand_base, rand_base), randrange(-rand_base, rand_base))
     for _ in range(nr_pairs)]
v = [(i := randrange(-rand_base, rand_base), i) for _ in range(nr_pairs)]


def test_extended_euclid() -> None:
	"""Tests extended_euclid:
	- greatest common divisor is tested against trusted Python gcd,
	- bezout_coefficients is tested against stand-alone bezout_coefficients
	  function, and verified against the Bézout identity ax + by = (signed) gdc.
	"""
	for i, (a, b) in enumerate(chain(t, v), start=1):
		signed_gcd, x, y, inv = extended_euclid(a, b)
		if inv and a > 0:
			assert (inv * b * signed_gcd) % a == 1 % a
		assert bezout_coefficients(a, b) == (x, y)
		assert abs(signed_gcd) == gcd(a, b)
		assert signed_gcd == a * x + b * y


def test_fast_mod_exp() -> None:
	"""Tests fast_mod_exp function."""
	
	bases = list(range(-25, -7)) + list(range(7, 25))
	modulos = (1, 2, 3, 5, 7, 11, 13, 17)
	# Make sure exponents is a range frpm 0 to some positive int
	exponents = range(357)
	# exponents = range(356, -1, -1)
	for base in bases:
		for modulo in modulos:
			for exponent in exponents:
				assert (fast_mod_exp(base, exponent, modulo) ==
				        (base ** exponent) % modulo), \
					f"{base = }, {exponent = }, {modulo = }"
	nr_bm_keys = _fast_mod_memo_nr_bm_keys()
	assert nr_bm_keys == len(bases) * len(modulos)
	nr_exp_mod_values = _fast_mod_memo_nr_exp_mod_values()
	# May NOT HOLD if exponents is NOT a range frpm 0 to some positive int
	assert nr_exp_mod_values == nr_bm_keys * len(exponents)
