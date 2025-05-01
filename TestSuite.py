import unittest
from TestUtils import TestUtils


class TestSymbolTable(unittest.TestCase):
    def test_0(self):
        input = ["INSERT a1 number", "INSERT b2 string"]
        expected = ["success", "success"]

        self.assertTrue(TestUtils.check(input, expected, 100))

    def test_1(self):
        input = ["INSERT x number", "INSERT y string", "INSERT x string"]
        expected = ["Redeclared: INSERT x string"]

        self.assertTrue(TestUtils.check(input, expected, 101))

    def test_2(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "ASSIGN x 15",
            "ASSIGN y 17",
            "ASSIGN x 'abc'",
        ]
        expected = ["TypeMismatch: ASSIGN y 17"]

        self.assertTrue(TestUtils.check(input, expected, 102))

    def test_3(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "BEGIN",
            "INSERT x number",
            "BEGIN",
            "INSERT y string",
            "END",
            "END",
        ]
        expected = ["success", "success", "success", "success"]

        self.assertTrue(TestUtils.check(input, expected, 103))

    def test_4(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "BEGIN",
            "INSERT x number",
            "LOOKUP x",
            "LOOKUP y",
            "END",
        ]
        expected = ["success", "success", "success", "1", "0"]

        self.assertTrue(TestUtils.check(input, expected, 104))

    def test_5(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "BEGIN",
            "INSERT x number",
            "INSERT z number",
            "PRINT",
            "END",
        ]
        expected = ["success", "success", "success", "success", "y//0 x//1 z//1"]

        self.assertTrue(TestUtils.check(input, expected, 105))

    def test_6(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "BEGIN",
            "INSERT x number",
            "INSERT z number",
            "RPRINT",
            "END",
        ]
        expected = ["success", "success", "success", "success", "z//1 x//1 y//0"]

        self.assertTrue(TestUtils.check(input, expected, 106))

    def test_7(self):
        input = ["INSERT x string", "ASSIGN x allocate"]
        expected = ["Invalid: ASSIGN x allocate"]

        self.assertTrue(TestUtils.check(input, expected, 107))

    def test_8(self):
        input = ["   INSERT x number"]
        expected = ["Invalid:    INSERT x number"]

        self.assertTrue(TestUtils.check(input, expected, 108))

    def test_9(self):
        input = [
            "INSERT a number",
            "ASSIGN a  1"
        ]
        expected = ["Invalid: ASSIGN a  1"]

        self.assertTrue(TestUtils.check(input, expected, 109))

    def test_10(self):
        input = [
            "INSERT a number",
            "INSERT b number",
            "BEGIN",
            "INSERT c string",
            "END",
            "INSERT d string",
            "BEGIN",
            "PRINT",
            "END",
        ]
        expected = ["success", "success", "success", "success", "a//0 b//0 d//0"]

        self.assertTrue(TestUtils.check(input, expected, 110))

    def test_11(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "BEGIN",
            "INSERT x number",
            "LOOKUP x",
            "LOOKUP y"
        ]
        expected = ["UnclosedBlock: 1"]

        self.assertTrue(TestUtils.check(input, expected, 111))

    def test_12(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "BEGIN",
            "INSERT x number",
            "LOOKUP x",
            "LOOKUP y",
            "END",
            "END"
        ]
        expected = ["UnknownBlock"]

        self.assertTrue(TestUtils.check(input, expected, 112))

    def test_13(self):
        input = [
            "BEGIN",
            "BEGIN",
            "BEGIN",
            "INSERT a number",
            "END",
            "INSERT b number",
            "ASSIGN a b",
            "END",
            "RPRINT"
        ]
        expected = ["Invalid: ASSIGN a b"]

        self.assertTrue(TestUtils.check(input, expected, 113))

    def test_14(self):
        input = [
            "INSERT x string",
            "INSERT y string",
            "ASSIGN x ''",
            "ASSIGN y x"
        ]
        expected = ["success", "success", "success", "success"]

        self.assertTrue(TestUtils.check(input, expected, 114))

    