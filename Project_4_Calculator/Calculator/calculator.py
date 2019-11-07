import numbers
import random
import numpy
import re


class Container:
    """Superclass for stack and queue"""

    def __init__(self):
        """Constructs a list"""
        self.items = []

    def size(self) -> int:
        """Returns the size of list"""
        return len(self.items)

    def is_empty(self) -> bool:
        """Returns true if list is empty"""
        return self.size() == 0

    def push(self, item):
        """Adds element to the end of the list"""
        self.items.append(item)

    def pop(self):
        """Removes and return element at given index"""
        raise NotImplementedError   # Dette konvensjon når lager klasse som imp. senere?

    def peek(self):
        """Return the given element without removing it"""
        raise NotImplementedError


class Queue(Container):
    """append og list[0] peek for queue. pop(0)"""

    def pop(self):
        """removes and return the first element of the list"""
        assert not self.is_empty()
        return self.items.pop(0)

    def peek(self):
        """returns the first element of the list"""
        assert not self.is_empty()
        return self.items[0]


class Stack(Container):
    """append og pop, list[-1] gir bakerste element(peek)"""

    def pop(self):
        """removes and return the last element of the list"""
        assert not self.is_empty()
        return self.items.pop(-1)

    def peek(self):
        """returns the last element of the list"""
        assert not self.is_empty()
        return self.items[-1]


class Function:
    """Gets the abilities to given function"""

    def __init__(self, func):
        """saves the function-type"""
        self.func = func

    def execute(self, element, debug=True):
        """Exexutes the function on a number"""
        if not isinstance(element, numbers.Number):
            raise TypeError("Cannot execute func if element is not a number")
        result = self.func(element)
        if debug is True:
            print(
                "Function: " +
                self.func.__name__ +
                "({:f}) = {:f}".format(
                    element,
                    result))
        return result

    def __str__(self):
        return self.func.__name__


class Operator:
    """Gets the ability to given operator"""

    def __init__(self, operation):
        """Gets the operator-type and strength of it"""
        self.operation = operation
        self.strength = -1
        if operation == numpy.add or operation == numpy.subtract:
            self.strength = 0
        elif operation == numpy.multiply or operation == numpy.divide:
            self.strength = 1

    def execute(self, first, second, debug=True):
        """Takes in two elements and execute given operation"""
        if not (isinstance(first, numbers.Number)
                or isinstance(second, numbers.Number)):
            raise TypeError("Cannot execute func if element is not a number")
        result = self.operation(first, second)
        if debug is True:
            print("Operator: " +
                  self.operation.__name__ +
                  "({:f} {:s} {:f}) = {:f}".format(
                      first, self.operation.__name__, second,
                      result))
        return result


class Calculator:
    """A calculator"""

    def __init__(self):
        """Defines all the functions a calculator has and RPN-represented equation"""
        self.functions = {"EXP": Function(numpy.exp),
                          "LOG": Function(numpy.log),
                          "SIN": Function(numpy.sin),
                          "COS": Function(numpy.cos),
                          "SQRT": Function(numpy.sqrt)}

        self.operators = {"PLUSS": Operator(numpy.add),
                          "GANGE": Operator(numpy.multiply),
                          "DELE": Operator(numpy.divide),
                          "MINUS": Operator(numpy.subtract)}
        self.output_queue = Queue()

    def add_to_queue(self, value):
        """Adds a element to output_queue"""
        self.output_queue.push(value)

    def solve_RPN(self):  # Mulig cleare outputqueue etter utregning
        """Solves the equation in outputqueue"""
        temporary_stack = Stack()
        for element in self.output_queue.items:
            if isinstance(element, numbers.Number):
                temporary_stack.push(element)
            elif isinstance(element, Function):
                value = temporary_stack.pop()
                temporary_stack.push(element.execute(value))
            elif isinstance(element, Operator):
                a = temporary_stack.pop()
                b = temporary_stack.pop()
                temporary_stack.push(element.execute(b, a))
        return temporary_stack.pop()

    def parse_to_RPN(self, input_queue: Queue):
        """sorts a queue so the operations on a equation is in right order"""
        output_queue = Queue()
        operator_stack = Stack()
        for element in input_queue.items:
            if isinstance(element, numbers.Number):
                output_queue.push(element)
            elif isinstance(element, Function) or element == '(':
                operator_stack.push(element)
            elif element == ')':
                for i in operator_stack.items:
                    check = operator_stack.peek()
                    if check != '(':
                        output_queue.push(operator_stack.pop())
                    else:
                        break
                operator_stack.pop()
            elif isinstance(element, Operator):
                while not operator_stack.is_empty() and operator_stack.items[-1] != '(' and \
                        not isinstance(operator_stack.items[-1], Function) \
                        and element.strength < operator_stack.items[-1].strength:
                    output_queue.push(operator_stack.pop())
                operator_stack.push(element)
        while not operator_stack.is_empty():
            output_queue.push(operator_stack.pop())
        return output_queue

    def set_output_queue(self, input: Queue):
        """sets the outputqueue to input"""
        self.output_queue = input

    def __str__(self):
        """Overwrites the stringmethod to print the list of items in outputqueue"""
        return str(self.output_queue.items)

    def string_to_parse(self, text: str):
        """Takes in a string and converts it to a queue with elements from string"""
        text = text.replace(" ", "").upper()
        parsed_list = []
        functargets = "|".join(["^" + func for func in self.functions.keys()])
        optargets = "|".join(["^" + op for op in self.operators.keys()])

        targets = functargets + "|" + optargets
        values = "^[-0123456789.]+"
        while len(text) != 0:
            temp_val = re.search(values, text)
            if temp_val is not None:
                parsed_list.append(float(temp_val.group(0)))
                text = text[temp_val.end(0):]
            temp_targ = re.search(targets, text)
            if temp_targ is not None:
                if re.search(functargets, text) is not None:
                    temp_targ = temp_targ.group(0)
                    temp_targ = self.functions[temp_targ]
                elif re.search(optargets, text) is not None:
                    temp_targ = temp_targ.group(0)
                    temp_targ = self.operators[temp_targ]
                parsed_list.append(temp_targ)
                text = text[re.search(targets, text).end(0):]
            if text[0] == "(":
                parsed_list.append("(")
                text = text[1:]
            if text[0] == ")":
                parsed_list.append(")")
                text = text[1:]
        queue = Queue()
        queue.items = parsed_list
        return queue

    def calculate_expression(self, text):
        """Take use of all the functions and calculates the input"""
        self.output_queue.items.clear()
        parse = self.string_to_parse(text)
        rpn = self.parse_to_RPN(parse)
        self.set_output_queue(rpn)
        return self.solve_RPN()


def main():
    calc = Calculator()
    print(calc.calculate_expression("((15 dele (7minus (1 pluss 1)))gange3)minus (2 PLUSS (1pluss 1))"))
    print(calc.calculate_expression("exp(1 pluss 2 gange 3pluss 4)"))
    print(calc.calculate_expression("1 pluss exp (2)"))


    #print(calc.string_to_parse("((15 dele (7minus (1 pluss 1)))gange3)minus (2 PLUSS (1pluss 1))").items)

main()
