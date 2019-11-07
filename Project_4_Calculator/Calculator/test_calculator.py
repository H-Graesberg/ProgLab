import unittest
import numpy
import numbers
import Project_4.calculator as calc


class CalculatorTestCase(unittest.TestCase):

    def setUp(self) -> None:

        self.queue = calc.Queue()
        self.stack = calc.Stack()
        self.counter = 0
        for i in range(1, 6):
            self.queue.push(i)
            self.stack.push(i)

        self.exponential_func = calc.Function(numpy.exp)
        self.sin_func = calc.Function(numpy.sin)
        self.absolute = calc.Function(numpy.abs)

        self.added = calc.Operator(numpy.add)
        self.sub = calc.Operator(numpy.subtract)
        self.divide = calc.Operator(numpy.divide)
        self.multi = calc.Operator(numpy.multiply)

        self.calculator = calc.Calculator()

    def tearDown(self) -> None:
        del self.stack, self.queue, self.counter

        del self.exponential_func, self.sin_func, self.absolute

        del self.added, self.sub, self.divide, self.multi

    def test_stack(self):
        print("----- Test for Stack -----\n\n")
        self.assertEqual(5, self.stack.peek())
        while not self.stack.is_empty():
            self.assertTrue(self.stack.peek(), 5 - self.counter)
            self.assertTrue(self.stack.size(), 5 - self.counter)
            self.counter += 1
            print("Element fjernet fra stack: ", self.stack.pop(),
                  "\nElementer igjen: ", self.stack.size())
        self.assertEqual(self.stack.is_empty(), True)

    def test_queue(self):
        print("----- Test for Queue -----\n\n")
        self.assertEqual(1, self.queue.peek())
        while not self.queue.is_empty():
            self.assertTrue(self.queue.peek(), self.counter + 1)
            self.assertTrue(self.queue.size(), 5 - self.counter)
            self.counter += 1
            print("Element fjernet fra queue: ", self.queue.pop(),
                  "\nElementer igjen: ", self.queue.size())
        self.assertEqual(self.queue.is_empty(), True)

    def test_function(self):
        print("----- Test for Function -----\n\n")
        self.assertAlmostEqual(self.exponential_func.execute(1), 2.71, 1)
        self.assertEqual(self.sin_func.execute(0), 0)
        self.assertEqual(self.absolute.execute(-12), 12)
        self.assertEqual(
            self.exponential_func.execute(
                self.sin_func.execute(0)), 1)

    def test_operator(self):
        self.assertEqual(self.added.execute(9, 0), 9)
        self.assertEqual(self.sub.execute(9, 3), 6)
        self.assertEqual(self.divide.execute(9, 3), 3)
        self.assertEqual(self.multi.execute(9, 3), 27)

        self.assertEqual(self.added.strength, 0)
        self.assertEqual(self.sub.strength, 0)
        self.assertEqual(self.divide.strength, 1)
        self.assertEqual(self.multi.strength, 1)

        self.assertEqual(self.sub.execute(1, self.multi.execute(2, 3)), -5)

    def test_calculator(self):
        self.assertAlmostEqual(self.calculator.functions["EXP"].execute(
            self.calculator.operators["PLUSS"].execute(
                1, self.calculator.operators["GANGE"].execute(2, 3))), 1096.6, 1)

    def test_calculator_RPN(self):
        self.calculator.output_queue.items.clear()
        self.calculator.output_queue.push(1)
        self.calculator.output_queue.push(2)
        self.calculator.output_queue.push(3)

        self.calculator.output_queue.push(self.calculator.operators["GANGE"])
        self.calculator.output_queue.push(self.calculator.operators["PLUSS"])
        self.calculator.output_queue.push(self.calculator.functions["EXP"])

        self.assertAlmostEqual(self.calculator.solve_RPN(), 1096.6, 1)

    def test_parse_to_RPN(self):
        self.calculator.output_queue.items.clear()
        self.calculator.output_queue.push(self.calculator.functions["EXP"])
        self.calculator.output_queue.push('(')
        self.calculator.output_queue.push(1)
        self.calculator.output_queue.push(self.calculator.operators["PLUSS"])
        self.calculator.output_queue.push(2)
        self.calculator.output_queue.push(self.calculator.operators["GANGE"])
        self.calculator.output_queue.push(3)
        self.calculator.output_queue.push(')')
        self.calculator.output_queue = self.calculator.parse_to_RPN(self.calculator.output_queue)
        self.assertAlmostEqual(self.calculator.solve_RPN(), 1096.6, 1)

    def test_complete_calculator(self):
        self.assertEqual(self.calculator.calculate_expression("((15 dele (7minus (1 pluss 1)))gange3)minus (2 PLUSS (1pluss 1))"), 5)



if __name__ == '__main__':
    unittest.main()
