"""Conversion from infix to prefix and postfix using stack."""
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum, auto
from operator import mul, truediv, add, sub, pow
from typing import TypeAlias, Optional

Operator: TypeAlias = str
EvalValue: TypeAlias = int | float | complex
Precedence: TypeAlias = int
PyOperator: TypeAlias = Callable[[EvalValue, EvalValue], EvalValue]


class Associativity(Enum):
	"""Right assoc: A~B~C=(A~B)~C, or left assoc: A~B~C=A~(B~C) (where all ~
	are operators with equal precedence)."""
	
	RIGHT = auto()
	LEFT = auto()
	

@dataclass
class OperatorProps:
	"""Properties of operators"""
	
	precedence: int
	python_operator: PyOperator
	associativity: Associativity


Operators: TypeAlias = dict[Operator, OperatorProps]
OperatorStack: TypeAlias = list[Operator]
Operand: TypeAlias = str
OperandStack: TypeAlias = list[Operand]
PopFunction: TypeAlias = Callable[[OperatorStack, Operator], Optional[Operator]]
OperandsFunc: TypeAlias = Callable[[OperatorStack], list[EvalValue]]

__power_operator = "**"   # Choose "**" or "^"
__operators = \
	{__power_operator: OperatorProps(4, pow, Associativity.RIGHT),
	 "*": OperatorProps(3, mul, Associativity.LEFT),
	 "/": OperatorProps(3, truediv, Associativity.LEFT),
	 "+": OperatorProps(2, add, Associativity.LEFT),
	 "-": OperatorProps(2, sub, Associativity.LEFT)}


def _python_operator(operator: Operator) -> PyOperator:
	return __operators[operator].python_operator


def _precedence(operator: Operator) -> int:
	return __operators[operator].precedence


def _associativity(operator: Operator) -> Associativity:
	return __operators[operator].associativity


def _is_operator(symbol: str) -> bool:
	return symbol in __operators


def _is_float(x: str) -> Optional[float]:
	try:
		x_as_float = float(x)
	except (TypeError, ValueError):
		return None
	else:
		return x_as_float


def _is_int(x: str) -> Optional[int]:
	try:
		a = float(x)
		b = int(a)
	except (TypeError, ValueError):
		return None
	else:
		return b if a == b else None


def _to_number(num_as_str: str) -> EvalValue:
	return _is_int(num_as_str) or _is_float(num_as_str) or complex(num_as_str)


def _get_operands(operand_stack: OperandStack, nr: int) -> list[EvalValue]:
	return [_to_number(operand_stack.pop()) for _ in range(nr)]


def _prefix_operands(operand_stack: OperandStack) -> list[EvalValue]:
	return _get_operands(operand_stack, 2)


def _prostfix_operands(operand_stack: OperandStack) -> list[EvalValue]:
	return _get_operands(operand_stack, 2)[::-1]


def _eval_polish(polish: list[str], operands_func: OperandsFunc) -> EvalValue:
	"""Return the value of evaluating the postfix expression"""

	operand_stack: OperandStack = []
	
	for symbol in polish:
		if _is_operator(symbol):
			operand_stack.append(
				str(_python_operator(symbol)(*operands_func(operand_stack))))
		else:
			operand_stack.append(symbol)
	return _to_number(operand_stack.pop())


def eval_postfix(postfix: str) -> EvalValue:
	"""Return the value of evaluating the postfix expression"""

	return _eval_polish(postfix.split(), _prostfix_operands)


def eval_prefix(prefix: str) -> int | float | complex:
	"""Return the value of evaluating the postfix expression"""

	return _eval_polish(prefix.split()[::-1], _prefix_operands)

	
# def _pop_any(operator_stack: OperatorStack, new_operator: Operator,
# 			 associative_ops: Operators) -> Optional[Operator]:
def _pop_any(operator_stack: OperatorStack, new_operator: Operator,
             associativity: Associativity) -> Optional[Operator]:
	"""Pop and return from *operator_stack* if top of stack is an operator that
	1. has higher precedence than *operator*, or
	2. has equal precedence than *operator* and *operator* is in the set of
	   associate operators."""
	
	if len(operator_stack) \
		and _is_operator(stack_operator := operator_stack[-1]):

		if _precedence(stack_operator) > _precedence(new_operator):
			return operator_stack.pop()
		
		if _precedence(stack_operator) == _precedence(new_operator) \
				and _associativity(new_operator) == associativity:
			return operator_stack.pop()

	return None


def _pop_postfix(operator_stack: OperatorStack, new_operator: Operator) \
		-> Optional[Operator]:
	
	return _pop_any(operator_stack, new_operator, Associativity.LEFT)


def _pop_prefix(operator_stack: OperatorStack, new_operator: Operator) \
		-> Optional[Operator]:
	
	return _pop_any(operator_stack, new_operator, Associativity.RIGHT)


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
	
	for symbol in postfix.split():
		if _is_operator(symbol):
			right_operand = operand_stack.pop()
			left_operand = operand_stack.pop()
			operand_stack.append("(" + left_operand + " "
								 + symbol
								 + " " + right_operand + ")")
		else:
			operand_stack.append(symbol)
	
	return ' '.join(operand_stack)[1:-1]


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
	
	for symbol in postfix.split():
		if _is_operator(symbol):
			right_operand = operand_stack.pop()
			left_operand = operand_stack.pop()
			operand_stack.append(symbol
			                     + " " + left_operand
			                     + " " + right_operand)
		else:
			operand_stack.append(symbol)
	
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
	
	for symbol in infix.split():
		if _is_operator(symbol):
			while operator := pop_function(operator_stack, symbol):
				postfix_list.append(operator)
			operator_stack.append(symbol)
		elif symbol == "(":
			operator_stack.append(symbol)
		elif symbol == ")":
			while (len(operator_stack)
				   and (popped_operator := operator_stack.pop()) != "("):
				postfix_list.append(popped_operator)
		else:
			postfix_list.append(symbol)

	while len(operator_stack):
		postfix_list.append(operator_stack.pop())
	
	return ' '.join(postfix_list)


def infix_to_prefix(infix: str) -> str:
	"""Using a few 'tricks' is faster than converting infix to postfix and then
	postfix to prefix...'"""
	
	return _infix_to_postfix(_swap_chars(infix, "(", ")")[::-1],
							 pop_function=_pop_prefix)[::-1]


def infix_to_postfix(infix: str) -> str:
	"""After introducing bla"""
	
	return _infix_to_postfix(infix, pop_function=_pop_postfix)


if __name__ == "__main__":
	
	def _main() -> None:
		# print(eval_postfix("3 4 +"))
		# print(eval_postfix("3 4 -"))
		# print(eval_postfix("3 4 *"))
		# print(eval_postfix("3 4 /"))
		# print(eval_postfix("3 4 **"))
		example = "3 + ( 3 - 2 ) + 2 ** 3 ** 2"
		print(f"{example = }")
	
		postfix = infix_to_postfix(example)
		print(f"{postfix = }")
		eval_post = eval_postfix(postfix)
		print(f"{eval_post = }")
		
		prefix = infix_to_prefix(example)
		print(f"{prefix = }")
		eval_pre = eval_prefix(prefix)
		# print(type(eval_pref))
		print(f"{eval_pre = }")
	
	_main()
