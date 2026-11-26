"""Strict 512-byte MOV emulator and deterministic differential tests."""
import random
import re
from pathlib import Path


def operand(s):
    if s.startswith('['):
        return ('mem', [int(t) if t.isdigit() else t for t in s[1:-1].split('+')])
    return ('imm', int(s)) if s.isdigit() else ('reg', s)


def compile_program(problem):
    return [tuple(map(operand, line.split('<'))) for line in
            Path(f'code/{problem}.mv').read_text().splitlines()
            if line and not line.startswith('#')]


def run(code, data):
    mem = [0] * 512
    reg = dict.fromkeys('ABCDEFGHIJKLMNOPQRSTUVWXYZ', 0)
    inp = iter(data)
    out = bytearray()
    def address(parts):
        a = sum(t if isinstance(t, int) else reg[t] for t in parts)
        assert 0 <= a < 512, a
        return a
    for cycle in range(10000):
        for (dk, d), (sk, s) in code:
            v = s if sk == 'imm' else (mem[address(s)] if sk == 'mem' else
                (next(inp, 0) if s == 'I' else reg[s]))
            if dk == 'mem':
                mem[address(d)] = v
            elif d == 'Z':
                if v:
                    return bytes(out)
            elif d == 'O':
                if v:
                    out.append(v)
            else:
                reg[d] = v
    raise AssertionError('program did not halt')


def hanoi(n, a=65, b=66, c=67):
    if not n:
        return b''
    return hanoi(n-1, a, c, b) + bytes([a,45,62,c,10]) + hanoi(n-1,b,a,c)


def main():
    random.seed(8)
    count = 0
    def check(p, data, expected):
        nonlocal count
        actual = run(programs[p], data)
        assert actual == expected, (p, data, actual[:100], expected[:100])
        count += 1
    programs = {p: compile_program(p) for p in range(2276, 2284)}
    check(2276, b'', b'Hello World!')
    for a in range(128):
        for b in (a, (a+1)%128):
            check(2277, bytes([a,b]), b'1' if a == b else b'0')
        check(2280, bytes([a]), str(a).encode())
    for a in range(10):
        check(2278, bytes([48+a]), bytes([48+(a+1)%10]))
    for data in (b'', b'hello\n', bytes(range(1,128))):
        check(2279, data, data)
    for a,b in [(0,0),(1,0),(9999999999,1),(9999999999,9999999999)] + [
            (random.randrange(10**10), random.randrange(10**10)) for _ in range(1000)]:
        check(2281, f'{a:010}+{b:010}'.encode(), str(a+b).encode())
    for _ in range(1000):
        data = bytes(random.randrange(48,58) for _ in range(5))
        check(2282, data, bytes(sorted(data)))
    for n in range(1,11):
        check(2283, bytes([48+n]), hanoi(n))
    print(f'Passed {count} differential cases with bounds checks.')


if __name__ == '__main__':
    main()
