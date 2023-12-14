def repl():
    while True:
        try:
            print("Type 'exit' to exit Calculator")
            text = input("calc> ")
            if text.strip().lower() == 'exit':
                break
            result = interpret(text)
            print(result)
        except Exception as e:
            print(f"Error: {e}")


def interpret(text):
    tokens = tokenize(text)
    ast = parse(tokens)
    return evaluate(ast)


def tokenize(text):
    tokens = []
    i = 0
    while i < len(text):
        if text[i].isdigit() or text[i] == '.':
            num = text[i]
            i += 1
            while i < len(text) and (text[i].isdigit() or text[i] == '.'):
                num += text[i]
                i += 1
            tokens.append(('NUMBER', float(num)))
        elif text[i] in '+-*/':
            tokens.append((text[i], text[i]))
            i += 1
        elif text[i] in '()':
            tokens.append((text[i], text[i]))
            i += 1
        elif text[i] == ' ':
            i += 1
        else:
            raise ValueError(f"Unknown character: {text[i]}")
    return tokens


def parse(tokens):
    def parse_expression(index):
        node, index = parse_term(index)
        while index < len(tokens) and tokens[index][0] in '+-':
            op = tokens[index][0]
            right_node, index = parse_term(index + 1)
            node = (op, node, right_node)
        return node, index

    def parse_term(index):
        node, index = parse_factor(index)
        while index < len(tokens) and tokens[index][0] in '*/':
            op = tokens[index][0]
            right_node, index = parse_factor(index + 1)
            node = (op, node, right_node)
        return node, index

    def parse_factor(index):
        token, value = tokens[index]
        if token == 'NUMBER':
            return value, index + 1
        elif token == '(':
            node, index = parse_expression(index + 1)
            if tokens[index][0] != ')':
                raise ValueError("Mismatched parenthesis")
            return node, index + 1
        else:
            raise ValueError(f"Unexpected token: {token}")

    ast, index = parse_expression(0)
    if index != len(tokens):
        raise ValueError("Invalid syntax")
    return ast


def evaluate(node):
    if isinstance(node, tuple):
        op, left, right = node
        if op == '+':
            return evaluate(left) + evaluate(right)
        elif op == '-':
            return evaluate(left) - evaluate(right)
        elif op == '*':
            return evaluate(left) * evaluate(right)
        elif op == '/':
            return evaluate(left) / evaluate(right)
    else:  # node is a number
        return node


if __name__ == "__main__":
    repl()
