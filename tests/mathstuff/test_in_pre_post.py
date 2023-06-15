"""Tests all available conversions."""
from in_pre_postfix import infix_to_postfix, postfix_to_infix, \
	infix_to_prefix, prefix_to_postfix, prefix_to_infix, postfix_to_prefix


def test_in_pre_pro_conversionos() -> None:
	
	test_in_post_pre = (
		("A+B-C", "AB+C-", "-+ABC"),
		("A+B*C", "ABC*+", "+A*BC"),
		("(A+B)/(C-D)", "AB+CD-/", "/+AB-CD"),
		("((A+B)*(C-D)+E)/(F+G)", "AB+CD-*E+FG+/", "/+*+AB-CDE+FG"),
		("A+B*C/D-E", "ABC*D/+E-", "-+A/*BCDE"),
		("(A+B*(C-D))/E", "ABCD-*+E/", "/+A*B-CDE"),
	)
	for infix, postfix, prefix in test_in_post_pre:
		assert infix_to_postfix(infix) == postfix
		assert infix_to_prefix(infix) == prefix
		assert postfix_to_infix(postfix) == prefix_to_infix(prefix)
		assert prefix_to_postfix(prefix) == postfix
		assert postfix_to_prefix(postfix) == prefix
