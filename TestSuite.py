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
        expected = ["Undeclared: ASSIGN x allocate"]

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
        expected = ["Undeclared: ASSIGN a b"]

        self.assertTrue(TestUtils.check(input, expected, 113))

    def test_14(self):
        input = [
            "INSERT x string",
            "ASSIGN x ''"
        ]
        expected = ["success", "success"]

        self.assertTrue(TestUtils.check(input, expected, 114))

    def test_15(self):
        input = [
            "INSERT x string",
            "INSERT y string",
            "ASSIGN x ''",
            "ASSIGN y x"
        ]
        expected = ["success", "success", "success", "success"]

        self.assertTrue(TestUtils.check(input, expected, 115))

    def test_16(self):
        input = [
            "INSERT x string",
            "ASSIGN x 'abc'",
            "INSERT y string",
            "ASSIGN y x",
        ]
        expected = ["success", "success", "success", "success"]

        self.assertTrue(TestUtils.check(input, expected, 116))

    def test_17(self):
        input = [
            "INSERT x string",
            "BEGIN",
            "INSERT y string",
            "ASSIGN y x",
            "PRINT",
            "END"
        ]
        expected = ["success", "success", "success", "x//0 y//1"]

        self.assertTrue(TestUtils.check(input, expected, 117))

    def test_18(self):
        input = [
            "INSERT x number",
            "BEGIN",
            "INSERT y string",
            "INSERT z number",
            "ASSIGN z 2300",
            "ASSIGN x 12",
            "ASSIGN x z",
            "RPRINT",
            "END",
            "PRINT"
        ]
        expected = ["success", "success", "success", "success", "success", "success", "z//1 y//1 x//0", "x//0"]

        self.assertTrue(TestUtils.check(input, expected, 118))

    def test_19(self):
        input = ["INSERT 'a' number"]
        expected = ["Invalid: INSERT 'a' number"]

        self.assertTrue(TestUtils.check(input, expected, 119))

    def test_20(self):
        input = ["INSERT A4 string", "PRINT"]
        expected = ["Invalid: INSERT A4 string"]

        self.assertTrue(TestUtils.check(input, expected, 120))

    def test_21(self):
        input = [
            "BEGIN",
            "INSERT x number",
            "ASSIGN x 9",
            "END",
            "INSERT y string",
            "ASSIGN y 2a",
            "PRINT"
        ]
        expected = ["Invalid: ASSIGN y 2a"]

        self.assertTrue(TestUtils.check(input, expected, 121))

    def test_22(self):
        input = ["INSERT x boolean", "ASSIGN x 1"]
        expected = ["Invalid: INSERT x boolean"]

        self.assertTrue(TestUtils.check(input, expected, 122))

    def test_23(self):
        input = ["INSERT x number", "ASSIGN x 1.5"]
        expected = ["Invalid: ASSIGN x 1.5"]

        self.assertTrue(TestUtils.check(input, expected, 123))

    def test_24(self):
        input = ["INSERT x string", "ASSIGN x 'a b'"]
        expected = ["Invalid: ASSIGN x 'a b'"]

        self.assertTrue(TestUtils.check(input, expected, 124))

    def test_25(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "ASSIGN x 18",
            "ASSIGN y x",
        ]
        expected = ["TypeMismatch: ASSIGN y x"]

        self.assertTrue(TestUtils.check(input, expected, 125))

    def test_26(self):
        input = [
            "BEGIN",
            "INSERT x1 string",
            "INSERT x2 string",
            "BEGIN",
            "INSERT x3 string",
            "ASSIGN x3 x2",
            "ASSIGN x2 x1",
            "BEGIN",
            "LOOKUP x3",
            "END",
            "LOOKUP x2",
            "PRINT",
            "END",
            "LOOKUP x1",
            "END",
            "RPRINT"
        ]
        expected = ["success", "success", "success", "success", "success", "2", "1", "x1//1 x2//1 x3//2", "1", ""]

        self.assertTrue(TestUtils.check(input, expected, 126))

    def test_27(self):
        input = ["END"]
        expected = ["UnknownBlock"]
        self.assertTrue(TestUtils.check(input, expected, 127))

    def test_28(self):
        input = [
            "INSERT z string",
            "BEGIN",
            "INSERT x number",
            "ASSIGN x z",
            "LOOKUP x",
            "END",
            "RPRINT"
        ]
        expected = ["TypeMismatch: ASSIGN x z"]

        self.assertTrue(TestUtils.check(input, expected, 128))

    def test_29(self):
        input = [
            "ADD x number",
            "LOOKUP x"
        ]
        expected = ["Invalid: ADD x number"]

        self.assertTrue(TestUtils.check(input, expected, 129))

    def test_30(self):
        input = [
            "INSERT a number",
            "BEGIN",
            "INSERT c string",
            "ASSIGN c 'xyz'",
            "BEGIN",
            "INSERT b number",
            "PRINT",
            "END",
            "RPRINT",
            "LOOKUP b",
            "END",
        ]
        expected = ["Undeclared: LOOKUP b"]

        self.assertTrue(TestUtils.check(input, expected, 130))

    def test_31(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "INSERT x number",
            "BEGIN",
            "INSERT z number",
            "PRINT",
            "END",
        ]
        expected = ["Redeclared: INSERT x number"]

        self.assertTrue(TestUtils.check(input, expected, 131))

    def test_32(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "BEGIN",
            "INSERT x string",
            "INSERT z number",
            "ASSIGN z 100",
            "LOOKUP z",
            "END",
            "PRINT",
        ]
        expected = ["success", "success", "success", "success", "success", "1", "x//0 y//0"]

        self.assertTrue(TestUtils.check(input, expected, 132))

    def test_33(self):
        input = [
            "Insert x number",
            "load x 1",
        ]
        expected = ["Invalid: Insert x number"]

        self.assertTrue(TestUtils.check(input, expected, 133))

    def test_34(self):
        input = [
            "PRINT",
            "INSERT x number",
            "BEGIN",
            "INSERT c string",
            "BEGIN",
            "INSERT h string",
            "RPRINT",
            "END",
            "PRINT",
            "END",
        ]
        expected = ["", "success", "success", "success", "h//2 c//1 x//0", "x//0 c//1"]

        self.assertTrue(TestUtils.check(input, expected, 134))

    def test_35(self):
        input = [
            "INSERT x number",
            "ASSIGN x 100",
            "BEGIN",
            "INSERT x number",
            "ASSIGN x 200",
            "BEGIN",
            "INSERT x number",
            "ASSIGN x 300",
            "END",
            "ASSIGN x 400",
            "END",
            "LOOKUP x",
        ]
        expected = ["success", "success", "success", "success", "success", "success", "success", "0"]

        self.assertTrue(TestUtils.check(input, expected, 135))

    def test_36(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "BEGIN",
            "INSERT z number",
            "ASSIGN z 42",
            "INSERT x string",
            "ASSIGN x 'hello'",
            "BEGIN",
            "INSERT y number",
            "ASSIGN y z",
            "LOOKUP x",
            "LOOKUP y",
            "LOOKUP z",
            "END",
            "LOOKUP x",
            "LOOKUP y",
            "END",
            "LOOKUP x",
            "LOOKUP y",
        ]
        expected = [
            "success", "success", "success", "success", "success", "success", "success", "success",
            "1", "2", "1", "1", "0", "0", "0"
        ]

        self.assertTrue(TestUtils.check(input, expected, 136))

    def test_37(self):
        input = [
            "INSERT x string",
            "ASSIGN x ''",
            "INSERT y string",
            "ASSIGN y x",
            "ASSIGN x 'abc'",
            "ASSIGN y x",
            "BEGIN",
            "INSERT z string",
            "ASSIGN z y",
            "END"
        ]
        expected = ["success", "success", "success", "success", "success", "success", "success", "success"]

        self.assertTrue(TestUtils.check(input, expected, 137))

    def test_38(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "BEGIN",
            "INSERT z number",
            "ASSIGN z x",
            "BEGIN",
            "INSERT a string",
            "ASSIGN a y",
            "INSERT b number",
            "ASSIGN b z",
            "ASSIGN b a",
            "END",
            "END"
        ]
        expected = ["TypeMismatch: ASSIGN b a"]

        self.assertTrue(TestUtils.check(input, expected, 138))

    def test_39(self):
        input = [
            "BEGIN",
            "INSERT x number",
            "BEGIN",
            "INSERT y string",
            "BEGIN",
            "INSERT z number",
            "END",
            "LOOKUP z",
            "END",
            "LOOKUP y",
            "END"
        ]
        expected = ["Undeclared: LOOKUP z"]

        self.assertTrue(TestUtils.check(input, expected, 139))

    def test_40(self):
        input = [
            "BEGIN",
            "BEGIN",
            "BEGIN",
            "INSERT x number",
            "END",
            "END",
            "END",
            "LOOKUP x"
        ]
        expected = ["Undeclared: LOOKUP x"]

        self.assertTrue(TestUtils.check(input, expected, 140))

    def test_41(self):
        input = [
            "INSERT x number",
            "BEGIN",
            "INSERT x string",
            "ASSIGN x 'abc'",
            "END",
            "ASSIGN x 'def'"
        ]
        expected = ["TypeMismatch: ASSIGN x 'def'"]

        self.assertTrue(TestUtils.check(input, expected, 141))

    def test_42(self):
        input = [
            "INSERT a number",
            "INSERT b number",
            "INSERT c number",
            "ASSIGN a 10",
            "ASSIGN b a",
            "ASSIGN c b",
            "BEGIN",
            "INSERT d number",
            "ASSIGN d c",
            "BEGIN",
            "INSERT e string",
            "ASSIGN e d",
            "END",
            "END"
        ]
        expected = ["TypeMismatch: ASSIGN e d"]

        self.assertTrue(TestUtils.check(input, expected, 142))

    def test_43(self):
        input = [
            "INSERT x number",
            "INSERT 123y string",
            "ASSIGN x 10",
            "PRINT"
        ]
        expected = ["Invalid: INSERT 123y string"]

        self.assertTrue(TestUtils.check(input, expected, 143))

    def test_44(self):
        input = [
            "INSERT x number",
            "BEGIN",
            "INSERT y string",
            "BEGIN",
            "INSERT x string",
            "END",
            "PRINT",
            "END"
        ]
        expected = ["success", "success", "success", "x//0 y//1"]

        self.assertTrue(TestUtils.check(input, expected, 144))

    def test_45(self):
        input = [
            "BEGIN",
            "BEGIN",
            "BEGIN",
            "PRINT",
            "END",
            "PRINT",
            "END",
            "PRINT",
            "END"
        ]
        expected = ["", "", ""]

        self.assertTrue(TestUtils.check(input, expected, 145))

    def test_46(self):
        input = [
            "INSERT",
            "ASSIGN x 10",
            "PRINT"
        ]
        expected = ["Invalid: INSERT"]

        self.assertTrue(TestUtils.check(input, expected, 146))

    def test_47(self):
        input = [
            "INSERT a string",
            "INSERT b string",
            "INSERT c string",
            "ASSIGN a 'hello'",
            "ASSIGN b a",
            "ASSIGN c b",
            "INSERT x number",
            "ASSIGN x c"
        ]
        expected = ["TypeMismatch: ASSIGN x c"]

        self.assertTrue(TestUtils.check(input, expected, 147))

    def test_48(self):
        input = [
            "INSERT x string",
            "ASSIGN x 'a'",
            "ASSIGN x ' '"
        ]
        expected = ["Invalid: ASSIGN x ' '"]

        self.assertTrue(TestUtils.check(input, expected, 148))

    def test_49(self):
        input = [
            "INSERT a number",
            "INSERT b string",
            "BEGIN",
            "INSERT c number",
            "INSERT d string",
            "BEGIN",
            "INSERT a string",
            "INSERT b number",
            "RPRINT",
            "END",
            "PRINT",
            "END",
            "RPRINT"
        ]
        expected = ["success", "success", "success", "success", "success", "success",
                    "b//2 a//2 d//1 c//1", "a//0 b//0 c//1 d//1", "b//0 a//0"]
        
        self.assertTrue(TestUtils.check(input, expected, 149))

    def test_50(self):
        input = ["INSERT number number"]
        expected = ["success"]

        self.assertTrue(TestUtils.check(input, expected, 150))

    def test_51(self):
        input = ["ASSIGN x 123.4"]
        expected = ["Invalid: ASSIGN x 123.4"]
        self.assertTrue(TestUtils.check(input, expected, 151))

    def test_52(self):
        input = ["LOOKUP A"]
        expected = ["Invalid: LOOKUP A"]
        self.assertTrue(TestUtils.check(input, expected, 152))

    def test_53(self):
        input = ["ASSIGN w string"]
        expected = ["Undeclared: ASSIGN w string"]
        self.assertTrue(TestUtils.check(input, expected, 153))

    def test_54(self):
        input = [
            "",
            "INSERT x string"
        ]
        expected = ["Invalid: "]
        
        self.assertTrue(TestUtils.check(input, expected, 154))

    def test_55(self):
        input = []
        expected = []
        self.assertTrue(TestUtils.check(input, expected, 155))

    def test_56(self):
        input = [
            "INSERT z string",
            "INSERT x string",
            "INSERT y string",
            "BEGIN",
            "INSERT x string",
            "BEGIN",
            "RPRINT",
            "INSERT z string",
            "END",
            "END"
        ]
        expected = ["success", "success", "success", "success", "x//1 y//0 z//0", "success"]

        self.assertTrue(TestUtils.check(input, expected, 156))

    def test_57(self):
        input = ["PRINT"]
        expected = []
        self.assertTrue(TestUtils.check(input, expected, 157))

    def test_58(self):
        input = [
            "BEGIN",
            "INSERT x number",
            "END",
            "INSERT x number",
            "BEGIN",
            "INSERT x number",
            "END",
            "LOOKUP x"
        ]
        expected = ["success", "success", "success", "0"]
        
        self.assertTrue(TestUtils.check(input, expected, 158))

    def test_59(self):
        input = [
            "BEGIN",
            "INSERT x string",
            "INSERT y string",
            "ASSIGN y 1",
            "INSERT x number",
            "INSERT y number",
            "END"
        ]
        expected = ["TypeMismatch: ASSIGN y 1"]

        self.assertTrue(TestUtils.check(input, expected, 159))

    def test_60(self):
        input = [
            "INSERT number number",
            "ASSIGN number number"
        ]
        expected = ["success", "success"]

        self.assertTrue(TestUtils.check(input, expected, 160))

    def test_61(self):
        input = [
            "INSERT string string",
            "INSERT number number",
            "ASSIGN string number"
        ]
        expected = ["TypeMismatch: ASSIGN string number"]

        self.assertTrue(TestUtils.check(input, expected, 161))

    def test_62(self):
        input = ["INSERT x number", "ASSIGN x bc~ed"]
        expected = ["Invalid: ASSIGN x bc~ed"]
        self.assertTrue(TestUtils.check(input, expected, 162))

    def test_63(self):
        input = ["INSERT x string", "ASSIGN x 'azAZq7e269'"]
        expected = ["success", "success"]
        self.assertTrue(TestUtils.check(input, expected, 163))

    def test_64(self):
        input = ["INSERT a number", "ASSIGN a 12e-7"]
        expected = ["Invalid: ASSIGN a 12e-7"]
        self.assertTrue(TestUtils.check(input, expected, 164))

    def test_65(self):
        input = [
            "INSERT abcde number", 
            "INSERT abc number", 
            "INSERT abcd number", 
            "INSERT abcdef number", 
            "INSERT abc number",
            "INSERT abcde number"
        ]
        expected = ["Redeclared: INSERT abc number"]

        self.assertTrue(TestUtils.check(input, expected, 165))

    def test_66(self):
        input = [
            "BEGIN", 
            "INSERT x string", 
            "ASSIGN x 'invalid'"
        ]
        expected = ["UnclosedBlock: 1"]

        self.assertTrue(TestUtils.check(input, expected, 166))

    def test_67(self):
        input = ["RPRINT "]
        expected = ["Invalid: RPRINT "]
        self.assertTrue(TestUtils.check(input, expected, 167))

    def test_68(self):
        input = [
            "INSERT x1 number", 
            "BEGIN", 
            "ASSIGN x1 12/9"
        ]
        expected = ["Invalid: ASSIGN x1 12/9"]

        self.assertTrue(TestUtils.check(input, expected, 168))

    def test_69(self):
        input = ["ASSIGN bc~ed 1"]
        expected = ["Invalid: ASSIGN bc~ed 1"]
        self.assertTrue(TestUtils.check(input, expected, 169))

    def test_70(self):
        input = ["INSERT x string", "ASSIGN x x"]
        expected = ["success", "success"]
        self.assertTrue(TestUtils.check(input, expected, 170))