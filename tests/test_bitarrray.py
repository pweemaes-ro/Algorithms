"""Test of bitarray class."""

from random import choice

from bitarray import BitArray


def test_bit_array() -> None:
	nr_bits = 12345
	ba = BitArray(nr_bits)
	for i in range(len(ba)):
		set_value = choice((False, True))
		ba[i] = set_value
		get_value = ba[i]
		assert set_value == get_value
	print(f"_test_bit_array: set and read {len(ba)} bits (OK).")


test_bit_array()
