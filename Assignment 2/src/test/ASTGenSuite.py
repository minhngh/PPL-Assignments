import unittest
from TestUtils import TestAST
from AST import *

class ASTGenSuite(unittest.TestCase):
    def test_case_1(self):
        input = """Var:x;"""
        expect = Program([VarDecl(Id("x"),[],None)])
        self.assertTrue(TestAST.checkASTGen(input,expect,300))
    def test_case_2(self):
        input = """Var:x, y[2][3] = {2, 3};"""
        expect = Program([VarDecl(Id('x'), [], None),VarDecl(Id('y'),[2,3],ArrayLiteral([IntLiteral(2),IntLiteral(3)]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,301))
    def test_case_3(self):
        input = """Var:x, y = 10, s ="ad\\fs", y[2][3] = {{2}, {3}};"""
        expect = Program([VarDecl(Id('x'), [], None), VarDecl(Id('y'), [], IntLiteral(10)),VarDecl(Id('s'), [], StringLiteral("ad\\fs")),VarDecl(Id('y'),[2,3],ArrayLiteral([ArrayLiteral([IntLiteral(2)]),ArrayLiteral([IntLiteral(3)])]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,302))
    def test_case_4(self):
        input = """Var:x, y = 10, s ="ad\\fs", y[2][3]; Var: xyasd = 123, flag = True;"""
        expect = Program([VarDecl(Id('x'), [], None),VarDecl(Id('y'), [],IntLiteral(10)),VarDecl(Id('s'), [],StringLiteral('ad\\fs')),VarDecl(Id('y'), [2, 3], None),VarDecl(Id('xyasd'),[],IntLiteral(123)),VarDecl(Id('flag'), [],BooleanLiteral(True))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 303))
    def test_case_5(self):
        input = """
        Function: main
        Body:
            Return 0;
        EndBody.
        """
        expect =  Program([FuncDecl(Id('main'),[], ([], [Return(IntLiteral(0))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 304))
    def test_case_6(self):
        input = """
        Function: main
        Body:
            Return 1 + 2 + 3;
        EndBody.
        """
        expect =  Program([FuncDecl(Id('main'),[], ([], [Return(BinaryOp('+',BinaryOp('+',IntLiteral(1),IntLiteral(2)),IntLiteral(3)))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 305))
    def test_case_7(self):
        input = """
        Function: fact
        Parameter: n
        Body:
            If n == 0 Then
                Return 1;
            Else
                Return n * fact (n - 1);
            EndIf.
        EndBody.
        """
        i1 = (BinaryOp('==',Id('n'),IntLiteral(0)), [], [Return(IntLiteral(1))])
        i2 = ([], [Return(BinaryOp('*',Id('n'),CallExpr(Id('fact'),[BinaryOp('-',Id('n'),IntLiteral(1))])))])
        if_stmts = If([i1], i2)
        fn = FuncDecl(Id('fact'), [VarDecl(Id('n'), [], None)], ([], [if_stmts]))
        expect =  Program([fn])
        self.assertTrue(TestAST.checkASTGen(input, expect, 306))
    def test_case_8(self):
        input = """
        Function: foo
        Parameter: a[5], b
        Body:
            Var: i = 0;
            While (i < 5) Do
                a[i] = b +. 1.0;
                i = i + 1;
            EndWhile.
        EndBody.
        """
        w = While(BinaryOp('<',Id('i'),IntLiteral(5)), ([], [Assign(ArrayCell(Id('a'),[Id('i')]), BinaryOp('+.',Id('b'),FloatLiteral(1.0))), Assign(Id('i'), BinaryOp('+', Id('i'), IntLiteral(1)))]))
        fn = FuncDecl(Id('foo'), [VarDecl(Id('a'), [5], None), VarDecl(Id('b'), [], None)], ([VarDecl(Id('i'), [], IntLiteral(0))], [w]))
        expect =  Program([fn])
        self.assertTrue(TestAST.checkASTGen(input, expect, 307))
    def test_case_9(self):
        input = """
        Function: main
        Body:
            For (i = 0, i < 10, 2) Do
                writeln(i);
            EndFor.
        EndBody.
        """
        f = For(Id('i'), IntLiteral(0), BinaryOp('<', Id('i'), IntLiteral(10)), IntLiteral(2), ([], [CallStmt(Id('writeln'), [Id('i')])]))
        fn = FuncDecl(Id('main'), [], ([], [f]))
        expect =  Program([fn])
        self.assertTrue(TestAST.checkASTGen(input, expect, 308))
    def test_case_10(self):
        input = """
        Function: main
        Body:
            Do
                a[3 + foo(2)] = a[b[2][3]] + 4;
            While i == False EndDo.

        EndBody.
        """
        f = Dowhile(([], [Assign(ArrayCell(Id('a'), [BinaryOp('+', IntLiteral(3), CallExpr(Id('foo'), [IntLiteral(2)]))]), BinaryOp('+', ArrayCell(Id('a'), [ArrayCell(Id('b'), [IntLiteral(2), IntLiteral(3)])]), IntLiteral(4)))]), BinaryOp('==', Id('i'), BooleanLiteral(False)))
        fn = FuncDecl(Id('main'), [], ([], [f]))
        expect =  Program([fn])
        self.assertTrue(TestAST.checkASTGen(input, expect, 309))
    def test_case_11(self):
        input = """
        Function: main
        Parameter: a[10], b
        Body:
            Var: i = 0;
            While x > 0 Do
                If i == 0 Then
                    Var: k = 0.;
                    main(i);
                EndIf.
            EndWhile.

        EndBody.
        """
        f = While(BinaryOp('>', Id('x'), IntLiteral(0)), ([], [If([(BinaryOp('==', Id('i'), IntLiteral(0)), [VarDecl(Id('k'), [], FloatLiteral(0.))], [CallStmt(Id('main'), [Id('i')])])], ([], []))]))
        fn = FuncDecl(Id('main'), [VarDecl(Id('a'), [10], None), VarDecl(Id('b'), [], None)], ([VarDecl(Id('i'), [], IntLiteral(0))], [f]))
        expect =  Program([fn])
        self.assertTrue(TestAST.checkASTGen(input, expect, 310))
    def test_case_12(self):
        input = """
        Var: a = 5, n[10], s = False;
        Var: bb[2][3] = {{2, 3, 4}, {4, 5, 6}};
        Function: main
        Body:
            flag = 2;
            a = !!!!True || dkd;
            Return fool() + uuuuu(2 + 3, f[2][4]) && dk;

        EndBody.
        """
        stmts = [Assign(Id('flag'), IntLiteral(2)), Assign(Id('a'), BinaryOp('||', UnaryOp('!', UnaryOp('!', UnaryOp('!', UnaryOp('!', BooleanLiteral(True))))),Id('dkd'))),\
                Return(BinaryOp('&&', BinaryOp('+', CallExpr(Id('fool'), []), CallExpr(Id('uuuuu'), [BinaryOp('+', IntLiteral(2), IntLiteral(3)), ArrayCell(Id('f'), [IntLiteral(2), IntLiteral(4)])])), Id('dk')))]
        fn = FuncDecl(Id('main'), [], ([], stmts))
        expect =  Program([VarDecl(Id('a'), [], IntLiteral(5)), VarDecl(Id('n'), [10], None), VarDecl(Id('s'), [], BooleanLiteral(False)), \
        VarDecl(Id('bb'), [2, 3], ArrayLiteral([ArrayLiteral([IntLiteral(2), IntLiteral(3), IntLiteral(4)]), ArrayLiteral([IntLiteral(4), IntLiteral(5), IntLiteral(6)])])), 
        fn])
        self.assertTrue(TestAST.checkASTGen(input, expect, 311))
    def test_case_13(self):
        input = """
        Var: s = "daofjsdg";
        Function: main
        Body:
            Var: arr[26];
            f = fact(n) % 0O10;
            While (i < length(s)) Do
                arr[lower(s[i]) - 97] =  arr[lower(s[i]) - 97] +. 1.e0;
            EndWhile.
            max_length = max(arr);
        EndBody.
        Function: sum
        Parameter: n
        Body:
            p = 1.;
            For (i = 1, i < n, 1) Do
                p = p *. i;
            EndFor.
            Return i;
        EndBody.
        """
        f1 = FuncDecl(Id('main'), [], ([VarDecl(Id('arr'), [26], None)], [Assign(Id('f'), BinaryOp('%', CallExpr(Id('fact'), [Id('n')]), IntLiteral(0o10))), \
            While(BinaryOp('<', Id('i'), CallExpr(Id('length'), [Id('s')])), ([], [Assign(ArrayCell(Id('arr'), [BinaryOp('-', CallExpr(Id('lower'), [ArrayCell(Id('s'), [Id('i')])]), IntLiteral(97))]), BinaryOp('+.', ArrayCell(Id('arr'), [BinaryOp('-', CallExpr(Id('lower'), [ArrayCell(Id('s'), [Id('i')])]), IntLiteral(97))]), FloatLiteral(1.0)))])),\
                Assign(Id('max_length'), CallExpr(Id('max'), [Id('arr')]))]))
        f2 = FuncDecl(Id('sum'), [VarDecl(Id('n'), [], None)], ([], [Assign(Id('p'), FloatLiteral(1.)), For(Id('i'), IntLiteral(1), BinaryOp('<', Id('i'), Id('n')), IntLiteral(1), ([], [Assign(Id('p'), BinaryOp('*.', Id('p'), Id('i')))])), Return(Id('i'))]))
        expect =  Program([VarDecl(Id('s'), [], StringLiteral("daofjsdg")), f1, f2])
        self.assertTrue(TestAST.checkASTGen(input, expect, 312))
    def test_case_14(self):
        input = """
        Var: s = "daofjsdg";
        Function: main
        Body:
            Var: arr[26];
            f = fact(n) % 0O10;
            While (i < length(s)) Do
                arr[lower(s[i]) - 97] =  arr[lower(s[i]) - 97] +. 1.e0;
            EndWhile.
            max_length = max(arr);
        EndBody.
        Function: sum
        Parameter: n
        Body:
            p = 1.;
            For (i = 1, i < n, 1) Do
                p = p *. i;
            EndFor.
            Return i;
        EndBody.
        """
        f1 = FuncDecl(Id('main'), [], ([VarDecl(Id('arr'), [26], None)], [Assign(Id('f'), BinaryOp('%', CallExpr(Id('fact'), [Id('n')]), IntLiteral(0o10))), \
            While(BinaryOp('<', Id('i'), CallExpr(Id('length'), [Id('s')])), ([], [Assign(ArrayCell(Id('arr'), [BinaryOp('-', CallExpr(Id('lower'), [ArrayCell(Id('s'), [Id('i')])]), IntLiteral(97))]), BinaryOp('+.', ArrayCell(Id('arr'), [BinaryOp('-', CallExpr(Id('lower'), [ArrayCell(Id('s'), [Id('i')])]), IntLiteral(97))]), FloatLiteral(1.0)))])),\
                Assign(Id('max_length'), CallExpr(Id('max'), [Id('arr')]))]))
        f2 = FuncDecl(Id('sum'), [VarDecl(Id('n'), [], None)], ([], [Assign(Id('p'), FloatLiteral(1.)), For(Id('i'), IntLiteral(1), BinaryOp('<', Id('i'), Id('n')), IntLiteral(1), ([], [Assign(Id('p'), BinaryOp('*.', Id('p'), Id('i')))])), Return(Id('i'))]))
        expect =  Program([VarDecl(Id('s'), [], StringLiteral("daofjsdg")), f1, f2])
        self.assertTrue(TestAST.checkASTGen(input, expect, 313))
    def test_case_15(self):
        input = """
        Function: main
        Body:
            Var: x = 0x213ACF, s = 123e-3;
            v = 4 \. (3 *. 314e-2) * r * r * r;
            If x < 10 Then
                Break;
            Else
                x = x && d >. 1;
            EndIf.
        EndBody.
        """
        expect =  Program([FuncDecl(Id('main'), [], ([VarDecl(Id('x'), [], IntLiteral(0x213ACF)), VarDecl(Id('s'), [], FloatLiteral(123e-3))], \
            [Assign(Id('v'), BinaryOp('*', BinaryOp('*', BinaryOp('*', BinaryOp('\\.', IntLiteral(4), BinaryOp('*.', IntLiteral(3), FloatLiteral(314e-2))), Id('r')),Id('r')), Id('r'))), \
                If([(BinaryOp('<', Id('x'), IntLiteral(10)), [], [Break()])], ([], [Assign(Id('x'), BinaryOp('>.', BinaryOp('&&', Id('x'), Id('d')), IntLiteral(1)))]))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 314))
    def test_case_16(self):
        input = """
        Function: main
        Body:
            Do
                Var: k = 12;
                k = -.-k;
                a[2][3 + 3] = foo(2 + k, k, arr[0]);
                m = a[1][2 + f[2]];
            While x == 0 EndDo.
        EndBody.
        """
        expect =  Program([FuncDecl(Id('main'), [], ([], [Dowhile(([VarDecl(Id('k'), [], IntLiteral(12))], [Assign(Id('k'), UnaryOp('-.', UnaryOp('-', Id('k')))), \
            Assign(ArrayCell(Id('a'), [IntLiteral(2), BinaryOp('+', IntLiteral(3), IntLiteral(3))]), \
            CallExpr(Id('foo'), [BinaryOp('+', IntLiteral(2), Id('k')), Id('k'), ArrayCell(Id('arr'), [IntLiteral(0)])])), \
            Assign(Id('m'), ArrayCell(Id('a'), [IntLiteral(1), BinaryOp('+', IntLiteral(2), ArrayCell(Id('f'), [IntLiteral(2)]))]))]), BinaryOp('==', Id('x'), IntLiteral(0)))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 315))
    def test_case_17(self):
        input = """
        Var: m, n[10]; 
        Function: main 
        Parameter: n 
        Body: 
            x = {{{1,2}, {3,4}}, {5,6}};
            If n == 0 Then 
                Return 1; 
            Else
                Return n * face({1,2});
            EndIf.
        EndBody. 
        """
        expect =  Program([VarDecl(Id('m'), [], None), VarDecl(Id('n'), [10], None), FuncDecl(Id('main'), [VarDecl(Id('n'), [], None)], ([], [\
            Assign(Id('x'), ArrayLiteral([ArrayLiteral([ArrayLiteral([IntLiteral(1), IntLiteral(2)]), ArrayLiteral([IntLiteral(3), IntLiteral(4)])]), ArrayLiteral([IntLiteral(5), IntLiteral(6)])])),\
            If([(BinaryOp('==', Id('n'), IntLiteral(0)), [], [Return(IntLiteral(1))])], ([], [Return(BinaryOp('*', Id('n'), CallExpr(Id('face'), [ArrayLiteral([IntLiteral(1), IntLiteral(2)])])))]))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 316))
    def test_case_18(self):
        input = """
        Var: a, b, c = 10e12;
        Function: main
        Body:
            Var: i = 0, arr[10];
            c = arr[0];
            For (i = 1, i < 10, 1) Do
                If (c < arr[i]) Then
                    c = arr[i];
                EndIf.
            EndFor.  
            f(1, 2, 3);
            Return;
        EndBody.
        """
        expect =  Program([VarDecl(Id('a'), [], None), VarDecl(Id('b'), [], None), VarDecl(Id('c'), [], FloatLiteral(10e12)), FuncDecl(Id('main'), [], ([VarDecl(Id('i'), [], IntLiteral(0)), VarDecl(Id('arr'), [10], None)], [\
                Assign(Id('c'), ArrayCell(Id('arr'), [IntLiteral(0)])),\
                For(Id('i'), IntLiteral(1), BinaryOp('<', Id('i'), IntLiteral(10)), IntLiteral(1), ([], [If([(BinaryOp('<', Id('c'), ArrayCell(Id('arr'), [Id('i')])), [], [Assign(Id('c'), ArrayCell(Id('arr'), [Id('i')]))])], ([], []))])),\
                CallStmt(Id('f'), [IntLiteral(1), IntLiteral(2), IntLiteral(3)]), Return(None)]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 317))
    def test_case_19(self):
        input = """
        Function: sort
        Parameter: arr[0o100], left, right
        Body:
            For(i = left + 1, i <= right, 1) Do
                Var: temp, j;
                temp = arr[i];
                j = i - 1;
                While (j >= left) && (arr[j] > temp) Do
                    arr[j + 1] = arr[j];
                    j = j - 1;
                EndWhile.
                arr[j + 1] = temp;
            EndFor.
        EndBody.
        """
        expect =  Program([FuncDecl(Id('sort'), [VarDecl(Id('arr'), [0o100], None), VarDecl(Id('left'), [], None), VarDecl(Id('right'), [], None)], ([], [\
                For(Id('i'), BinaryOp('+', Id('left'), IntLiteral(1)), BinaryOp('<=', Id('i'), Id('right')), IntLiteral(1), ([VarDecl(Id('temp'), [], None), VarDecl(Id('j'), [], None)], \
                [Assign(Id('temp'), ArrayCell(Id('arr'), [Id('i')])), Assign(Id('j'), BinaryOp('-', Id('i'), IntLiteral(1))),\
                While(BinaryOp('&&', BinaryOp('>=', Id('j'), Id('left')), BinaryOp('>', ArrayCell(Id('arr'), [Id('j')]), Id('temp'))),([], [Assign(ArrayCell(Id('arr'), [BinaryOp('+', Id('j'), IntLiteral(1))]), ArrayCell(Id('arr'), [Id('j')])), Assign(Id('j'), BinaryOp('-', Id('j'), IntLiteral(1)))])),\
                Assign(ArrayCell(Id('arr'), [BinaryOp('+', Id('j'), IntLiteral(1))]), Id('temp'))
                ]))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 318))
    def test_case_20(self):
        input = """
        Function: convert
        Parameter: str
        Body:
            Var: arr[100];
            Var: length;
            length = length(str) - 1;
            Return length;
        EndBody.
        Function: main
        Body:
            convert();
        EndBody.
        """
        f1 = FuncDecl(Id('convert'), [VarDecl(Id('str'), [], None)], ([VarDecl(Id('arr'), [100], None), VarDecl(Id('length'), [], None)], [Assign(Id('length'), BinaryOp('-', CallExpr(Id('length'), [Id('str')]), IntLiteral(1))), Return(Id('length'))]))
        f2 = FuncDecl(Id('main'), [], ([], [CallStmt(Id('convert'), [])]))
        expect =  Program([f1, f2])
        self.assertTrue(TestAST.checkASTGen(input, expect, 319))
    def test_case_21(self):
        input = """
        Function: main
        Body:
            a = f(2, 3 + 4)[1 + 2];
        EndBody.
        """
        f = FuncDecl(Id('main'), [], ([], [Assign(Id('a'), ArrayCell(CallExpr(Id('f'), [IntLiteral(2), BinaryOp('+', IntLiteral(3), IntLiteral(4))]), [BinaryOp('+', IntLiteral(1), IntLiteral(2))]))]))
        expect =  Program([f])
        self.assertTrue(TestAST.checkASTGen(input, expect, 320))
    def test_case_22(self):
        input = """
        Function: fact
        Parameter: x, a[2]
        Body:
            For (i = 0, i < 10, 2) Do
                If (x) Then Break; EndIf.
            EndFor.
            If (x) Then Break; EndIf.
        EndBody.
        """
        if_stmt = If([(Id('x'), [], [Break()])], ([], []))
        f = FuncDecl(Id('fact'), [VarDecl(Id('x'), [], None), VarDecl(Id('a'), [2], None)], ([], [For(Id('i'), IntLiteral(0), BinaryOp('<', Id('i'), IntLiteral(10)), IntLiteral(2), ([], [if_stmt])), if_stmt]))
        expect =  Program([f])
        self.assertTrue(TestAST.checkASTGen(input, expect, 321))
    def test_case_23(self):
        input = """
        Function: main
        Body:
            Var: x = 10;
            kk = 0o10 && 0x123 || 12.3 + True;
            f(1 + 2, a)[2 + a[2]] = a[0][2 + 2][f()]; 
            While x < cond() Do
                print("string, hala madrid");
            EndWhile.
        EndBody.
        """
        f = FuncDecl(Id('main'), [], ([VarDecl(Id('x'), [], IntLiteral(10))], [Assign(Id('kk'), BinaryOp('||', BinaryOp('&&', IntLiteral(0o10), IntLiteral(0x123)), BinaryOp('+', FloatLiteral(12.3), BooleanLiteral(True)))), \
                                        Assign(ArrayCell(CallExpr(Id('f'), [BinaryOp('+', IntLiteral(1), IntLiteral(2)), Id('a')]), [BinaryOp('+', IntLiteral(2), ArrayCell(Id('a'), [IntLiteral(2)]))]), ArrayCell(Id('a'), [IntLiteral(0), BinaryOp('+', IntLiteral(2), IntLiteral(2)), CallExpr(Id('f'), [])])),\
                                        While(BinaryOp('<', Id('x'), CallExpr(Id('cond'), [])), ([], [CallStmt(Id('print'), [StringLiteral("string, hala madrid")])]))
                                        ]))
        expect = Program([f])
        self.assertTrue(TestAST.checkASTGen(input, expect, 322))
    def test_case_24(self):
        input = """
        Function: main
        Body:
            Do
                f_n_f(12);
                While x Do
                    Var: x;
                    If x == 1 Then
                        Var: x;
                    EndIf.
                EndWhile.
            While True EndDo.
        EndBody.
        """
        dowhile = Dowhile(([], [CallStmt(Id('f_n_f'), [IntLiteral(12)]), While(Id('x'), ([VarDecl(Id('x'), [], None)], [If([(BinaryOp('==', Id('x'), IntLiteral(1)), [VarDecl(Id('x'), [], None)], [])], ([], []))]))]), BooleanLiteral(True))
        f = FuncDecl(Id('main'), [], ([], [dowhile]))
        expect = Program([f])
        self.assertTrue(TestAST.checkASTGen(input, expect, 323))
    def test_case_25(self):
        input = """
        Function: main
        Body:
            For(i = init(), i < bound(), step()) Do
                a = in(f(in(2, f())))[f()];
            EndFor.
        EndBody.
        """
        f = FuncDecl(Id('main'), [], ([], [For(Id('i'), CallExpr(Id('init'), []), BinaryOp('<', Id('i'), CallExpr(Id('bound'), [])), CallExpr(Id('step'), []), ([],\
             [Assign(Id('a'), ArrayCell(CallExpr(Id('in'), [CallExpr(Id('f'), [CallExpr(Id('in'), [IntLiteral(2), CallExpr(Id('f'), [])])])]), [CallExpr(Id('f'), [])]))]))]))
        expect = Program([f])
        self.assertTrue(TestAST.checkASTGen(input, expect, 324))
    def test_case_26(self):
        input = """
        Function: main
        Body:
            Var: x = 0., y = 2.;
            While (x =/= f()) Do
                x = x +. 1;
                y = y -. 1;
            EndWhile.
            Return 0;
        EndBody.
        """
        f = FuncDecl(Id('main'), [], ([VarDecl(Id('x'), [], FloatLiteral(0.)), VarDecl(Id('y'), [], FloatLiteral(2.))], [While(BinaryOp('=/=', Id('x'), CallExpr(Id('f'), [])), ([], \
            [Assign(Id('x'), BinaryOp('+.', Id('x'), IntLiteral(1))), Assign(Id('y'), BinaryOp('-.', Id('y'), IntLiteral(1)))])), Return(IntLiteral(0))]))
        expect = Program([f])
        self.assertTrue(TestAST.checkASTGen(input, expect, 325))
    def test_case_27(self):
        input = """
        Function: main
        Parameter: k
        Body:
            Var: i = 10, k[10][2] = {{}, {}};
            Do
                Continue;
            While i <= 10 EndDo.
            Return 0;
        EndBody.
        """
        f = FuncDecl(Id('main'), [VarDecl(Id('k'), [], None)], ([VarDecl(Id('i'), [], IntLiteral(10)), VarDecl(Id('k'), [10, 2], ArrayLiteral([ArrayLiteral([]), ArrayLiteral([])]))], [Dowhile(([], [Continue()]), BinaryOp('<=', Id('i'), IntLiteral(10))), Return(IntLiteral(0))]))
        expect = Program([f])
        self.assertTrue(TestAST.checkASTGen(input, expect, 326))
    def test_case_28(self):
        input = """
        Function: main
        Body:
           x =  f("1", "194") + a[0][3] * "blu bla";
        EndBody.
        """
        f = FuncDecl(Id('main'), [], ([], [Assign(Id('x'), BinaryOp('+', CallExpr(Id('f'), [StringLiteral("1"), StringLiteral("194")]), BinaryOp('*', ArrayCell(Id('a'), [IntLiteral(0), IntLiteral(3)]), StringLiteral("blu bla"))))]))
        expect = Program([f])
        self.assertTrue(TestAST.checkASTGen(input, expect, 327))
    def test_case_29(self):
        input = """
        Function: main
        Body:
            For(counter = 0., foo() * a[23] == 2, "asd") Do
                x = 213;
            EndFor.
        EndBody.
        """
        f = FuncDecl(Id('main'), [], ([], [For(Id('counter'), FloatLiteral(0.), BinaryOp('==', BinaryOp('*', CallExpr(Id('foo'), []), ArrayCell(Id('a'), [IntLiteral(23)])), IntLiteral(2)), StringLiteral("asd"), ([], [Assign(Id('x'), IntLiteral(213))]))]))
        expect = Program([f])
        self.assertTrue(TestAST.checkASTGen(input, expect, 328))
    def test_case_30(self):
        input = """
        Function: main
        Body:
            inp = 123 * daf[g132[423][2] * 132 + {13}];
        EndBody.
        """
        expect = Program([FuncDecl(Id('main'), [],([], [Assign(Id('inp'),BinaryOp('*',IntLiteral(123),ArrayCell(Id('daf'),[BinaryOp('+',BinaryOp('*',ArrayCell(Id('g132'),[IntLiteral(423),IntLiteral(2)]),IntLiteral(132)),ArrayLiteral([IntLiteral(13)]))])))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 329))
    def test_case_31(self):
        input = """
        Function: main
        Body:
            If "" Then
            in = 123 - 4234 +. 432 || !False;
            inp = {123, 435, 423} * in;
            EndIf.
        EndBody.
        """
        expect = Program([FuncDecl(Id('main'), [],([], [If([(StringLiteral(''),[],[Assign(Id('in'),BinaryOp('||',BinaryOp('+.',BinaryOp('-',IntLiteral(123),IntLiteral(4234)),IntLiteral(432)),UnaryOp('!',BooleanLiteral(False)))),Assign(Id('inp'),BinaryOp('*',ArrayLiteral([IntLiteral(123),IntLiteral(435),IntLiteral(423)]),Id('in')))])], ([], []))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 330))
    def test_case_32(self):
        input = """
        Var: x, y =1, y = "abc'" hello \\t ", m[13425], n[1053245] = {1,2,{"a534n",5.54324},5.e-145232};
            Var: a_jacj933 = 00012.21; 
        Function: fact
        Parameter: n, aca_312aAX[3][44][0x31FF], cxa[0x12][0o1][8][0]
        Body:
        Var: t, r= 10.;
        Var: thread = 0000212.3123E+2120, r= 10.;
        v = (4. \\. 3.) *.   3.14 *. r * r * a;
        
        object = 4123542 + 7 > 4;
        EndBody.
        """
        expect = Program([VarDecl(Id('x'), [], None),VarDecl(Id('y'), [],IntLiteral(1)),VarDecl(Id('y'), [],StringLiteral("""abc'" hello \\t """)),VarDecl(Id('m'),[13425], None),VarDecl(Id('n'),[1053245],ArrayLiteral([IntLiteral(1),IntLiteral(2),ArrayLiteral([StringLiteral("""a534n"""),FloatLiteral(5.54324)]),FloatLiteral(0.0)])),VarDecl(Id('a_jacj933'), [],FloatLiteral(12.21)),FuncDecl(Id('fact'),[VarDecl(Id('n'), [], None),VarDecl(Id('aca_312aAX'),[3,44,12799], None),VarDecl(Id('cxa'),[18,1,8,0], None)],([VarDecl(Id('t'), [], None),VarDecl(Id('r'), [],FloatLiteral(10.0)),VarDecl(Id('thread'), [],FloatLiteral('inf')),VarDecl(Id('r'), [],FloatLiteral(10.0))],[Assign(Id('v'),BinaryOp('*',BinaryOp('*',BinaryOp('*.',BinaryOp('*.',BinaryOp('\.',FloatLiteral(4.0),FloatLiteral(3.0)),FloatLiteral(3.14)),Id('r')),Id('r')),Id('a'))),Assign(Id('object'),BinaryOp('>',BinaryOp('+',IntLiteral(4123542),IntLiteral(7)),IntLiteral(4)))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 331))
    def test_case_33(self):
        input = """
        Function: main
        Body:
            If "" Then
                If 1 Then
                    inp = f23 + ads[2+10] --- 2 *f ** "87235jkfgshgsfg $&^# ** ;
                ElseIf 1 Then 
                EndIf.
            EndIf.
        EndBody.
        """
        expect = Program([FuncDecl(Id('main'), [],([],[If([(StringLiteral(""""""),[],[If([(IntLiteral(1),[],[Assign(Id('inp'),BinaryOp('-',BinaryOp('+',Id('f23'),ArrayCell(Id('ads'),[BinaryOp('+',IntLiteral(2),IntLiteral(10))])),BinaryOp('*',UnaryOp('-',UnaryOp('-',IntLiteral(2))),Id('f'))))]),(IntLiteral(1),[],[])], ([], []))])], ([], []))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 332))
    def test_case_34(self):
        input = """
		Var: x = 1,y= "abc",z[1];
		Var: temp = 0;
		Function: main
		Parameter: x,y,arr[10][12]
		Body:
			Var: x = 1;
			x = True && 1;
			Break;
			foo(1);
			Return x + 1;
		EndBody.
		"""
        expect = Program([VarDecl(Id('x'), [],IntLiteral(1)),VarDecl(Id('y'), [],StringLiteral("""abc""")),VarDecl(Id('z'), [1], None),VarDecl(Id('temp'), [],IntLiteral(0)),FuncDecl(Id('main'), [VarDecl(Id('x'), [], None),VarDecl(Id('y'), [], None),VarDecl(Id('arr'), [10,12], None)],([VarDecl(Id('x'), [],IntLiteral(1))],[Assign(Id('x'),BinaryOp('&&',BooleanLiteral(True),IntLiteral(1))),Break(),CallStmt(Id('foo'),[IntLiteral(1)]),Return(BinaryOp('+',Id('x'),IntLiteral(1)))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 333))
    def test_case_35(self):
        input = """
        Var: max_length = 100;
        Function: countintSort
        Parameter: arr[100]
        Body:
            Var: output[100];
            Var: count[100], i;
            memset(count, 0, sizeof(count));
            For(i = 0, arr[i] > 0, 1) Do
                count[arr[i]] = count[arr[i]] + 1;
            EndFor.
            For(i = 1, i <= range(arr), 1) Do
                count[i] = count[i] + count[i - 1];
            EndFor.
            For(i = 0, arr[i] > 0, 1) Do
                output[count[arr[i]] - 1] = arr[i];
                count[arr[i]] = count[arr[i]] - 1;
            EndFor.
            For( i = 0, arr[i] != 0, 1) Do
                If i % 2 == 0 Then
                    arr[i] = i \\ 2;
                ElseIf i % 3 == 0 Then
                    arr[i] = 3 *. i;
                ElseIf i % 5 == 1 Then
                    arr[i] = i;
                Else
                    arr[i] = output[i];
                EndIf.
            EndFor.
        EndBody.
        """
        expect = Program([VarDecl(Id('max_length'), [],IntLiteral(100)),FuncDecl(Id('countintSort'), [VarDecl(Id('arr'), [100], None)],([VarDecl(Id('output'), [100], None),VarDecl(Id('count'), [100], None),VarDecl(Id('i'), [], None)],[CallStmt(Id('memset'),[Id('count'),IntLiteral(0),CallExpr(Id('sizeof'),[Id('count')])]),For(Id('i'),IntLiteral(0),BinaryOp('>',ArrayCell(Id('arr'),[Id('i')]),IntLiteral(0)),IntLiteral(1), ([],[Assign(ArrayCell(Id('count'),[ArrayCell(Id('arr'),[Id('i')])]),BinaryOp('+',ArrayCell(Id('count'),[ArrayCell(Id('arr'),[Id('i')])]),IntLiteral(1)))])),For(Id('i'),IntLiteral(1),BinaryOp('<=',Id('i'),CallExpr(Id('range'),[Id('arr')])),IntLiteral(1), ([],[Assign(ArrayCell(Id('count'),[Id('i')]),BinaryOp('+',ArrayCell(Id('count'),[Id('i')]),ArrayCell(Id('count'),[BinaryOp('-',Id('i'),IntLiteral(1))])))])),For(Id('i'),IntLiteral(0),BinaryOp('>',ArrayCell(Id('arr'),[Id('i')]),IntLiteral(0)),IntLiteral(1), ([],[Assign(ArrayCell(Id('output'),[BinaryOp('-',ArrayCell(Id('count'),[ArrayCell(Id('arr'),[Id('i')])]),IntLiteral(1))]),ArrayCell(Id('arr'),[Id('i')])),Assign(ArrayCell(Id('count'),[ArrayCell(Id('arr'),[Id('i')])]),BinaryOp('-',ArrayCell(Id('count'),[ArrayCell(Id('arr'),[Id('i')])]),IntLiteral(1)))])),For(Id('i'),IntLiteral(0),BinaryOp('!=',ArrayCell(Id('arr'),[Id('i')]),IntLiteral(0)),IntLiteral(1), ([],[If([(BinaryOp('==',BinaryOp('%',Id('i'),IntLiteral(2)),IntLiteral(0)),[],[Assign(ArrayCell(Id('arr'),[Id('i')]),BinaryOp('\\',Id('i'),IntLiteral(2)))]),(BinaryOp('==',BinaryOp('%',Id('i'),IntLiteral(3)),IntLiteral(0)),[],[Assign(ArrayCell(Id('arr'),[Id('i')]),BinaryOp('*.',IntLiteral(3),Id('i')))]),(BinaryOp('==',BinaryOp('%',Id('i'),IntLiteral(5)),IntLiteral(1)),[],[Assign(ArrayCell(Id('arr'),[Id('i')]),Id('i'))])], ([],[Assign(ArrayCell(Id('arr'),[Id('i')]),ArrayCell(Id('output'),[Id('i')]))]))]))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 334))
    def test_case_36(self):
        input = """
        Var:x ;
        Var: f = 1232324.e23432;
        Function: main
        Parameter: a[2], b
        Body:
            While i < 10 Do
                While i < 10 Do
                    For (i = init(), con(), up()) Do
                    EndFor.
                EndWhile.
            EndWhile.
        EndBody."""
        expect = Program([VarDecl(Id('x'), [], None),VarDecl(Id('f'), [],FloatLiteral('inf')),FuncDecl(Id('main'), [VarDecl(Id('a'), [2], None),VarDecl(Id('b'), [], None)],([],[While(BinaryOp('<',Id('i'),IntLiteral(10)),([],[While(BinaryOp('<',Id('i'),IntLiteral(10)),([],[For(Id('i'),CallExpr(Id('init'),[]),CallExpr(Id('con'),[]),CallExpr(Id('up'),[]), ([],[]))]))]))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,335))
    def test_case_37(self):
        input = """Var:x;
        Function: test
        Body:
            f = -1234.;
            Do 
                Do
                    If k Then If k Then EndIf. EndIf.
                While False
                EndDo.
            While f < 10
            EndDo.
        EndBody."""
        expect = Program([VarDecl(Id('x'), [], None),FuncDecl(Id('test'), [],([],[Assign(Id('f'),UnaryOp('-',FloatLiteral(1234.0))),Dowhile(([],[Dowhile(([],[If([(Id('k'),[],[If([(Id('k'),[],[])], ([], []))])], ([], []))]),BooleanLiteral(False))]),BinaryOp('<',Id('f'),IntLiteral(10)))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,336))
    def test_case_38(self):
        input = """
        Var: s = "dad";
        Function: sum
        Body:
            Var: sum = 0.;
            For (i = init(i * init()), cond(c *. c() - c(c())), step(step - step(step \. step(step % step)))) Do
                sum = sum + random(randint(range(0, rand())));
            EndFor.
        EndBody.
        """
        expect = Program([VarDecl(Id('s'), [],StringLiteral("""dad""")),FuncDecl(Id('sum'), [],([VarDecl(Id('sum'), [],FloatLiteral(0.0))],[For(Id('i'),CallExpr(Id('init'),[BinaryOp('*',Id('i'),CallExpr(Id('init'),[]))]),CallExpr(Id('cond'),[BinaryOp('-',BinaryOp('*.',Id('c'),CallExpr(Id('c'),[])),CallExpr(Id('c'),[CallExpr(Id('c'),[])]))]),CallExpr(Id('step'),[BinaryOp('-',Id('step'),CallExpr(Id('step'),[BinaryOp('\.',Id('step'),CallExpr(Id('step'),[BinaryOp('%',Id('step'),Id('step'))]))]))]), ([],[Assign(Id('sum'),BinaryOp('+',Id('sum'),CallExpr(Id('random'),[CallExpr(Id('randint'),[CallExpr(Id('range'),[IntLiteral(0),CallExpr(Id('rand'),[])])])])))]))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,337))
    def test_case_39(self):
        input = """
        Var: s;
        Function: reverse
        Parameter: str
        Body:
            For(i = 0, i < len(str) \ 2, s) Do
                str[i] = str[len(str) - i - 1];
            EndFor.
        EndBody."""
        expect = Program([VarDecl(Id('s'), [], None),FuncDecl(Id('reverse'), [VarDecl(Id('str'), [], None)],([],[For(Id('i'),IntLiteral(0),BinaryOp('<',Id('i'),BinaryOp('\\',CallExpr(Id('len'),[Id('str')]),IntLiteral(2))),Id('s'), ([],[Assign(ArrayCell(Id('str'),[Id('i')]),ArrayCell(Id('str'),[BinaryOp('-',BinaryOp('-',CallExpr(Id('len'),[Id('str')]),Id('i')),IntLiteral(1))]))]))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,338))
    def test_case_40(self):
        input = """
        Var: ar[0x13][0o2][23];
        Function: ppl
        Parameter: threshold
        Body:
            If score >= threshold Then
                Return "Pass";
            Else
                Return "Again";
            EndIf.
            Return ppl;
        EndBody."""
        expect = Program([VarDecl(Id('ar'), [19,2,23], None),FuncDecl(Id('ppl'), [VarDecl(Id('threshold'), [], None)],([],[If([(BinaryOp('>=',Id('score'),Id('threshold')),[],[Return(StringLiteral("""Pass"""))])], ([],[Return(StringLiteral("""Again"""))])),Return(Id('ppl'))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,339))
    def test_case_41(self):
        input = """
        Function: dfff
        Body:
            Var: s[100];
            While !empty(s) Do
                print(pop(s));
            EndWhile.
            While !full(s) Do
                s = push(s, vr());
            EndWhile.
        EndBody."""
        expect = Program([FuncDecl(Id('dfff'), [],([VarDecl(Id('s'), [100], None)],[While(UnaryOp('!',CallExpr(Id('empty'),[Id('s')])),([],[CallStmt(Id('print'),[CallExpr(Id('pop'),[Id('s')])])])),While(UnaryOp('!',CallExpr(Id('full'),[Id('s')])),([],[Assign(Id('s'),CallExpr(Id('push'),[Id('s'),CallExpr(Id('vr'),[])]))]))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,340))
    def test_case_42(self):
        input = """
        Function: main
        Parameter: arr
        Body:
            print(1 + 2, 0x22)[f()[2][3+arr[3]]] = arr[2 * f()[f()]];
        EndBody.
        """
        expect = Program([FuncDecl(Id('main'), [VarDecl(Id('arr'), [], None)],([],[Assign(ArrayCell(CallExpr(Id('print'),[BinaryOp('+',IntLiteral(1),IntLiteral(2)),IntLiteral(34)]),[ArrayCell(CallExpr(Id('f'),[]),[IntLiteral(2),BinaryOp('+',IntLiteral(3),ArrayCell(Id('arr'),[IntLiteral(3)]))])]),ArrayCell(Id('arr'),[BinaryOp('*',IntLiteral(2),ArrayCell(CallExpr(Id('f'),[]),[CallExpr(Id('f'),[])]))]))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,341))
    def test_case_43(self):
        input = """
        Function: fn
        Body:
            f(f(2 + 2));
            If i == 0 Then
                If True Then
                    If t Then ElseIf con Then ElseIf con Then Else EndIf.
                EndIf.
            EndIf.
        EndBody.
        """
        expect = Program([FuncDecl(Id('fn'), [],([],[CallStmt(Id('f'),[CallExpr(Id('f'),[BinaryOp('+',IntLiteral(2),IntLiteral(2))])]),If([(BinaryOp('==',Id('i'),IntLiteral(0)),[],[If([(BooleanLiteral(True),[],[If([(Id('t'),[],[]),(Id('con'),[],[]),(Id('con'),[],[])], ([],[]))])], ([], []))])], ([], []))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,342))
    def test_case_44(self):
        input = """Var: x;
        Function: symmetry
        Body:
            Var: str = "";
            str = str(input());
            For(i = 0, i < len(str) \. 2, 1) Do
                If str[i] != str[len(str) - i - 1] Then
                    Return False;
                EndIf.
            EndFor.
            Return True;
            Return;
        EndBody.
        """
        expect = Program([VarDecl(Id('x'), [], None),FuncDecl(Id('symmetry'), [],([VarDecl(Id('str'), [],StringLiteral(""""""))],[Assign(Id('str'),CallExpr(Id('str'),[CallExpr(Id('input'),[])])),For(Id('i'),IntLiteral(0),BinaryOp('<',Id('i'),BinaryOp('\.',CallExpr(Id('len'),[Id('str')]),IntLiteral(2))),IntLiteral(1), ([],[If([(BinaryOp('!=',ArrayCell(Id('str'),[Id('i')]),ArrayCell(Id('str'),[BinaryOp('-',BinaryOp('-',CallExpr(Id('len'),[Id('str')]),Id('i')),IntLiteral(1))])),[],[Return(BooleanLiteral(False))])], ([], []))])),Return(BooleanLiteral(True)),Return(None)]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,343))
    def test_case_45(self):
        input = """Var: x;
        Function: test
        Body:
            While True Do
                v = receive(socket, max_len);
                If v Then
                    handle();
                Else
                    raise(error("failed"));
                EndIf.
            EndWhile.
        EndBody.
        """
        expect = Program([VarDecl(Id('x'), [], None),FuncDecl(Id('test'), [],([],[While(BooleanLiteral(True),([],[Assign(Id('v'),CallExpr(Id('receive'),[Id('socket'),Id('max_len')])),If([(Id('v'),[],[CallStmt(Id('handle'),[])])], ([],[CallStmt(Id('raise'),[CallExpr(Id('error'),[StringLiteral("""failed""")])])]))]))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,344))
    def test_case_46(self):
        input = """
        Var: b = False, arr[0o10] = {120, 0x123};
        Function: test
        Body:
            Do
                While True Do
                    lock();
                    send(i + 1);
                    unlock();
                EndWhile.
            While True EndDo.
        EndBody."""
        expect = Program([VarDecl(Id('b'), [],BooleanLiteral(False)),VarDecl(Id('arr'), [8],ArrayLiteral([IntLiteral(120),IntLiteral(291)])),FuncDecl(Id('test'), [],([],[Dowhile(([],[While(BooleanLiteral(True),([],[CallStmt(Id('lock'),[]),CallStmt(Id('send'),[BinaryOp('+',Id('i'),IntLiteral(1))]),CallStmt(Id('unlock'),[])]))]),BooleanLiteral(True))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,345))
    def test_case_47(self):
        input = """
        Var: kk = {123, 0x13, 0o13, "dasd", {}};
        Function: main
        Body:
            While exp == exp() && !error() Do
                print("kfkfkf" * 4);
                If cond() Then
                    process();
                    log();
                    Break;
                ElseIf k Then
                    handle();
                    error();
                    log();
                Else
                    log();
                    close();
                    finish();
                EndIf.
            EndWhile. 
        EndBody."""
        expect = Program([VarDecl(Id('kk'), [],ArrayLiteral([IntLiteral(123),IntLiteral(19),IntLiteral(11),StringLiteral("""dasd"""),ArrayLiteral([])])),FuncDecl(Id('main'), [],([],[While(BinaryOp('==',Id('exp'),BinaryOp('&&',CallExpr(Id('exp'),[]),UnaryOp('!',CallExpr(Id('error'),[])))),([],[CallStmt(Id('print'),[BinaryOp('*',StringLiteral("""kfkfkf"""),IntLiteral(4))]),If([(CallExpr(Id('cond'),[]),[],[CallStmt(Id('process'),[]),CallStmt(Id('log'),[]),Break()]),(Id('k'),[],[CallStmt(Id('handle'),[]),CallStmt(Id('error'),[]),CallStmt(Id('log'),[])])], ([],[CallStmt(Id('log'),[]),CallStmt(Id('close'),[]),CallStmt(Id('finish'),[])]))]))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,346))
    def test_case_48(self):
        input = """
        Var: x;
        Function: test
        Body:
            Var: x = 10;
            Var: mm[10] = {1, 0x123, 0o123, "dasd"};
            If k == 10 Then
                While True Do
                    move_left();
                    Do 
                        For(i = 0, i < upper(), step) Do
                            While k > 10 Do
                                print("das", 123, exp(p + 2));
                            EndWhile.
                        EndFor.
                    While k == True EndDo.
                EndWhile.
            EndIf.
        EndBody."""
        expect = Program([VarDecl(Id('x'), [], None),FuncDecl(Id('test'), [],([VarDecl(Id('x'), [],IntLiteral(10)),VarDecl(Id('mm'), [10],ArrayLiteral([IntLiteral(1),IntLiteral(291),IntLiteral(83),StringLiteral("""dasd""")]))],[If([(BinaryOp('==',Id('k'),IntLiteral(10)),[],[While(BooleanLiteral(True),([],[CallStmt(Id('move_left'),[]),Dowhile(([],[For(Id('i'),IntLiteral(0),BinaryOp('<',Id('i'),CallExpr(Id('upper'),[])),Id('step'), ([],[While(BinaryOp('>',Id('k'),IntLiteral(10)),([],[CallStmt(Id('print'),[StringLiteral("""das"""),IntLiteral(123),CallExpr(Id('exp'),[BinaryOp('+',Id('p'),IntLiteral(2))])])]))]))]),BinaryOp('==',Id('k'),BooleanLiteral(True)))]))])], ([], []))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,347))
    def test_case_49(self):
        input = """
        Var: var = {0o123, 123., 123e-1, "das", 0x123};
        Function: test
        Body:
            Var: x = 12;
            For(i = "dasd" * 12, "dasd", "d") Do
                Var: m = 10;
                If m != 10 Then
                    Var: x;
                    x = int(input());
                ElseIf m && False Then
                    Var: x;
                    print(x);
                Else
                    Do
                        Var: k;
                        k = int(input());
                        If k == 10 Then
                            Var: i;
                            Break;
                        EndIf.
                    While True EndDo.
                EndIf.
            EndFor.
        EndBody."""
        expect = Program([VarDecl(Id('var'), [],ArrayLiteral([IntLiteral(83),FloatLiteral(123.0),FloatLiteral(12.3),StringLiteral("""das"""),IntLiteral(291)])),FuncDecl(Id('test'), [],([VarDecl(Id('x'), [],IntLiteral(12))],[For(Id('i'),BinaryOp('*',StringLiteral("""dasd"""),IntLiteral(12)),StringLiteral("""dasd"""),StringLiteral("""d"""), ([VarDecl(Id('m'), [],IntLiteral(10))],[If([(BinaryOp('!=',Id('m'),IntLiteral(10)),[VarDecl(Id('x'), [], None)],[Assign(Id('x'),CallExpr(Id('int'),[CallExpr(Id('input'),[])]))]),(BinaryOp('&&',Id('m'),BooleanLiteral(False)),[VarDecl(Id('x'), [], None)],[CallStmt(Id('print'),[Id('x')])])], ([],[Dowhile(([VarDecl(Id('k'), [], None)],[Assign(Id('k'),CallExpr(Id('int'),[CallExpr(Id('input'),[])])),If([(BinaryOp('==',Id('k'),IntLiteral(10)),[VarDecl(Id('i'), [], None)],[Break()])], ([], []))]),BooleanLiteral(True))]))]))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,348))
    def test_case_50(self):
        input = """
        Function: test
        Parameter: a, b[10][0o12][0x43]
        Body:
            a[2 + f()[12] * ((adr[0o23] >=. d) -. 32)] = kh;
            flag = -. True && !f(2) % 2 || f == 32;
            While cond()[123][0x312][0o32] Do
                print("dasd");
            EndWhile.
        EndBody."""
        expect = Program([FuncDecl(Id('test'), [VarDecl(Id('a'), [], None),VarDecl(Id('b'), [10,10,67], None)],([],[Assign(ArrayCell(Id('a'),[BinaryOp('+',IntLiteral(2),BinaryOp('*',ArrayCell(CallExpr(Id('f'),[]),[IntLiteral(12)]),BinaryOp('-.',BinaryOp('>=.',ArrayCell(Id('adr'),[IntLiteral(19)]),Id('d')),IntLiteral(32))))]),Id('kh')),Assign(Id('flag'),BinaryOp('==',BinaryOp('||',BinaryOp('&&',UnaryOp('-.',BooleanLiteral(True)),BinaryOp('%',UnaryOp('!',CallExpr(Id('f'),[IntLiteral(2)])),IntLiteral(2))),Id('f')),IntLiteral(32))),While(ArrayCell(CallExpr(Id('cond'),[]),[IntLiteral(123),IntLiteral(786),IntLiteral(26)]),([],[CallStmt(Id('print'),[StringLiteral("""dasd""")])]))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,349))
    def test_case_51(self):
        input = """
        Function: test
        Body:
            For(i = f() * fp()[12][0x13], i < f()[13], fn(f)[0o123]) Do
                Var: x;
                If x == 1 Then f(); k = kad();
                ElseIf x Then 
                While i < -12 Do
                Var: m;
                EndWhile.
                EndIf.
            EndFor.
        EndBody."""
        expect = Program([FuncDecl(Id('test'), [],([],[For(Id('i'),BinaryOp('*',CallExpr(Id('f'),[]),ArrayCell(CallExpr(Id('fp'),[]),[IntLiteral(12),IntLiteral(19)])),BinaryOp('<',Id('i'),ArrayCell(CallExpr(Id('f'),[]),[IntLiteral(13)])),ArrayCell(CallExpr(Id('fn'),[Id('f')]),[IntLiteral(83)]), ([VarDecl(Id('x'), [], None)],[If([(BinaryOp('==',Id('x'),IntLiteral(1)),[],[CallStmt(Id('f'),[]),Assign(Id('k'),CallExpr(Id('kad'),[]))]),(Id('x'),[],[While(BinaryOp('<',Id('i'),UnaryOp('-',IntLiteral(12))),([VarDecl(Id('m'), [], None)],[]))])], ([], []))]))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,350))
    def test_case_52(self):
        input = """
        Function: test
        Body:
            Var: k;
            k = "13" + "das";
            k = k && 31 - 13 * (k == 0) || dask;
        EndBody."""
        expect = Program([FuncDecl(Id('test'), [],([VarDecl(Id('k'), [], None)],[Assign(Id('k'),BinaryOp('+',StringLiteral("""13"""),StringLiteral("""das"""))),Assign(Id('k'),BinaryOp('||',BinaryOp('&&',Id('k'),BinaryOp('-',IntLiteral(31),BinaryOp('*',IntLiteral(13),BinaryOp('==',Id('k'),IntLiteral(0))))),Id('dask')))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,351))
    def test_case_53(self):
        input = """
        Function: test
        Body:
            x = f == (d > 43)  \ (!-(4 =/= f(k + 2, k())) % 9 == 2);
            x = (!x || True) * kd[12] == 2 % 123 && False \ blala;
            Return;
        EndBody."""
        expect = Program([FuncDecl(Id('test'), [],([],[Assign(Id('x'),BinaryOp('==',Id('f'),BinaryOp('\\',BinaryOp('>',Id('d'),IntLiteral(43)),BinaryOp('==',BinaryOp('%',UnaryOp('!',UnaryOp('-',BinaryOp('=/=',IntLiteral(4),CallExpr(Id('f'),[BinaryOp('+',Id('k'),IntLiteral(2)),CallExpr(Id('k'),[])])))),IntLiteral(9)),IntLiteral(2))))),Assign(Id('x'),BinaryOp('==',BinaryOp('*',BinaryOp('||',UnaryOp('!',Id('x')),BooleanLiteral(True)),ArrayCell(Id('kd'),[IntLiteral(12)])),BinaryOp('&&',BinaryOp('%',IntLiteral(2),IntLiteral(123)),BinaryOp('\\',BooleanLiteral(False),Id('blala'))))),Return(None)]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,352))
    def test_case_54(self):
        input = """
        Function: test
        Body:
            Var: guard = 0;
            While guard Do
                a[i] = b +. 1.;
                If i % 2 Then
                    Do
                        x = test();
                    While (a >=. b) EndDo.
                ElseIf i Then
                    test()[123] = 123;
                EndIf.
            EndWhile.
        EndBody."""
        expect = Program([FuncDecl(Id('test'), [],([VarDecl(Id('guard'), [],IntLiteral(0))],[While(Id('guard'),([],[Assign(ArrayCell(Id('a'),[Id('i')]),BinaryOp('+.',Id('b'),FloatLiteral(1.0))),If([(BinaryOp('%',Id('i'),IntLiteral(2)),[],[Dowhile(([],[Assign(Id('x'),CallExpr(Id('test'),[]))]),BinaryOp('>=.',Id('a'),Id('b')))]),(Id('i'),[],[Assign(ArrayCell(CallExpr(Id('test'),[]),[IntLiteral(123)]),IntLiteral(123))])], ([], []))]))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,353))
    def test_case_55(self):
        input = """
        Function: test
        Parameter: a[132], b, c
        Body:
            Do
                print(a[12] + b);
                If isnull(a) Then
                    segmentfailure(error());
                ElseIf len(a) > 1 Then
                    Return {1, 2, 3} + test(a, 1, len(a));
                Else
                    Return {0};
                EndIf.
            While a =/= b EndDo.
        EndBody."""
        expect = Program([FuncDecl(Id('test'), [VarDecl(Id('a'), [132], None),VarDecl(Id('b'), [], None),VarDecl(Id('c'), [], None)],([],[Dowhile(([],[CallStmt(Id('print'),[BinaryOp('+',ArrayCell(Id('a'),[IntLiteral(12)]),Id('b'))]),If([(CallExpr(Id('isnull'),[Id('a')]),[],[CallStmt(Id('segmentfailure'),[CallExpr(Id('error'),[])])]),(BinaryOp('>',CallExpr(Id('len'),[Id('a')]),IntLiteral(1)),[],[Return(BinaryOp('+',ArrayLiteral([IntLiteral(1),IntLiteral(2),IntLiteral(3)]),CallExpr(Id('test'),[Id('a'),IntLiteral(1),CallExpr(Id('len'),[Id('a')])])))])], ([],[Return(ArrayLiteral([IntLiteral(0)]))]))]),BinaryOp('=/=',Id('a'),Id('b')))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,354))
    def test_case_56(self):
        input = """
        Function: ooooo
        Body:
            While !compile() Do EndWhile.
            While !linker() Do EndWhile.
            If flag Then loader(); Else fail(); EndIf.
            Return runner();
        EndBody."""
        expect = Program([FuncDecl(Id('ooooo'), [],([],[While(UnaryOp('!',CallExpr(Id('compile'),[])),([],[])),While(UnaryOp('!',CallExpr(Id('linker'),[])),([],[])),If([(Id('flag'),[],[CallStmt(Id('loader'),[])])], ([],[CallStmt(Id('fail'),[])])),Return(CallExpr(Id('runner'),[]))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,355))
    def test_case_57(self):
        input = """
        Function: fn
        Parameter: arr[0x123][0o13][312]
        Body:
            Var: hex = 0x123;
            For(i = f(), a(), s()[12]) Do
                fn(hex, fn(fn(s + 3, k * 123 || False == 321)));
            EndFor.
        EndBody."""
        expect = Program([FuncDecl(Id('fn'), [VarDecl(Id('arr'), [291,11,312], None)],([VarDecl(Id('hex'), [],IntLiteral(291))],[For(Id('i'),CallExpr(Id('f'),[]),CallExpr(Id('a'),[]),ArrayCell(CallExpr(Id('s'),[]),[IntLiteral(12)]), ([],[CallStmt(Id('fn'),[Id('hex'),CallExpr(Id('fn'),[CallExpr(Id('fn'),[BinaryOp('+',Id('s'),IntLiteral(3)),BinaryOp('==',BinaryOp('||',BinaryOp('*',Id('k'),IntLiteral(123)),BooleanLiteral(False)),IntLiteral(321))])])])]))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,356))
    def test_case_58(self):
        input = """
        Function: test
        Parameter: arr[1000]
        Body:
            If !len(arr) Then Return {}; EndIf.
            Return reduce(arr[0] + t(arr, 1), arr, {});
            Do
                Var: l = 0;
                l = print() * das;
                If l < 10 Then
                    Var: p;
                    If j < l Then
                        Var: op;
                        If l >=. 100 Then
                            print("Hello World!");
                        ElseIf l >. 50 Then
                            print("string string");
                        Else
                            print("-213++314");
                        EndIf.
                    EndIf.
                EndIf.
            While guard() EndDo.
        EndBody."""
        expect = Program([FuncDecl(Id('test'), [VarDecl(Id('arr'), [1000], None)],([],[If([(UnaryOp('!',CallExpr(Id('len'),[Id('arr')])),[],[Return(ArrayLiteral([]))])], ([], [])),Return(CallExpr(Id('reduce'),[BinaryOp('+',ArrayCell(Id('arr'),[IntLiteral(0)]),CallExpr(Id('t'),[Id('arr'),IntLiteral(1)])),Id('arr'),ArrayLiteral([])])),Dowhile(([VarDecl(Id('l'), [],IntLiteral(0))],[Assign(Id('l'),BinaryOp('*',CallExpr(Id('print'),[]),Id('das'))),If([(BinaryOp('<',Id('l'),IntLiteral(10)),[VarDecl(Id('p'), [], None)],[If([(BinaryOp('<',Id('j'),Id('l')),[VarDecl(Id('op'), [], None)],[If([(BinaryOp('>=.',Id('l'),IntLiteral(100)),[],[CallStmt(Id('print'),[StringLiteral("""Hello World!""")])]),(BinaryOp('>.',Id('l'),IntLiteral(50)),[],[CallStmt(Id('print'),[StringLiteral("""string string""")])])], ([],[CallStmt(Id('print'),[StringLiteral("""-213++314""")])]))])], ([], []))])], ([], []))]),CallExpr(Id('guard'),[]))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,357))
    def test_case_59(self):
        input = """
        Function: test
        Body:
            If n == 0 Then
                Return n;
            Else
                If test > 0 Then
                    print("akakakak");
                EndIf.
                Return n % 10 + test(n \ 10);
            EndIf.
        EndBody."""
        expect = Program([FuncDecl(Id('test'), [],([],[If([(BinaryOp('==',Id('n'),IntLiteral(0)),[],[Return(Id('n'))])], ([],[If([(BinaryOp('>',Id('test'),IntLiteral(0)),[],[CallStmt(Id('print'),[StringLiteral("""akakakak""")])])], ([], [])),Return(BinaryOp('+',BinaryOp('%',Id('n'),IntLiteral(10)),CallExpr(Id('test'),[BinaryOp('\\',Id('n'),IntLiteral(10))])))]))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,358))
    def test_case_60(self):
        input = """
        Function: mean
        Parameter: arr
        Body:
            If len(arr) == 0 Then Return; EndIf.
            m = mean(arr, axis, {1, 2, 3, 4, 5});
            Do
                mean(arr, 1, n, len(arr) - 1);
            While !((flag == False) || (flag != 23) * (flag <=. 123)) EndDo.
        EndBody."""
        expect = Program([FuncDecl(Id('mean'), [VarDecl(Id('arr'), [], None)],([],[If([(BinaryOp('==',CallExpr(Id('len'),[Id('arr')]),IntLiteral(0)),[],[Return(None)])], ([], [])),Assign(Id('m'),CallExpr(Id('mean'),[Id('arr'),Id('axis'),ArrayLiteral([IntLiteral(1),IntLiteral(2),IntLiteral(3),IntLiteral(4),IntLiteral(5)])])),Dowhile(([],[CallStmt(Id('mean'),[Id('arr'),IntLiteral(1),Id('n'),BinaryOp('-',CallExpr(Id('len'),[Id('arr')]),IntLiteral(1))])]),UnaryOp('!',BinaryOp('||',BinaryOp('==',Id('flag'),BooleanLiteral(False)),BinaryOp('*',BinaryOp('!=',Id('flag'),IntLiteral(23)),BinaryOp('<=.',Id('flag'),IntLiteral(123))))))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,359))
    def test_case_61(self):
        input = """
        Function: test
        Parameter: arr[0x1000], low, high
        Body:
            Var: min, max;
            For(i = 1, i < high, 1) Do
                For(j = 0, j < i, 1) Do
                    If arr[j] < min Then
                        min = arr[j];
                    ElseIf arr[j] > max Then
                        max = arr[j];
                    Else
                        print("************");
                        print("NO OPERATION");
                        print("************");
                    EndIf.
                    While min =/= max Do
                        Var: temp;
                        For(i = low, i < high, 1) Do
                            println(arr[i]);
                        EndFor.
                    EndWhile.
                EndFor.
            EndFor.
        EndBody."""
        expect = Program([FuncDecl(Id('test'), [VarDecl(Id('arr'), [4096], None),VarDecl(Id('low'), [], None),VarDecl(Id('high'), [], None)],([VarDecl(Id('min'), [], None),VarDecl(Id('max'), [], None)],[For(Id('i'),IntLiteral(1),BinaryOp('<',Id('i'),Id('high')),IntLiteral(1), ([],[For(Id('j'),IntLiteral(0),BinaryOp('<',Id('j'),Id('i')),IntLiteral(1), ([],[If([(BinaryOp('<',ArrayCell(Id('arr'),[Id('j')]),Id('min')),[],[Assign(Id('min'),ArrayCell(Id('arr'),[Id('j')]))]),(BinaryOp('>',ArrayCell(Id('arr'),[Id('j')]),Id('max')),[],[Assign(Id('max'),ArrayCell(Id('arr'),[Id('j')]))])], ([],[CallStmt(Id('print'),[StringLiteral("""************""")]),CallStmt(Id('print'),[StringLiteral("""NO OPERATION""")]),CallStmt(Id('print'),[StringLiteral("""************""")])])),While(BinaryOp('=/=',Id('min'),Id('max')),([VarDecl(Id('temp'), [], None)],[For(Id('i'),Id('low'),BinaryOp('<',Id('i'),Id('high')),IntLiteral(1), ([],[CallStmt(Id('println'),[ArrayCell(Id('arr'),[Id('i')])])]))]))]))]))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,360))
    def test_case_62(self):
        input = """
        Function: test
        Body:
            Var: flag;
            flag = (True != 123) + !3 * (False && kj % 123 <. f());
            praaa(--------.-.-(!123 == kk * 12 - 3)||False + !!!!!!9==4);
        EndBody."""
        expect = Program([FuncDecl(Id('test'), [],([VarDecl(Id('flag'), [], None)],[Assign(Id('flag'),BinaryOp('+',BinaryOp('!=',BooleanLiteral(True),IntLiteral(123)),BinaryOp('*',UnaryOp('!',IntLiteral(3)),BinaryOp('<.',BinaryOp('&&',BooleanLiteral(False),BinaryOp('%',Id('kj'),IntLiteral(123))),CallExpr(Id('f'),[]))))),CallStmt(Id('praaa'),[BinaryOp('==',BinaryOp('||',UnaryOp('-',UnaryOp('-',UnaryOp('-',UnaryOp('-',UnaryOp('-',UnaryOp('-',UnaryOp('-',UnaryOp('-.',UnaryOp('-.',UnaryOp('-',BinaryOp('==',UnaryOp('!',IntLiteral(123)),BinaryOp('-',BinaryOp('*',Id('kk'),IntLiteral(12)),IntLiteral(3))))))))))))),BinaryOp('+',BooleanLiteral(False),UnaryOp('!',UnaryOp('!',UnaryOp('!',UnaryOp('!',UnaryOp('!',UnaryOp('!',IntLiteral(9))))))))),IntLiteral(4))])]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,361))
    def test_case_63(self):
        input = """
        Function: test
        Parameter: str
        Body:
            Var: dt;
            For(i = 0, i < len(str), 1) Do
                dt[dt[dt[arr[i]]]] = dt[arr[dt[arr[i]]]] + 1;
                f(dt, k * {1, 2, 3, 4});
            EndFor.
        EndBody."""
        expect = Program([FuncDecl(Id('test'), [VarDecl(Id('str'), [], None)],([VarDecl(Id('dt'), [], None)],[For(Id('i'),IntLiteral(0),BinaryOp('<',Id('i'),CallExpr(Id('len'),[Id('str')])),IntLiteral(1), ([],[Assign(ArrayCell(Id('dt'),[ArrayCell(Id('dt'),[ArrayCell(Id('dt'),[ArrayCell(Id('arr'),[Id('i')])])])]),BinaryOp('+',ArrayCell(Id('dt'),[ArrayCell(Id('arr'),[ArrayCell(Id('dt'),[ArrayCell(Id('arr'),[Id('i')])])])]),IntLiteral(1))),CallStmt(Id('f'),[Id('dt'),BinaryOp('*',Id('k'),ArrayLiteral([IntLiteral(1),IntLiteral(2),IntLiteral(3),IntLiteral(4)]))])]))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,362))
    def test_case_64(self):
        input = """
        Var: x;
        Var: arr[123] = {1, 2, 3, 5, "dasd", {12, {12}}};
        Function: test
        Parameter: array
        Body:
            While array Do
                If arr Then
                    For(i = 0, i < length(arr), step()) Do
                        print(arr[i] * kk);
                    EndFor.
                    If True && (123 == 3123) Then
                        do();
                        Break;
                    EndIf.
                EndIf.
            EndWhile.
            Return;
        EndBody.
        """
        expect = Program([VarDecl(Id('x'), [], None),VarDecl(Id('arr'), [123],ArrayLiteral([IntLiteral(1),IntLiteral(2),IntLiteral(3),IntLiteral(5),StringLiteral("""dasd"""),ArrayLiteral([IntLiteral(12),ArrayLiteral([IntLiteral(12)])])])),FuncDecl(Id('test'), [VarDecl(Id('array'), [], None)],([],[While(Id('array'),([],[If([(Id('arr'),[],[For(Id('i'),IntLiteral(0),BinaryOp('<',Id('i'),CallExpr(Id('length'),[Id('arr')])),CallExpr(Id('step'),[]), ([],[CallStmt(Id('print'),[BinaryOp('*',ArrayCell(Id('arr'),[Id('i')]),Id('kk'))])])),If([(BinaryOp('&&',BooleanLiteral(True),BinaryOp('==',IntLiteral(123),IntLiteral(3123))),[],[CallStmt(Id('do'),[]),Break()])], ([], []))])], ([], []))])),Return(None)]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,363))
    def test_case_65(self):
        input = """
        Function: test
        Body:
            Var: kASKHD0123;
            Do
                Var: l123OKKD;
                While l123OKDS Do
                    print()[13] = {1,2,3,4,5,6,7,8,9};
                EndWhile.
            While False EndDo.
        EndBody.
        """
        expect = Program([FuncDecl(Id('test'), [],([VarDecl(Id('kASKHD0123'), [], None)],[Dowhile(([VarDecl(Id('l123OKKD'), [], None)],[While(Id('l123OKDS'),([],[Assign(ArrayCell(CallExpr(Id('print'),[]),[IntLiteral(13)]),ArrayLiteral([IntLiteral(1),IntLiteral(2),IntLiteral(3),IntLiteral(4),IntLiteral(5),IntLiteral(6),IntLiteral(7),IntLiteral(8),IntLiteral(9)]))]))]),BooleanLiteral(False))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,364))
    def test_case_66(self):
        input = ""
        expect = Program([])
        self.assertTrue(TestAST.checkASTGen(input,expect,365))
    def test_case_67(self):
        input = """
        Function: test
        Body:
            For(i = 0, i < 100, up()) Do
                If i % 2 == 0 Then
                    Break;
                    Continue;
                ElseIf i > 10 Then
                    w(i);
                EndIf.
            EndFor.
        EndBody."""
        expect = Program([FuncDecl(Id('test'), [],([],[For(Id('i'),IntLiteral(0),BinaryOp('<',Id('i'),IntLiteral(100)),CallExpr(Id('up'),[]), ([],[If([(BinaryOp('==',BinaryOp('%',Id('i'),IntLiteral(2)),IntLiteral(0)),[],[Break(),Continue()]),(BinaryOp('>',Id('i'),IntLiteral(10)),[],[CallStmt(Id('w'),[Id('i')])])], ([], []))]))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,366))
    def test_case_68(self):
        input = """
        Function: swap
        Parameter: a, b
        Body:
            Var: temp;
            temp = a;
            a = b;
            b = temp;
        EndBody."""
        expect = Program([FuncDecl(Id('swap'), [VarDecl(Id('a'), [], None),VarDecl(Id('b'), [], None)],([VarDecl(Id('temp'), [], None)],[Assign(Id('temp'),Id('a')),Assign(Id('a'),Id('b')),Assign(Id('b'),Id('temp'))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,367))
    def test_case_69(self):
        input = """
        Function: max
        Parameter: x, y
        Body:
            If x > y Then
                Return x;
            Else
                Return y;
            EndIf.
        EndBody.
        Function: main
        Body:
            Var: a = 10, b = 20;
            print("%d", max(a, b));
            Return;
        EndBody."""
        expect = Program([FuncDecl(Id('max'), [VarDecl(Id('x'), [], None),VarDecl(Id('y'), [], None)],([],[If([(BinaryOp('>',Id('x'),Id('y')),[],[Return(Id('x'))])], ([],[Return(Id('y'))]))])),FuncDecl(Id('main'), [],([VarDecl(Id('a'), [],IntLiteral(10)),VarDecl(Id('b'), [],IntLiteral(20))],[CallStmt(Id('print'),[StringLiteral("""%d"""),CallExpr(Id('max'),[Id('a'),Id('b')])]),Return(None)]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,368))
    def test_case_70(self):
        input = """
        Function: test
        Body:
            Var: x = 1;
            print("kdkd");
            If (((((x < 0))))) Then
                throw(x);
            EndIf.
        EndBody.
        Function: fun
        Parameter: ptr, x
        Body:
            If null(ptr) Then
                throw(ptr);
            ElseIf x == 0 Then
                throw(x);
            EndIf.
        EndBody."""
        expect = Program([FuncDecl(Id('test'), [],([VarDecl(Id('x'), [],IntLiteral(1))],[CallStmt(Id('print'),[StringLiteral("""kdkd""")]),If([(BinaryOp('<',Id('x'),IntLiteral(0)),[],[CallStmt(Id('throw'),[Id('x')])])], ([], []))])),FuncDecl(Id('fun'), [VarDecl(Id('ptr'), [], None),VarDecl(Id('x'), [], None)],([],[If([(CallExpr(Id('null'),[Id('ptr')]),[],[CallStmt(Id('throw'),[Id('ptr')])]),(BinaryOp('==',Id('x'),IntLiteral(0)),[],[CallStmt(Id('throw'),[Id('x')])])], ([], []))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,369))
    def test_case_71(self):
        input = """
        Function: test
        Parameter: k, a
        Body:
            Var: str = "this is a string";
            Var: token;
            token = strtok(str, "-");
            While ((token != null)) Do
                printf("%s", token);
                token = strtok(str, "-");
            EndWhile.
        EndBody."""
        expect = Program([FuncDecl(Id('test'), [VarDecl(Id('k'), [], None),VarDecl(Id('a'), [], None)],([VarDecl(Id('str'), [],StringLiteral("""this is a string""")),VarDecl(Id('token'), [], None)],[Assign(Id('token'),CallExpr(Id('strtok'),[Id('str'),StringLiteral("""-""")])),While(BinaryOp('!=',Id('token'),Id('null')),([],[CallStmt(Id('printf'),[StringLiteral("""%s"""),Id('token')]),Assign(Id('token'),CallExpr(Id('strtok'),[Id('str'),StringLiteral("""-""")]))]))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,370))
    def test_case_72(self):
        input = """
        Function: print
        Parameter: i
        Body:
            print(i);
        EndBody.
        Function: main
        Body:
            print(i);
        EndBody.
        """
        expect = Program([FuncDecl(Id('print'), [VarDecl(Id('i'), [], None)],([],[CallStmt(Id('print'),[Id('i')])])),FuncDecl(Id('main'), [],([],[CallStmt(Id('print'),[Id('i')])]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,371))
    def test_case_73(self):
        input = """
        Function: test
        Body:
            For(i = 0, i < max, i) Do
                If (i % 7 == 0) && (i % 5 != 0) Then
                    arr = arr + {1};
                EndIf.
            EndFor.
            print(join("", arr));
        EndBody."""
        expect = Program([FuncDecl(Id('test'), [],([],[For(Id('i'),IntLiteral(0),BinaryOp('<',Id('i'),Id('max')),Id('i'), ([],[If([(BinaryOp('&&',BinaryOp('==',BinaryOp('%',Id('i'),IntLiteral(7)),IntLiteral(0)),BinaryOp('!=',BinaryOp('%',Id('i'),IntLiteral(5)),IntLiteral(0))),[],[Assign(Id('arr'),BinaryOp('+',Id('arr'),ArrayLiteral([IntLiteral(1)])))])], ([], []))])),CallStmt(Id('print'),[CallExpr(Id('join'),[StringLiteral(""""""),Id('arr')])])]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,372))
    def test_case_74(self):
        input = """
        Function: test
        Body:
            For(i = 0, i < max, 1) Do
                If is_upper(s[i]) Then
                    d["upper"] = d["upper"] + 1;
                ElseIf is_lower(get(s, i)) Then
                    d["lower"] = d["lower"] + 1;
                Else
                    Continue;
                EndIf.
            EndFor.
        EndBody."""
        expect = Program([FuncDecl(Id('test'), [],([],[For(Id('i'),IntLiteral(0),BinaryOp('<',Id('i'),Id('max')),IntLiteral(1), ([],[If([(CallExpr(Id('is_upper'),[ArrayCell(Id('s'),[Id('i')])]),[],[Assign(ArrayCell(Id('d'),[StringLiteral("""upper""")]),BinaryOp('+',ArrayCell(Id('d'),[StringLiteral("""upper""")]),IntLiteral(1)))]),(CallExpr(Id('is_lower'),[CallExpr(Id('get'),[Id('s'),Id('i')])]),[],[Assign(ArrayCell(Id('d'),[StringLiteral("""lower""")]),BinaryOp('+',ArrayCell(Id('d'),[StringLiteral("""lower""")]),IntLiteral(1)))])], ([],[Continue()]))]))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,373))
    def test_case_75(self):
        input = """
        Function: test
        Body:
            While True Do
                Var: arr;
                s = input("Enter a string");
                If !s Then Break; EndIf.
                arr = split(s, " ");
                operation = arr[0];
                amount = int_of_string(operation);
                If operation == "A" Then
                    amount = amount + 10;
                EndIf.
            EndWhile.
        EndBody."""
        expect = Program([FuncDecl(Id('test'), [],([],[While(BooleanLiteral(True),([VarDecl(Id('arr'), [], None)],[Assign(Id('s'),CallExpr(Id('input'),[StringLiteral("""Enter a string""")])),If([(UnaryOp('!',Id('s')),[],[Break()])], ([], [])),Assign(Id('arr'),CallExpr(Id('split'),[Id('s'),StringLiteral(""" """)])),Assign(Id('operation'),ArrayCell(Id('arr'),[IntLiteral(0)])),Assign(Id('amount'),CallExpr(Id('int_of_string'),[Id('operation')])),If([(BinaryOp('==',Id('operation'),StringLiteral("""A""")),[],[Assign(Id('amount'),BinaryOp('+',Id('amount'),IntLiteral(10)))])], ([], []))]))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,374))
    def test_case_76(self):
        input = """
        Function: test
        Body:
            While True Do
                s = str(input());
                If len(s) == 0 Then
                    Continue;
                EndIf.
                arr[arr + i] = append(split(arr, " "));
            EndWhile.
        EndBody."""
        expect = Program([FuncDecl(Id('test'), [],([],[While(BooleanLiteral(True),([],[Assign(Id('s'),CallExpr(Id('str'),[CallExpr(Id('input'),[])])),If([(BinaryOp('==',CallExpr(Id('len'),[Id('s')]),IntLiteral(0)),[],[Continue()])], ([], [])),Assign(ArrayCell(Id('arr'),[BinaryOp('+',Id('arr'),Id('i'))]),CallExpr(Id('append'),[CallExpr(Id('split'),[Id('arr'),StringLiteral(""" """)])]))]))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,375))
    def test_case_77(self):
        input = """
        Function: test
        Parameter: str
        Body:
            l = split(str, " ");
            If !l Then print("empty string"); EndIf.
            Return array(l);
        EndBody."""
        expect = Program([FuncDecl(Id('test'), [VarDecl(Id('str'), [], None)],([],[Assign(Id('l'),CallExpr(Id('split'),[Id('str'),StringLiteral(""" """)])),If([(UnaryOp('!',Id('l')),[],[CallStmt(Id('print'),[StringLiteral("""empty string""")])])], ([], [])),Return(CallExpr(Id('array'),[Id('l')]))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,376))
    def test_case_78(self):
        input = """
        Function: square
        Parameter: num
        Body:
            rand();
            sleep(random(randint(max) % int(1e10)));
            Return num * num;
        EndBody.
        Function: main
        Body:
            print(square(10));
        EndBody."""
        expect = Program([FuncDecl(Id('square'), [VarDecl(Id('num'), [], None)],([],[CallStmt(Id('rand'),[]),CallStmt(Id('sleep'),[CallExpr(Id('random'),[BinaryOp('%',CallExpr(Id('randint'),[Id('max')]),CallExpr(Id('int'),[FloatLiteral(10000000000.0)]))])]),Return(BinaryOp('*',Id('num'),Id('num')))])),FuncDecl(Id('main'), [],([],[CallStmt(Id('print'),[CallExpr(Id('square'),[IntLiteral(10)])])]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,377))
    def test_case_79(self):
        input = """
        Function: huber
        Parameter: y, x, fn, theta
        Body:
            Var: sum = 0.;
            sum = mean(abs(y - fn(x)), "mean");
            If sum <= theta Then
                Return mean(square(y - fn(x)), "mean") \. 2;
            Else
                Return theta * abs(y - fn(x)) - theta * theta \. 2;
            EndIf.
        EndBody."""
        expect = Program([FuncDecl(Id('huber'), [VarDecl(Id('y'), [], None),VarDecl(Id('x'), [], None),VarDecl(Id('fn'), [], None),VarDecl(Id('theta'), [], None)],([VarDecl(Id('sum'), [],FloatLiteral(0.0))],[Assign(Id('sum'),CallExpr(Id('mean'),[CallExpr(Id('abs'),[BinaryOp('-',Id('y'),CallExpr(Id('fn'),[Id('x')]))]),StringLiteral("""mean""")])),If([(BinaryOp('<=',Id('sum'),Id('theta')),[],[Return(BinaryOp('\.',CallExpr(Id('mean'),[CallExpr(Id('square'),[BinaryOp('-',Id('y'),CallExpr(Id('fn'),[Id('x')]))]),StringLiteral("""mean""")]),IntLiteral(2)))])], ([],[Return(BinaryOp('-',BinaryOp('*',Id('theta'),CallExpr(Id('abs'),[BinaryOp('-',Id('y'),CallExpr(Id('fn'),[Id('x')]))])),BinaryOp('\.',BinaryOp('*',Id('theta'),Id('theta')),IntLiteral(2))))]))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,378))
    def test_case_80(self):
        input = """
        Function: mse
        Parameter: a, b
        Body:
            Var: sum = 0.;
            If len(a) =/= len(b) Then raise(error()); EndIf.
            For(i = 0, i < len(a), 1) Do
                sum = sum + (a[i] - b[i]) * (a[i] - b[i]);
            EndFor.
            print(sum * sum \. 2);
        EndBody.
        """
        expect = Program([FuncDecl(Id('mse'), [VarDecl(Id('a'), [], None),VarDecl(Id('b'), [], None)],([VarDecl(Id('sum'), [],FloatLiteral(0.0))],[If([(BinaryOp('=/=',CallExpr(Id('len'),[Id('a')]),CallExpr(Id('len'),[Id('b')])),[],[CallStmt(Id('raise'),[CallExpr(Id('error'),[])])])], ([], [])),For(Id('i'),IntLiteral(0),BinaryOp('<',Id('i'),CallExpr(Id('len'),[Id('a')])),IntLiteral(1), ([],[Assign(Id('sum'),BinaryOp('+',Id('sum'),BinaryOp('*',BinaryOp('-',ArrayCell(Id('a'),[Id('i')]),ArrayCell(Id('b'),[Id('i')])),BinaryOp('-',ArrayCell(Id('a'),[Id('i')]),ArrayCell(Id('b'),[Id('i')])))))])),CallStmt(Id('print'),[BinaryOp('\.',BinaryOp('*',Id('sum'),Id('sum')),IntLiteral(2))])]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,379))
    def test_case_81(self):
        input = """
        Var: arr[10][0o10] = {{1,2,3,4}, {1,2,3}, {2,3,4}};
        Function: main
        Body:
            For(i = 0, i < getlength(arr, axis(0)), 1) Do
                Var: j = 0;
                While (isvalid(arr, axis(1), j)) Do
                    print(arr[i][j] * 10);
                    j = j + 1;
                EndWhile.
            EndFor.
        EndBody."""
        expect = Program([VarDecl(Id('arr'), [10,8],ArrayLiteral([ArrayLiteral([IntLiteral(1),IntLiteral(2),IntLiteral(3),IntLiteral(4)]),ArrayLiteral([IntLiteral(1),IntLiteral(2),IntLiteral(3)]),ArrayLiteral([IntLiteral(2),IntLiteral(3),IntLiteral(4)])])),FuncDecl(Id('main'), [],([],[For(Id('i'),IntLiteral(0),BinaryOp('<',Id('i'),CallExpr(Id('getlength'),[Id('arr'),CallExpr(Id('axis'),[IntLiteral(0)])])),IntLiteral(1), ([VarDecl(Id('j'), [],IntLiteral(0))],[While(CallExpr(Id('isvalid'),[Id('arr'),CallExpr(Id('axis'),[IntLiteral(1)]),Id('j')]),([],[CallStmt(Id('print'),[BinaryOp('*',ArrayCell(Id('arr'),[Id('i'),Id('j')]),IntLiteral(10))]),Assign(Id('j'),BinaryOp('+',Id('j'),IntLiteral(1)))]))]))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,380))
    def test_case_82(self):
        input = """
        Function: is_even
        Parameter: x
        Body:
            If x && 1 == 0 Then
                Return True;
            EndIf.
            Return False;
        EndBody."""
        expect = Program([FuncDecl(Id('is_even'), [VarDecl(Id('x'), [], None)],([],[If([(BinaryOp('==',BinaryOp('&&',Id('x'),IntLiteral(1)),IntLiteral(0)),[],[Return(BooleanLiteral(True))])], ([], [])),Return(BooleanLiteral(False))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,381))
    def test_case_83(self):
        input = """
        Function: test
        Body:
            Return "dasd" * asd  - {1,2,3} || 82 == False;
        EndBody."""
        expect = Program([FuncDecl(Id('test'), [],([],[Return(BinaryOp('==',BinaryOp('||',BinaryOp('-',BinaryOp('*',StringLiteral("""dasd"""),Id('asd')),ArrayLiteral([IntLiteral(1),IntLiteral(2),IntLiteral(3)])),IntLiteral(82)),BooleanLiteral(False)))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,382))
    def test_case_84(self):
        input = """
        Function: t____
        Parameter: n
        Body:
            create(size, {400, 400});
            For(i = enum(), isend(i), steps(iter())) Do
                sub(n, 1, i + 1);
                im = coverted(read("path", "w"), type);
                b = im[1];
                While b Do
                    im = draw(im, figure);
                    pop(p, rand());
                EndWhile.
            EndFor.
        EndBody.
        """
        expect = Program([FuncDecl(Id('t____'), [VarDecl(Id('n'), [], None)],([],[CallStmt(Id('create'),[Id('size'),ArrayLiteral([IntLiteral(400),IntLiteral(400)])]),For(Id('i'),CallExpr(Id('enum'),[]),CallExpr(Id('isend'),[Id('i')]),CallExpr(Id('steps'),[CallExpr(Id('iter'),[])]), ([],[CallStmt(Id('sub'),[Id('n'),IntLiteral(1),BinaryOp('+',Id('i'),IntLiteral(1))]),Assign(Id('im'),CallExpr(Id('coverted'),[CallExpr(Id('read'),[StringLiteral("""path"""),StringLiteral("""w""")]),Id('type')])),Assign(Id('b'),ArrayCell(Id('im'),[IntLiteral(1)])),While(Id('b'),([],[Assign(Id('im'),CallExpr(Id('draw'),[Id('im'),Id('figure')])),CallStmt(Id('pop'),[Id('p'),CallExpr(Id('rand'),[])])]))]))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,383))
    def test_case_85(self):
        input = """
        Var: k = False;
        Var: str = "no thing";
        Var: d = 123;
        Function: t___k
        Body:
        EndBody."""
        expect = Program([VarDecl(Id('k'), [],BooleanLiteral(False)),VarDecl(Id('str'), [],StringLiteral("""no thing""")),VarDecl(Id('d'), [],IntLiteral(123)),FuncDecl(Id('t___k'), [],([],[]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,384))
    def test_case_86(self):
        input = """
        Function: mmmmmmm
        Body:
            For(i = 0, i < len(row), 1) Do
                For(j = 0, i < len(col), 1) Do
                    result[i][j] = row[i] * col[j];
                EndFor.
            EndFor.
        EndBody."""
        expect = Program([FuncDecl(Id('mmmmmmm'), [],([],[For(Id('i'),IntLiteral(0),BinaryOp('<',Id('i'),CallExpr(Id('len'),[Id('row')])),IntLiteral(1), ([],[For(Id('j'),IntLiteral(0),BinaryOp('<',Id('i'),CallExpr(Id('len'),[Id('col')])),IntLiteral(1), ([],[Assign(ArrayCell(Id('result'),[Id('i'),Id('j')]),BinaryOp('*',ArrayCell(Id('row'),[Id('i')]),ArrayCell(Id('col'),[Id('j')])))]))]))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,385))
    def test_case_87(self):
        input = """
        Var: arr[100];
        Var: x;
        Function: binary_search
        Parameter: low, high
        Body:
            Var: mid;
            If low > high Then Return False; EndIf.
            mid = (low + high) \ 2;
            If (arr[mid] == x) Then Return False; EndIf.
            If (arr[mid] < x) Then
                Return binary_search(mid + 1, high);
            Else
                Return binary_search(low, mid - 1);
            EndIf.
        EndBody."""
        expect = Program([VarDecl(Id('arr'), [100], None),VarDecl(Id('x'), [], None),FuncDecl(Id('binary_search'), [VarDecl(Id('low'), [], None),VarDecl(Id('high'), [], None)],([VarDecl(Id('mid'), [], None)],[If([(BinaryOp('>',Id('low'),Id('high')),[],[Return(BooleanLiteral(False))])], ([], [])),Assign(Id('mid'),BinaryOp('\\',BinaryOp('+',Id('low'),Id('high')),IntLiteral(2))),If([(BinaryOp('==',ArrayCell(Id('arr'),[Id('mid')]),Id('x')),[],[Return(BooleanLiteral(False))])], ([], [])),If([(BinaryOp('<',ArrayCell(Id('arr'),[Id('mid')]),Id('x')),[],[Return(CallExpr(Id('binary_search'),[BinaryOp('+',Id('mid'),IntLiteral(1)),Id('high')]))])], ([],[Return(CallExpr(Id('binary_search'),[Id('low'),BinaryOp('-',Id('mid'),IntLiteral(1))]))]))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,386))
    def test_case_88(self):
        input = """
        Function: is_valid_index
        Parameter: arr[10], max_length, index
        Body:
            If index >= max_length Then raise(error());
            Else
                Return arr[index];
            EndIf.
        EndBody."""
        expect = Program([FuncDecl(Id('is_valid_index'), [VarDecl(Id('arr'), [10], None),VarDecl(Id('max_length'), [], None),VarDecl(Id('index'), [], None)],([],[If([(BinaryOp('>=',Id('index'),Id('max_length')),[],[CallStmt(Id('raise'),[CallExpr(Id('error'),[])])])], ([],[Return(ArrayCell(Id('arr'),[Id('index')]))]))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,387))
    def test_case_89(self):
        input = """
        Function: no_ideas
        Body:
            If x % 2 == y % f() Then
                print(a[2]);
            ElseIf f() % g(f()) > f() * 12 - f[123] Then
            ElseIf x % 12 == 1 Then
            EndIf.
        EndBody."""
        expect = Program([FuncDecl(Id('no_ideas'), [],([],[If([(BinaryOp('==',BinaryOp('%',Id('x'),IntLiteral(2)),BinaryOp('%',Id('y'),CallExpr(Id('f'),[]))),[],[CallStmt(Id('print'),[ArrayCell(Id('a'),[IntLiteral(2)])])]),(BinaryOp('>',BinaryOp('%',CallExpr(Id('f'),[]),CallExpr(Id('g'),[CallExpr(Id('f'),[])])),BinaryOp('-',BinaryOp('*',CallExpr(Id('f'),[]),IntLiteral(12)),ArrayCell(Id('f'),[IntLiteral(123)]))),[],[]),(BinaryOp('==',BinaryOp('%',Id('x'),IntLiteral(12)),IntLiteral(1)),[],[])], ([], []))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,388))
    def test_case_90(self):
        input = """
        Var: x, y, z, t;
        Function: test___
        Body:
            Var: a, b, c;
            Var: ksd[123][0x10][0o231340];
            Var: s = "132";
            Var: f = 0x13, sd = 123, s = "ad", k = 0.123, u = {1, 2, 4, 5, 6};
        EndBody.
        """
        expect = Program([VarDecl(Id('x'), [], None),VarDecl(Id('y'), [], None),VarDecl(Id('z'), [], None),VarDecl(Id('t'), [], None),FuncDecl(Id('test___'), [],([VarDecl(Id('a'), [], None),VarDecl(Id('b'), [], None),VarDecl(Id('c'), [], None),VarDecl(Id('ksd'), [123,16,78560], None),VarDecl(Id('s'), [],StringLiteral("""132""")),VarDecl(Id('f'), [],IntLiteral(19)),VarDecl(Id('sd'), [],IntLiteral(123)),VarDecl(Id('s'), [],StringLiteral("""ad""")),VarDecl(Id('k'), [],FloatLiteral(0.123)),VarDecl(Id('u'), [],ArrayLiteral([IntLiteral(1),IntLiteral(2),IntLiteral(4),IntLiteral(5),IntLiteral(6)]))],[]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,389))
    def test_case_91(self):
        input = """
        Var: x;
        Function: m
        Body:
            Break;
        EndBody.
        """
        expect = Program([VarDecl(Id('x'), [], None),FuncDecl(Id('m'), [],([],[Break()]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,390))
    def test_case_92(self):
        input = """
        Function: m
        Body:
            f = (a + f(2 + 3, f + 2) * (f)[f((f[0]))[t]])[123] - 123;
            a[2 + f()] = f(f * k(a[0]));
            f()[2 + f()[2]] = "dasf" + f(2, 3 - f[2])[2];
            Continue;
        EndBody."""
        expect = Program([FuncDecl(Id('m'), [],([],[Assign(Id('f'),BinaryOp('-',ArrayCell(BinaryOp('+',Id('a'),BinaryOp('*',CallExpr(Id('f'),[BinaryOp('+',IntLiteral(2),IntLiteral(3)),BinaryOp('+',Id('f'),IntLiteral(2))]),ArrayCell(Id('f'),[ArrayCell(CallExpr(Id('f'),[ArrayCell(Id('f'),[IntLiteral(0)])]),[Id('t')])]))),[IntLiteral(123)]),IntLiteral(123))),Assign(ArrayCell(Id('a'),[BinaryOp('+',IntLiteral(2),CallExpr(Id('f'),[]))]),CallExpr(Id('f'),[BinaryOp('*',Id('f'),CallExpr(Id('k'),[ArrayCell(Id('a'),[IntLiteral(0)])]))])),Assign(ArrayCell(CallExpr(Id('f'),[]),[BinaryOp('+',IntLiteral(2),ArrayCell(CallExpr(Id('f'),[]),[IntLiteral(2)]))]),BinaryOp('+',StringLiteral("""dasf"""),ArrayCell(CallExpr(Id('f'),[IntLiteral(2),BinaryOp('-',IntLiteral(3),ArrayCell(Id('f'),[IntLiteral(2)]))]),[IntLiteral(2)]))),Continue()]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,391))
    def test_case_93(self):
        input = """
        Function: blink
        Body:
            sys_call(3 * 2, sys(delete("path")));
            print();
            function();
            If "" Then EndIf.
        EndBody."""
        expect = Program([FuncDecl(Id('blink'), [],([],[CallStmt(Id('sys_call'),[BinaryOp('*',IntLiteral(3),IntLiteral(2)),CallExpr(Id('sys'),[CallExpr(Id('delete'),[StringLiteral("""path""")])])]),CallStmt(Id('print'),[]),CallStmt(Id('function'),[]),If([(StringLiteral(""""""),[],[])], ([], []))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,392))
    def test_case_94(self):
        input = """
        Function: test
        Body:
            print();
        EndBody.
        Function: fn1
        Body: runfn(); EndBody.
        Function: fn2
        Body: EndBody.
        Function: main
        Body: Return test() + fn1() + fn2(); EndBody."""
        expect = Program([FuncDecl(Id('test'), [],([],[CallStmt(Id('print'),[])])),FuncDecl(Id('fn1'), [],([],[CallStmt(Id('runfn'),[])])),FuncDecl(Id('fn2'), [],([],[])),FuncDecl(Id('main'), [],([],[Return(BinaryOp('+',BinaryOp('+',CallExpr(Id('test'),[]),CallExpr(Id('fn1'),[])),CallExpr(Id('fn2'),[])))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,393))
    def test_case_95(self):
        input = """
        Function: t__________________________
        Body:
            Var: y;
            k = 120;
            x[12] = 123;
            x = {1, 2, 3, 4, {4, 5}, {{{{{}}}}}};
        EndBody."""
        expect = Program([FuncDecl(Id('t__________________________'), [],([VarDecl(Id('y'), [], None)],[Assign(Id('k'),IntLiteral(120)),Assign(ArrayCell(Id('x'),[IntLiteral(12)]),IntLiteral(123)),Assign(Id('x'),ArrayLiteral([IntLiteral(1),IntLiteral(2),IntLiteral(3),IntLiteral(4),ArrayLiteral([IntLiteral(4),IntLiteral(5)]),ArrayLiteral([ArrayLiteral([ArrayLiteral([ArrayLiteral([ArrayLiteral([])])])])])]))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,394))
    def test_case_96(self):
        input = """
        Function: tEEEEEEEEEEEEEE
        Body:
            While rand() Do
                print(rand());
            EndWhile.
        EndBody."""
        expect = Program([FuncDecl(Id('tEEEEEEEEEEEEEE'), [],([],[While(CallExpr(Id('rand'),[]),([],[CallStmt(Id('print'),[CallExpr(Id('rand'),[])])]))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,395))
    def test_case_97(self):
        input = """
        Function: testttt
        Body:
            For(iter = 0, iter < max_iter, 1) Do
                If do_some_thing() == end Then
                    Return;
                EndIf.
                Continue; 
            EndFor.
        EndBody."""
        expect = Program([FuncDecl(Id('testttt'), [],([],[For(Id('iter'),IntLiteral(0),BinaryOp('<',Id('iter'),Id('max_iter')),IntLiteral(1), ([],[If([(BinaryOp('==',CallExpr(Id('do_some_thing'),[]),Id('end')),[],[Return(None)])], ([], [])),Continue()]))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,396))
    def test_case_98(self):
        input = """Var: t;
        Function: t__Ddas
        Body:
            x = 2 -. 3 -. 4 + 123 + ((f() == 23) || 123) * 24 % (2 == 22);
        EndBody."""
        expect = Program([VarDecl(Id('t'), [], None),FuncDecl(Id('t__Ddas'), [],([],[Assign(Id('x'),BinaryOp('+',BinaryOp('+',BinaryOp('-.',BinaryOp('-.',IntLiteral(2),IntLiteral(3)),IntLiteral(4)),IntLiteral(123)),BinaryOp('%',BinaryOp('*',BinaryOp('||',BinaryOp('==',CallExpr(Id('f'),[]),IntLiteral(23)),IntLiteral(123)),IntLiteral(24)),BinaryOp('==',IntLiteral(2),IntLiteral(22)))))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,397))
    def test_case_99(self):
        input = """
        Function: t_2937124
        Parameter: arr[100]
        Body:
            Var: sum = 0;
            create_multi_threads(num_threads);
            For (i = 0, i < len, 1) Do
                lock();
                sum = sum + arr[i];
                unlock();
            EndFor.
            destroy_all_resources();
        EndBody."""
        expect = Program([FuncDecl(Id('t_2937124'), [VarDecl(Id('arr'), [100], None)],([VarDecl(Id('sum'), [],IntLiteral(0))],[CallStmt(Id('create_multi_threads'),[Id('num_threads')]),For(Id('i'),IntLiteral(0),BinaryOp('<',Id('i'),Id('len')),IntLiteral(1), ([],[CallStmt(Id('lock'),[]),Assign(Id('sum'),BinaryOp('+',Id('sum'),ArrayCell(Id('arr'),[Id('i')]))),CallStmt(Id('unlock'),[])])),CallStmt(Id('destroy_all_resources'),[])]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,398))
    def test_case_100(self):
        input = """
        Var: a, b = 120, c = "123", d[10] = {1,2,5};
        Var: f = {12, 3,4, {{}}};
        Function: test_
        Parameter: flag
        Body:
            If flag[0] && 1 Then
                For(i = 0, i < upp(upp(i)), s()) Do
                    update(f, i, d[i]);
                EndFor.
            ElseIf flag[2] && 2 Then
                Return;
            ElseIf all(flag, {0,1,2,3,4,5,6}) Then
                test_(flag[i]);
            ElseIf !flag Then
                Break;
            ElseIf is___(flag) Then
                flag = flag * ad - 123 + {1,2} % "124";
            Else
                println("da");
                delete(flag);
            EndIf.
        EndBody.
        Function: main
        Parameter: flags[100], len
        Body:
            For(i = 0, i < len, 1) Do
                test_(flags[i]);
            EndFor.
            Return 0;
        EndBody."""
        expect = Program([VarDecl(Id('a'), [], None),VarDecl(Id('b'), [],IntLiteral(120)),VarDecl(Id('c'), [],StringLiteral("""123""")),VarDecl(Id('d'), [10],ArrayLiteral([IntLiteral(1),IntLiteral(2),IntLiteral(5)])),VarDecl(Id('f'), [],ArrayLiteral([IntLiteral(12),IntLiteral(3),IntLiteral(4),ArrayLiteral([ArrayLiteral([])])])),FuncDecl(Id('test_'), [VarDecl(Id('flag'), [], None)],([],[If([(BinaryOp('&&',ArrayCell(Id('flag'),[IntLiteral(0)]),IntLiteral(1)),[],[For(Id('i'),IntLiteral(0),BinaryOp('<',Id('i'),CallExpr(Id('upp'),[CallExpr(Id('upp'),[Id('i')])])),CallExpr(Id('s'),[]), ([],[CallStmt(Id('update'),[Id('f'),Id('i'),ArrayCell(Id('d'),[Id('i')])])]))]),(BinaryOp('&&',ArrayCell(Id('flag'),[IntLiteral(2)]),IntLiteral(2)),[],[Return(None)]),(CallExpr(Id('all'),[Id('flag'),ArrayLiteral([IntLiteral(0),IntLiteral(1),IntLiteral(2),IntLiteral(3),IntLiteral(4),IntLiteral(5),IntLiteral(6)])]),[],[CallStmt(Id('test_'),[ArrayCell(Id('flag'),[Id('i')])])]),(UnaryOp('!',Id('flag')),[],[Break()]),(CallExpr(Id('is___'),[Id('flag')]),[],[Assign(Id('flag'),BinaryOp('+',BinaryOp('-',BinaryOp('*',Id('flag'),Id('ad')),IntLiteral(123)),BinaryOp('%',ArrayLiteral([IntLiteral(1),IntLiteral(2)]),StringLiteral("""124"""))))])], ([],[CallStmt(Id('println'),[StringLiteral("""da""")]),CallStmt(Id('delete'),[Id('flag')])]))])),FuncDecl(Id('main'), [VarDecl(Id('flags'), [100], None),VarDecl(Id('len'), [], None)],([],[For(Id('i'),IntLiteral(0),BinaryOp('<',Id('i'),Id('len')),IntLiteral(1), ([],[CallStmt(Id('test_'),[ArrayCell(Id('flags'),[Id('i')])])])),Return(IntLiteral(0))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,399))
    def test_case_101(self):
        input = """
        Var: x;
        Var: y = 2;
        Function: main
        Body:
            While i Do
            EndWhile.
        EndBody.
        """
        expect = Program([VarDecl(Id('x'), [], None),VarDecl(Id('y'), [],IntLiteral(2)),FuncDecl(Id('main'), [],([],[While(Id('i'),([],[]))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 400))
    def test_case_102(self):
        input = """
        Var: x;
        Var: y = 2;
        Function: main
        Body:
            While y == 2 Do
                Var: i;
                For(i = 1, i < 2, y) Do
                    Break;
                EndFor.
                Break;
            EndWhile.
            Break;
        EndBody.
        """
        expect = Program([VarDecl(Id('x'), [], None),VarDecl(Id('y'), [],IntLiteral(2)),FuncDecl(Id('main'), [],([],[While(BinaryOp('==',Id('y'),IntLiteral(2)),([VarDecl(Id('i'), [], None)],[For(Id('i'),IntLiteral(1),BinaryOp('<',Id('i'),IntLiteral(2)),Id('y'), ([],[Break()])),Break()])),Break()]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 401))
    def test_case_103(self):
        input = """
        Var: x;
        Var: y = 2;
        Function: main
        Body:
            While y == 2 Do
                Var: i;
                For(i = 1, i < 2, y) Do
                    Break;
                EndFor.
            EndWhile.
        EndBody.
        """
        expect = Program([VarDecl(Id('x'), [], None),VarDecl(Id('y'), [],IntLiteral(2)),FuncDecl(Id('main'), [],([],[While(BinaryOp('==',Id('y'),IntLiteral(2)),([VarDecl(Id('i'), [], None)],[For(Id('i'),IntLiteral(1),BinaryOp('<',Id('i'),IntLiteral(2)),Id('y'), ([],[Break()]))]))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 402))
    def test_case_104(self):
        input = """
        Var: x;
        Var: y = 2;
        Function: main
        Body:
            Var: x = {{1, 2}, {2, 3}};
        EndBody.
        """
        expect =  Program([VarDecl(Id('x'), [], None),VarDecl(Id('y'), [],IntLiteral(2)),FuncDecl(Id('main'), [],([VarDecl(Id('x'), [],ArrayLiteral([ArrayLiteral([IntLiteral(1),IntLiteral(2)]),ArrayLiteral([IntLiteral(2),IntLiteral(3)])]))],[]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 403))
    def test_case_105(self):
        input = """
        Var: x, y = 12;
        Function: main
        Parameter: a[10]
        Body:
            x = 2 + test(12);
        EndBody.
        Function: test
        Parameter: n
        Body:
            n = 0x1;
            printStrLn(read());
        EndBody.
        """
        expect = ''
        self.assertTrue(TestAST.checkASTGen(input, expect, 404))
    