#!/usr/bin/env python3
'''
Markov's Normal Algoritms interpreter
'''
import re
# TODO: AL emulator compatibility mode

class NAM:
    sep: str = "\n"
    sub: str = "->"
    fin: str = "=>"
    gap: str = r"\s*"
    com: str = "# "
    alp: str = r"\S*"
    prog: dict = {}

    def __init__(self, text, sep=sep, sub=sub, fin=fin, gap=gap, com=com, alp=alp):
        self.sep, self.sub, self.fin, self.gap, self.com, self.alp = sep, sub, fin, gap, com, alp
        self.rule = re.compile(rf"({alp}){gap}({sub}|{fin}){gap}({alp})(?:\s+{com}.*)?|({com}.*)?")
        self.parse(text)

    def parse(self, text):
        for line in map(str.strip, text.split(self.sep)):
            left, op, right, comm = self.rule.fullmatch(line).groups()
            if op:
                self.prog[left] = (right, op == self.sub)

    def __call__(self, word):
        op = True
        while op:
            for left, (right, op) in self.prog.items():
                if left in word:
                    newword = word.replace(left, right, 1)
                    upword = yield word, self._rulestr(left, op, right), newword
                    print("@@", word, upword, newword)
                    word = upword or newword
                    break
            else:
                break
        return newword

    def _rulestr(self, left, op, right):
        return f"{left} {self.fin if op else self.sub} {right}"

    def __str__(self):
        return self.sep.join(self._rulestr(left, op, right) for left, (right, op) in self.prog.items())
