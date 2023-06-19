"""Tests all available conversions."""
from math import isclose
from random import randint
from typing import Any

from in_pre_postfix import infix_to_postfix, postfix_to_infix, \
	infix_to_prefix, prefix_to_postfix, prefix_to_infix, postfix_to_prefix, \
	__power_operator, __operators, eval_postfix, eval_prefix

unspaced_tuple = (
	("A+B-C", "AB+C-", "-+ABC"),
	("A+B*C", "ABC*+", "+A*BC"),
	("(A+B)/(C-D)", "AB+CD-/", "/+AB-CD"),
	("((A+B)*(C-D)+E)/(F+G)", "AB+CD-*E+FG+/", "/+*+AB-CDE+FG"),
	("A+B*C/D-E", "ABC*D/+E-", "-+A/*BCDE"),
	("(A+B*(C-D))/E", "ABCD-*+E/", "/+A*B-CDE"),
	("A+B", "AB+", "+AB"),
	("A+B*C", "ABC*+", "+A*BC"),
	("(A+B)*C", "AB+C*", "*+ABC"),
	("A+B-C", "AB+C-", "-+ABC"),
	("A*B+C", "AB*C+", "+*ABC"),
	("A*(B+C)", "ABC+*", "*A+BC"),
	("A^B^C", "ABC^^", "^A^BC"),
	("A^B*C", "AB^C*", "*^ABC"),
	("A^(B*C)", "ABC*^", "^A*BC"),
	("(A^B)*C", "AB^C*", "*^ABC"),
	("A+(B*C^D-E)^(F+G*H)-I", 'ABCD^*E-FGH*+^+I-', "-+A^-*B^CDE+F*GHI"),
)


def _get_test_data() -> tuple[list[str]]:
	return tuple(list(' '.join(string).replace("^", __power_operator)
	                  for string in line)
	             for line in unspaced_tuple)


def _get_operand_value_pairs(line: list[str]) -> list[tuple[str]]:
	operands: set[str] = set(c for c in line[0] if c not in __operators)
	operands -= set(' ()')
	values: list[str] = [str(randint(-3, 3)) for _ in operands]
	
	return [*zip(operands, values)]


def _get_randomized_eval_data(symbol_data: tuple[list[str]]) \
	-> tuple[list[str]]:
	
	eval_lines: list[list[str]] = []
	for line in symbol_data:
		eval_line: list[str] = []
		operand_value_pairs = _get_operand_value_pairs(line)
		for string in line:
			eval_string = string
			for operand, value in operand_value_pairs:
				eval_string = eval_string.replace(operand, value)
			eval_line.append(eval_string)
		eval_lines.append(eval_line)
	return tuple(eval_lines)


in_post_pre_data = _get_test_data()
eval_data = _get_randomized_eval_data(in_post_pre_data)


def test_infix_to_postfix() -> None:
	for infix, postfix, _ in in_post_pre_data:
		assert infix_to_postfix(infix) == postfix


def test_infix_to_prefix() -> None:
	for infix, _, prefix in in_post_pre_data:
		assert infix_to_prefix(infix) == prefix, \
			f"{infix=}, " \
			f"expected (my tests): {prefix}, " \
			f"got: {infix_to_prefix(infix)}"


def test_any_to_infix() -> None:
	for infix, postfix, prefix in in_post_pre_data:
		infix_from_postfix = postfix_to_infix(postfix)
		infix_from_prefix = prefix_to_infix(prefix)
		assert infix_from_postfix == infix_from_prefix, \
			f"{infix = }, {infix_from_postfix = }, {infix_from_prefix = }"


def test_prefix_to_postfix() -> None:
	for _, postfix, prefix in in_post_pre_data:
		assert prefix_to_postfix(prefix) == postfix


def test_postfix_to_prefix() -> None:
	for _, postfix, prefix in in_post_pre_data:
		assert postfix_to_prefix(postfix) == prefix


def _parenthesize_negative_values(infix: str) -> str:
	"""In order to let eval return the same value as the polish versions, we
	must put parentheses around all negative operands in the eval input."""
	
	as_list = infix.split()
	for i, string in enumerate(as_list):
		if len(as_list[i]) > 1 and as_list[i][0] == '-':
			as_list[i] = "(" + as_list[i] + ")"
	return " ".join(as_list)


def _types_ok(expected: Any, eval_value: Any) -> bool:
	assert isinstance(expected, complex) == isinstance(eval_value, complex)
	
	if isinstance(expected, (int, float)):
		assert isinstance(eval_value, (int, float))

	return True


def _values_ok(expected: Any, eval_value: Any) -> bool:
	
	if isinstance(expected, complex):
		assert (expected.real == eval_value.real) and \
			(expected.imag == eval_value.imag)
	
	if isinstance(expected, (float, int)):
		assert isclose(expected, eval_value, rel_tol=0.001)
	
	return True


def test_eval_postfix() -> None:
	ok = 0

	global eval_data
	
	iterations = 500
	for i in range(iterations):
		# Each iteration uses different random test values!
		eval_data = _get_randomized_eval_data(in_post_pre_data)
		
		for infix, postfix, _ in eval_data:
			try:
				expected = eval(_parenthesize_negative_values(infix))
				postfix_value = eval_postfix(postfix)
				
				assert _types_ok(expected, postfix_value)

				assert _values_ok(expected, postfix_value)

				ok += 1
			
			except ZeroDivisionError:
				ok += 1
			except (TypeError, OverflowError):
				assert False

	assert ok == iterations * len(eval_data)


def test_eval_prefix() -> None:
	ok = 0
	
	global eval_data
	
	iterations = 500
	for i in range(iterations):

		# Each iteration uses different random test values!
		eval_data = _get_randomized_eval_data(in_post_pre_data)
	
		for infix, _, prefix in eval_data:
			try:
				expected = eval(_parenthesize_negative_values(infix))
				# postfix_value = eval_postfix(postfix)
				prefix_value = eval_prefix(prefix)

				assert _types_ok(expected, prefix_value)

				assert _values_ok(expected, prefix_value)

				ok += 1
			
			except ZeroDivisionError:
				ok += 1
			except (TypeError, OverflowError):
				assert False

	assert ok == iterations * len(eval_data)
