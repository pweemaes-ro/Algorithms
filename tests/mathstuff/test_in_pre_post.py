"""Tests all available conversions."""
from in_pre_postfix import infix_to_postfix, postfix_to_infix, \
	infix_to_prefix, prefix_to_postfix, prefix_to_infix, postfix_to_prefix

test_in_post_pre = (
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


def test_infix_to_postfix() -> None:
	for infix, postfix, _ in test_in_post_pre:
		assert infix_to_postfix(infix) == postfix


def test_infix_to_prefix() -> None:
	for infix, _, prefix in test_in_post_pre:
		assert infix_to_prefix(infix) == prefix, \
			f"{infix=}, " \
			f"expected (my tests): {prefix}, " \
			f"got: {infix_to_prefix(infix)}"


def test_any_to_infix() -> None:
	for infix, postfix, prefix in test_in_post_pre:
		infix_from_postfix = postfix_to_infix(postfix)
		infix_from_prefix = prefix_to_infix(prefix)
		assert infix_from_postfix == infix_from_prefix, \
			f"{infix = }, {infix_from_postfix = }, {infix_from_prefix = }"


def test_prefix_to_postfix() -> None:
	for _, postfix, prefix in test_in_post_pre:
		assert prefix_to_postfix(prefix) == postfix


def test_postfix_to_prefix() -> None:
	for _, postfix, prefix in test_in_post_pre:
		assert postfix_to_prefix(postfix) == prefix
