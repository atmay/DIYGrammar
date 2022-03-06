"""
Basic recursive descent parser for * and + arithmetical operations
"""

from typing import List, Optional

example = [
    ["3", '3'],
    ["5+7", ['5', '+', '7']],
    ["5+7+9", ['5', '+', ['7', '+', '9']]],

    ["5*7", ['5', '*', '7']],
    ["5*7+3", [['5', '*', '7'], '+', '3']],
    ["5+7*3", ['5', '+', ['7', '*', '3']]],
    ["8*(7+4)+2", [['8', '*', ['7', '+', '4']], '+', '2']]
]

"""
Grammar rules:
E = E + T
E = T
T = T * F
T = F
F = ( E )
F = n


After getting rid of left recursion:
exp = mul | sum | n
mul = n * exp
sum = n + exp

mul = n mul1
mul1 = * n mul1
mul1 = #

sum = n sum1
sum1 = + n sum1
sum1 = #


Reverse Polish notation for rules
E = T E1
E1 = + T E1
E1 = #

T = F T1
T1 = * F T1
T1 = #

F = ( E )
F = n
"""


def parse(expr: str) -> List:
    tokens = list(expr)
    # return parse_expression(tokens=tokens)
    return E(tokens)


'''
E = T E1
E1 = + T E1 | #

T = F T1
T1 = * F T1
T1 = #

F = ( E )
F = n
'''


def E(tokens):
    """E = T E1"""
    _T = T(tokens)
    _E1 = E1(tokens)
    return [_T, _E1]


def E1(tokens):
    """E1 = + T E1 | #"""
    if len(tokens) == 0:
        return None
    if tokens[0] == '+':
        operand = tokens.pop(0)
        _T = T(tokens)
        res = [operand, _T]
        _E1 = E1(tokens)
        if _E1:
            res += _E1
        else:
            res.append(_E1)
        return res
    return None


def T(tokens):
    """T = F T1"""
    _F = F(tokens)
    _T1 = T1(tokens)
    return [_F, _T1]


def T1(tokens):
    """
    T1 = * F T1
    T1 = #
    """
    if len(tokens) == 0:
        return None
    if tokens[0] == '*':
        operand = tokens.pop(0)
        _F = F(tokens)
        res = [operand, _F]
        _T1 = T1(tokens)
        if _T1:
            res += _T1
        else:
            res.append(_T1)
        return res
    return None


def F(tokens):
    """
    F = ( E )
    F = n
    """
    if len(tokens) == 0:
        return None
    first_symbol: str = tokens[0]
    if first_symbol == '(':
        tokens.pop(0)
        _E = E(tokens)
        bracket_closing = tokens.pop(0)
        if bracket_closing == ')':
            return _E
        else:
            raise ValueError('Wrong expression. Missing bracket.')
    if first_symbol.isdigit():
        return tokens.pop(0)
    return None


def parse_expression(tokens: List) -> Optional[List]:
    """exp = mul | sum | n"""
    if tree := parse_mul(tokens=tokens):
        return tree
    if tree := parse_sum(tokens=tokens):
        return tree
    if (result := tokens[0]).isdigit():
        return result
    return None


def parse_mul(tokens: List) -> Optional[List]:
    if len(tokens) < 3:
        return None
    a: str = tokens[0]
    b: str = tokens[1]
    if a.isdigit() and b == '*':
        return [a, b, parse_expression(tokens[2:])]
    return None


def parse_sum(tokens: List) -> Optional[List]:
    # sum = n + exp
    if len(tokens) < 3:
        return None
    a: str = tokens[0]
    b: str = tokens[1]
    if a.isdigit() and b == '+':
        #       n  +  exp
        return [a, b, parse_expression(tokens[2:])]
    return None


def clear_none(ast: List) -> List:
    if isinstance(ast, list):
        if None in ast:
            ast.remove(None)
        for i in range(len(ast)):
            ast[i] = clear_none(ast[i])
    return ast


def app():
    for i in example:
        sample = i[0]
        res = clear_none(parse(sample))
        valid_result = i[1]
        print(f'Sample: {sample}\n'
              f'Valid:  {valid_result}\n'
              f'Result: {res}\n'
              f'        {res == valid_result}\n'
              f'*************')


if __name__ == '__main__':
    app()
