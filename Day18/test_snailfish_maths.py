import unittest
from day_18 import parse_pair, add_all, read_numbers, reduce_number, get_magnitude, Child
from io import StringIO


class TestDay18(unittest.TestCase):
    def test_explode_pair(self):
        number = parse_pair(StringIO("[[[[[9,8],1],2],3],4]"), None)
        number.get_child(Child.LEFT).get_child(Child.LEFT).get_child(Child.LEFT).get_child(Child.LEFT).explode(4)
        self.assertEqual("[[[[0,9],2],3],4]", number.__repr__())

        number = parse_pair(StringIO("[7,[6,[5,[4,[3,2]]]]]"), None)
        number.get_child(Child.RIGHT).get_child(Child.RIGHT).get_child(Child.RIGHT).get_child(Child.RIGHT).explode(4)
        self.assertEqual("[7,[6,[5,[7,0]]]]", number.__repr__())

        number = parse_pair(StringIO("[[6,[5,[4,[3,2]]]],1]"), None)
        number.get_child(Child.LEFT).get_child(Child.RIGHT).get_child(Child.RIGHT).get_child(Child.RIGHT).explode(4)
        self.assertEqual("[[6,[5,[7,0]]],3]", number.__repr__())

        number = parse_pair(StringIO("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]"), None)
        number.get_child(Child.LEFT).get_child(Child.RIGHT).get_child(Child.RIGHT).get_child(Child.RIGHT).explode(4)
        self.assertEqual("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]", number.__repr__())

        number = parse_pair(StringIO("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]"), None)
        number.get_child(Child.RIGHT).get_child(Child.RIGHT).get_child(Child.RIGHT).get_child(Child.RIGHT).explode(4)
        self.assertEqual("[[3,[2,[8,0]]],[9,[5,[7,0]]]]", number.__repr__())

    def test_add(self):
        numbers = read_numbers(StringIO("[1,1]\n[2,2]\n[3,3]\n[4,4]"))
        self.assertEqual("[[[[1,1],[2,2]],[3,3]],[4,4]]", add_all(numbers).__repr__())

        numbers = read_numbers(StringIO("[1,1]\n[2,2]\n[3,3]\n[4,4]\n[5,5]"))
        self.assertEqual("[[[[3,0],[5,3]],[4,4]],[5,5]]", add_all(numbers).__repr__())

        numbers = read_numbers(StringIO("[1,1]\n[2,2]\n[3,3]\n[4,4]\n[5,5]\n[6,6]"))
        self.assertEqual("[[[[5,0],[7,4]],[5,5]],[6,6]]", add_all(numbers).__repr__())

    def test_reduce(self):
        number = parse_pair(StringIO("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]"), None)
        reduce_number(number)
        self.assertEqual("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]", number.__repr__())

    def test_add_2(self):
        numbers = read_numbers(StringIO("[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]\n[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]"))
        self.assertEqual("[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]", add_all(numbers).__repr__())

    def test_add_3(self):
        numbers = read_numbers(StringIO("[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]\n"
                                        "[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]"))
        self.assertEqual("[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]", add_all(numbers).__repr__())

    def test_add_4(self):
        numbers = read_numbers(StringIO("[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]\n"
                                        "[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]"))
        self.assertEqual("[[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]", add_all(numbers).__repr__())

    def test_add_5(self):
        numbers = read_numbers(StringIO("[[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]\n"
                                        "[7,[5,[[3,8],[1,4]]]]"))
        self.assertEqual("[[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]]", add_all(numbers).__repr__())

    def test_add_6(self):
        numbers = read_numbers(StringIO("[[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]]\n"
                                        "[[2,[2,2]],[8,[8,1]]]"))
        self.assertEqual("[[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]]",
                         add_all(numbers).__repr__())

    def test_add_7(self):
        numbers = read_numbers(StringIO("[[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]]\n"
                                        "[2,9]"))
        self.assertEqual("[[[[6,6],[7,7]],[[0,7],[7,7]]],[[[5,5],[5,6]],9]]",
                         add_all(numbers).__repr__())

    def test_add_8(self):
        numbers = read_numbers(StringIO("[[[[6,6],[7,7]],[[0,7],[7,7]]],[[[5,5],[5,6]],9]]\n"
                                        "[1,[[[9,3],9],[[9,0],[0,7]]]]"))
        self.assertEqual("[[[[7,8],[6,7]],[[6,8],[0,8]]],[[[7,7],[5,0]],[[5,5],[5,6]]]]",
                         add_all(numbers).__repr__())

    def test_add_9(self):
        numbers = read_numbers(StringIO("[[[[7,8],[6,7]],[[6,8],[0,8]]],[[[7,7],[5,0]],[[5,5],[5,6]]]]\n"
                                        "[[[5,[7,4]],7],1]"))
        self.assertEqual("[[[[7,7],[7,7]],[[8,7],[8,7]]],[[[7,0],[7,7]],9]]",
                         add_all(numbers).__repr__())

    def test_add_10(self):
        numbers = read_numbers(StringIO("[[[[7,7],[7,7]],[[8,7],[8,7]]],[[[7,0],[7,7]],9]]\n"
                                        "[[[[4,2],2],6],[8,7]]"))
        self.assertEqual("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]",
                         add_all(numbers).__repr__())

    def test_larger_add(self):
        numbers_input = "[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]\n" \
                        "[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]\n" \
                        "[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]\n" \
                        "[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]\n" \
                        "[7,[5,[[3,8],[1,4]]]]\n" \
                        "[[2,[2,2]],[8,[8,1]]]\n" \
                        "[2,9]\n" \
                        "[1,[[[9,3],9],[[9,0],[0,7]]]]\n" \
                        "[[[5,[7,4]],7],1]\n" \
                        "[[[[4,2],2],6],[8,7]]"
        numbers = read_numbers(StringIO(numbers_input))
        self.assertEqual("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]", add_all(numbers).__repr__())

    def test_magnitude(self):
        magnitude = get_magnitude(parse_pair(StringIO("[9,1]"), None))
        self.assertEqual(29, magnitude)

        magnitude = get_magnitude(parse_pair(StringIO("[[1,2],[[3,4],5]]"), None))
        self.assertEqual(143, magnitude)

        magnitude = get_magnitude(parse_pair(StringIO("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"), None))
        self.assertEqual(1384, magnitude)

        magnitude = get_magnitude(parse_pair(StringIO("[[[[1,1],[2,2]],[3,3]],[4,4]]"), None))
        self.assertEqual(445, magnitude)

        magnitude = get_magnitude(parse_pair(StringIO("[[[[3,0],[5,3]],[4,4]],[5,5]]"), None))
        self.assertEqual(791, magnitude)

        magnitude = get_magnitude(parse_pair(StringIO("[[[[5,0],[7,4]],[5,5]],[6,6]]"), None))
        self.assertEqual(1137, magnitude)

        magnitude = get_magnitude(parse_pair(StringIO("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]"), None))
        self.assertEqual(3488, magnitude)


if __name__ == '__main__':
    unittest.main()
