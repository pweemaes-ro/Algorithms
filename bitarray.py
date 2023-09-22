"""A simple bitarray class."""


class BitArray:
	"""A (very) simple bitarray class. All bits are initialized to 0. Bits can
	be set and read using indexing, and len() is supported."""
	
	def __init__(self, nr_bits: int) -> None:
		self.__nr_bits = nr_bits
		self.__data = bytearray(0 for _ in range((nr_bits + 7) // 8))

	def __getitem__(self, bit_nr: int) -> bool:
		byte_offset, bit_offset = divmod(bit_nr, 8)
		return bool(self.__data[byte_offset] & (1 << bit_offset))
	
	def __setitem__(self, bit_nr: int, bit_value: bool) -> None:
		byte_offset, bit_offset = divmod(bit_nr, 8)
		mask = 1 << bit_offset
		if bit_value:
			self.__data[byte_offset] |= mask
		else:
			self.__data[byte_offset] &= ~mask

	def __len__(self) -> int:
		return self.__nr_bits

#
# if __name__ == "__main__":
# 	from random import choice
#
# 	def _test_bit_array() -> None:
# 		nr_bits = 12345
# 		ba = BitArray(nr_bits)
# 		for i in range(len(ba)):
# 			set_value = choice((False, True))
# 			ba[i] = set_value
# 			get_value = ba[i]
# 			assert set_value == get_value
# 		print(f"_test_bit_array: set and read {len(ba)} bits (OK).")
#
# 	_test_bit_array()
