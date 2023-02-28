from antlr4 import *
from funxLexer import funxLexer
from funxParser import funxParser
from flask import Flask, render_template, request

if __name__ is not None and "." in __name__:
    from .funxParser import funxParser
    from .funxVisitor import funxVisitor
else:
    from funxParser import funxParser
    from funxVisitor import funxVisitor


d = {'+': lambda x, y: x + y, '-': lambda x, y: x - y, '*': lambda x, y: x * y, '/': lambda x, y: x//y, '^': lambda x, y: x ** y, '%': lambda x, y: x % y,
     '==': lambda x, y: x == y, '!=': lambda x, y: x != y, '<': lambda x, y: x < y, '>': lambda x, y: x > y, '<=': lambda x, y: x <= y, '>=': lambda x, y: x >= y,
     'and': lambda x, y: x and y, 'or': lambda x, y: x or y, 'xor': lambda x, y: ((x and not y) or (not x and y)), 'not': lambda x: not x,
     '->': lambda x, y: not x or y, '<->': lambda x, y: x == y}


class EvalVisitor(funxVisitor):

    def __init__(self, ts=[{}], tf={}, error="", localFuncs=[{}]):
        self.ts = ts
        self.tf = tf
        self.error = error
        self.localFuncs = localFuncs

    def visitRoot(self, ctx):
        children = list(ctx.getChildren())
        for elem in children[:-2]:
            self.visit(elem)
        return self.visit(children[-2])

    def visitBin(self, ctx):
        children = list(ctx.getChildren())
        op = children[1].getText()
        x = self.visit(children[0])
        y = self.visit(children[2])
        if (y == 0 and op == '/'):
            self.error = "Division by 0"
            raise Exception(self.error)
        return (d[op])(x, y)

    def visitValor(self, ctx):
        children = list(ctx.getChildren())
        return int(children[0].getText())

    def visitPar(self, ctx):
        children = list(ctx.getChildren())
        return self.visit(children[1])

    def visitAssig(self, ctx):
        children = list(ctx.getChildren())
        self.ts[-1][children[0].getText()] = self.visit(children[2])

    def visitVariable(self, ctx):
        children = list(ctx.getChildren())
        var = children[0].getText()
        if var not in self.ts[-1]:
            return 0
        return self.ts[-1][var]

    def visitComparison(self, ctx):
        children = list(ctx.getChildren())
        op = children[1].getText()
        x = self.visit(children[0])
        y = self.visit(children[2])
        return (d[op])(x, y)

    def visitNegation(self, ctx):
        children = list(ctx.getChildren())
        x = self.visit(children[1])
        return not x

    def visitBoolPar(self, ctx):
        children = list(ctx.getChildren())
        return self.visit(children[1])

    def visitConditional(self, ctx):
        children = list(ctx.getChildren())
        cond = self.visit(children[1])
        if cond:
            return self.visit(children[2])

        elif len(children) == 5:
            return self.visit(children[4])

    def visitWhile(self, ctx):
        children = list(ctx.getChildren())
        while self.visit(children[1]):
            stat = self.visit(children[2])
            if stat is not None:
                return stat

    def visitBloc(self, ctx):
        children = list(ctx.getChildren())
        for x in children:
            stat = self.visit(x)
            if stat is not None:
                return stat

    def visitFunc(self, ctx):
        children = list(ctx.getChildren())
        funcId = children[0].getText()
        if funcId in self.tf:
            self.error = funcId + " is already defined"
            raise Exception(self.error)

        param = [x.getText() for x in children[1:-1]]
        if len(param) != len(set(param)):
            self.error = "Duplicated names"
            raise Exception(self.error)

        self.tf[funcId] = (param, children[-1])

    def visitCall(self, ctx):
        children = list(ctx.getChildren())
        funcId = children[0].getText()
        self.error = ""
        if funcId not in self.localFuncs[-1]:
            if funcId not in self.tf:
                self.error = funcId + " is not defined"
                raise Exception(self.error)

        tsAux = {}
        tfAux = {}
        if funcId in self.localFuncs[-1]:
            (paramNames, bloc) = self.localFuncs[-1][funcId]
        else:
            (paramNames, bloc) = self.tf[funcId]

        if len(children[1:]) != len(paramNames):
            self.error = "Incorrect number of parameters"
            raise Exception(self.error)

        for i in range(0, len(paramNames)):
            callVarName = children[i + 1].getText()
            if (paramNames[i][0]).isupper():
                if not (callVarName in self.tf or callVarName in self.localFuncs[-1]):
                    self.error = callVarName + " has to be a defined function"
                    raise Exception(self.error)

                if callVarName in self.localFuncs[-1]:
                    tfAux[paramNames[i]] = self.localFuncs[-1][children[i + 1].getText()]
                else:
                    tfAux[paramNames[i]] = self.tf[children[i + 1].getText()]

            else:
                tsAux[paramNames[i]] = self.visit(children[i + 1])

        self.ts.append(tsAux)
        self.localFuncs.append(tfAux)
        result = self.visit(bloc)
        del self.ts[-1]
        del self.localFuncs[-1]

        return result

    def visitNegative(self, ctx):
        children = list(ctx.getChildren())
        x = self.visit(children[1])
        return (-x)


eval = EvalVisitor()


def run(inp):
    inputStream = InputStream(inp)
    lexer = funxLexer(inputStream)
    token_stream = CommonTokenStream(lexer)
    parser = funxParser(token_stream)
    tree = parser.root()
    return eval.visitRoot(tree)


app = Flask(__name__)
results = []


@app.route('/')
def index():
    lastRes = results[-5:]
    lastRes.reverse()
    return render_template('base.html', results=results, functions=eval.tf)


@app.route('/execute', methods=['POST', 'GET'])
def execute():
    if request.method == 'GET':
        lastRes = results[-5:]
        lastRes.reverse()
        return render_template('base.html', results=results, functions=eval.tf)

    code = request.form['code']
    err = None

    try:
        result = run(code)

    except Exception:
        result = None
        err = eval.error

    if (result is not None):
        results.append((code, result))

    lastRes = results[-5:]
    lastRes.reverse()
    return render_template('base.html', results=lastRes, functions=eval.tf, error=err)


if __name__ == '__main__':
    app.run(debug=True)
