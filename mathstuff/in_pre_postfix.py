"""Conversion from infix to prefix and postfix using stack."""
from string import ascii_uppercase
from typing import TypeVar, TypeAlias, Optional


T = TypeVar('T')

__precedence: dict[str, int] = {'^': 4, '*': 3, '/': 3, '+': 2, '-': 2}
__right_associative_operators = set("^")
__left_associative_operators = set("+-*/")
__operators = __right_associative_operators.union(__left_associative_operators)
__operands = set(ascii_uppercase)

Operator: TypeAlias = str
Operand: TypeAlias = str
OperatorStack: TypeAlias = list[Operator]
OperandStack: TypeAlias = list[Operand]


def _is_operand(symbol: str) -> bool:
	return len(symbol) == 1 and symbol.upper() in __operands


def _is_operator(symbol: str) -> bool:
	return symbol in __operators


def _pop_operator(operator_stack: OperatorStack, operator: Operator) \
	-> Optional[Operator]:
	# i. Pop operator on the stack that
	#       a. is above the most recently scanned left parenthesis, and
	#       b. has precedence higher than or is a right-associative
	#          operator of equal precedence to that of the new operator
	#          symbol.

	if len(operator_stack) == 0:
		return None

	stack_operator = operator_stack[-1]
	if stack_operator not in __operators:
		return None

	if __precedence[stack_operator] > __precedence[operator]:
		return operator_stack.pop()

	if __precedence[stack_operator] == __precedence[operator]:
		if operator in __left_associative_operators:
			return operator_stack.pop()

	return None


def postfix_to_infix(postfix: str) -> str:
	"""Return the infix representation of the postfix expression. Result may
	have redundant parentheses."""
	
	operand_stack: OperandStack = []
	
	for c in postfix:
		if c in __operators:
			right_operand = operand_stack.pop()
			left_operand = operand_stack.pop()
			operand_stack.append("(" + left_operand + c + right_operand + ")")
		else:
			operand_stack.append(c)
	
	return operand_stack.pop()[1:-1]


def postfix_to_prefix(postfix: str) -> str:
	"""Return prefix representation of the postfix expression."""
	
	operand_stack: OperandStack = []
	
	for symbol in postfix:
		if _is_operand(symbol):
			operand_stack.append(symbol)
		else:
			operand_1 = operand_stack.pop()
			operand_2 = operand_stack.pop()
			operand_stack.append(symbol + operand_2 + operand_1)
	
	return operand_stack.pop()


def prefix_to_postfix(prefix: str) -> str:
	"""Return postfix representation of the prefix expression."""

	operand_stack: OperandStack = []
	
	for symbol in reversed(prefix):
		if _is_operand(symbol):
			operand_stack.append(symbol)
		else:
			operand_1 = operand_stack.pop()
			operand_2 = operand_stack.pop()
			operand_stack.append(symbol + operand_2 + operand_1)
	
	return operand_stack.pop()[::-1]


def infix_to_postfix(infix: str) -> str:
	"""Return postfix representation of the infix expression."""

	postfix_list: list[str] = []
	operator_stack: OperatorStack = []
	
	# Scan the input string (infix notation) from left to right. One pass is
	# sufficient.
	for symbol in infix:
		# If the next symbol scanned is an operand, it may be immediately
		# appended to the postfix string.
		if _is_operand(symbol):
			# print(f"1. appending operand = {symbol}")
			postfix_list.append(symbol)
		
		# If the next symbol is an operator,
		# i. Pop and append to the postfix string every operator on the stack
		#    that
		#       a. is above the most recently scanned left parenthesis, and
		#       b. has precedence higher than or is a right-associative
		#          operator of equal precedence to that of the new operator
		#          symbol.
		# ii. Push the new operator onto the stack.
		elif _is_operator(symbol):
			while operator := _pop_operator(operator_stack, symbol):
				postfix_list.append(operator)
			operator_stack.append(symbol)
		
		# When a left parenthesis is seen, it must be pushed onto the stack.
		elif symbol == "(":
			operator_stack.append(symbol)
		
		# When a right parenthesis is seen, all operators down to the most
		# recently scanned left parenthesis must be popped and appended to the
		# postfix string. Furthermore, this pair of parentheses must be
		# discarded.
		elif symbol == ")":
			while len(operator_stack) \
					and (popped_operator := operator_stack.pop()) != "(":
				postfix_list.append(popped_operator)
	
	# When the infix string is completely scanned, the stack may still contain
	# some operators. [Why are there no parentheses on the stack at this
	# point?] All the remaining operators should be popped and appended to the
	# postfix string.
	while len(operator_stack):
		operator = operator_stack.pop()
		postfix_list.append(operator)
	
	return ''.join(postfix_list)


def infix_to_prefix(infix: str) -> str:
	"""Return the prefix representation of the infix expression (supports
	operators: ^, *, /, + and -."""

	return postfix_to_prefix(infix_to_postfix(infix))


def prefix_to_infix(prefix: str) -> str:
	"""Return infix representation of the prefix expression."""

	return postfix_to_infix(prefix_to_postfix(prefix))
