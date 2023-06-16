"""Conversion from infix to prefix and postfix using stack."""
from collections.abc import Callable
from string import ascii_uppercase
from typing import TypeAlias, Optional


__precedence: dict[str, int] = {'^': 4, '*': 3, '/': 3, '+': 2, '-': 2}
__right_associative_operators = set("^")
__left_associative_operators = set("+-*/")
__operators = __right_associative_operators.union(__left_associative_operators)
__operands = set(ascii_uppercase)

Operator: TypeAlias = str
Operators: TypeAlias = set[Operator]
Operand: TypeAlias = str
OperatorStack: TypeAlias = list[Operator]
OperandStack: TypeAlias = list[Operand]
PopFunction: TypeAlias = Callable[[OperatorStack, Operator], Optional[Operator]]


def _is_operand(symbol: str) -> bool:
	return len(symbol) == 1 and symbol.upper() in __operands


def _is_operator(symbol: str) -> bool:
	return symbol in __operators


def _pop_any(operator_stack: OperatorStack, operator: Operator,
             associative_operators: Operators) -> Optional[Operator]:
	"""Pop and return from *operator_stack* if top of stack is an operator that
	1. has higher precedence than *operator*, or
	2. has equal precedence than *operator* and *operator* is in the set of
	   associate operators."""

	if len(operator_stack) == 0:
		return None

	stack_operator = operator_stack[-1]

	if not _is_operator(stack_operator):
		return None

	if __precedence[stack_operator] > __precedence[operator]:
		return operator_stack.pop()

	if __precedence[stack_operator] == __precedence[operator]:
		if operator in associative_operators:
			return operator_stack.pop()

	return None


def _pop_postfix(operator_stack: OperatorStack, operator: Operator) \
	-> Optional[Operator]:

	return _pop_any(operator_stack, operator, __left_associative_operators)


def _pop_prefix(operator_stack: OperatorStack, operator: Operator) \
	-> Optional[Operator]:

	return _pop_any(operator_stack, operator, __right_associative_operators)


def _swap_chars(string: str, char_1: str, char_2: str) -> str:
	"""Return *string* but with all occurances of *char_1* replaced by *char_2*
	and all occurances of *char_2* replaced by *char_1*."""
	
	swapped_list = list(string)
	
	for i in range(len(swapped_list)):
		if swapped_list[i] == char_1:
			swapped_list[i] = char_2
		elif swapped_list[i] == char_2:
			swapped_list[i] = char_1
	
	return ''.join(swapped_list)


def _postfix_to_infix(postfix: str) -> str:
	
	operand_stack: OperandStack = []
	
	for symbol in postfix:
		if _is_operator(symbol):
			right_operand = operand_stack.pop()
			left_operand = operand_stack.pop()
			operand_stack.append("(" + left_operand + symbol + right_operand
			                     + ")")
		else:
			operand_stack.append(symbol)
	
	return ''.join(operand_stack)[1:-1]


def postfix_to_infix(postfix: str) -> str:
	"""Return the infix representation of the postfix expression. Result may
	have redundant parentheses."""
	
	return _postfix_to_infix(postfix)


def prefix_to_infix(prefix: str) -> str:
	"""Return the infix representation of the prefix expression. Result may
	have redundant parentheses."""
	
	return _swap_chars(_postfix_to_infix(prefix[::-1])[::-1], "(", ")")


def _postfix_to_prefix(postfix: str) -> str:
	
	operand_stack: OperandStack = []
	
	for symbol in postfix:
		if _is_operand(symbol):
			operand_stack.append(symbol)
		else:
			right_operand = operand_stack.pop()
			left_operand = operand_stack.pop()
			operand_stack.append(symbol + left_operand + right_operand)
	
	return operand_stack.pop()


def postfix_to_prefix(postfix: str) -> str:
	"""Return prefix representation of the postfix expression."""
	
	return _postfix_to_prefix(postfix)


def prefix_to_postfix(prefix: str) -> str:
	"""Return postfix representation of the prefix expression."""

	return _postfix_to_prefix(prefix[::-1])[::-1]


def _infix_to_postfix(infix: str, *, pop_function: PopFunction) -> str:
	"""Return postfix representation of the infix expression."""

	postfix_list: list[str] = []
	operator_stack: OperatorStack = []
	
	for symbol in infix:
		if _is_operand(symbol):
			postfix_list.append(symbol)
		
		elif _is_operator(symbol):
			while operator := pop_function(operator_stack, symbol):
				postfix_list.append(operator)
			operator_stack.append(symbol)
		
		elif symbol == "(":
			operator_stack.append(symbol)
		
		elif symbol == ")":
			while len(operator_stack) \
					and (popped_operator := operator_stack.pop()) != "(":
				postfix_list.append(popped_operator)
	
	while len(operator_stack):
		postfix_list.append(operator_stack.pop())
	
	return ''.join(postfix_list)


def infix_to_prefix(infix: str) -> str:
	"""Using a few 'tricks' is faster than converting infix to postfix and then
	postfix to prefix...'"""

	return _infix_to_postfix(_swap_chars(infix, "(", ")")[::-1],
	                         pop_function=_pop_prefix)[::-1]


def infix_to_postfix(infix: str) -> str:
	"""After introducing bla"""
	return _infix_to_postfix(infix, pop_function=_pop_postfix)
