"""Generate standalone MOV programs. All memory addresses stay below 512."""
from pathlib import Path


def save(problem, lines):
    Path('code').mkdir(exist_ok=True)
    Path(f'code/{problem}.mv').write_text('\n'.join(lines) + '\n')
    print(problem, len(lines), 'instructions')


save(2276, [f'O<{c}' for c in b'Hello World!'] + ['Z<1'])
save(2277, ['A<I', 'B<I', '[A]<48', '[B]<49', 'O<[A]', 'Z<1'])
save(2278, [f'[{48+i}]<{48+(i+1)%10}' for i in range(10)]
     + ['A<I', 'O<[A]', 'Z<1'])
save(2279, ['A<I', '[A]<0', '[0]<1', 'Z<[A]', 'O<A'])

# Reuse one lookup region for the three decimal positions.
p = ['A<I']
for position in (100, 10, 1):
    for c in range(128):
        value = 48 + (c // position) % 10 if c >= position or position == 1 else 0
        if value or position != 100:
            p.append(f'[{c}]<{value}')
    p.append('O<[A]')
save(2280, p + ['Z<1'])

# Addition is performed from right to left with a one-bit carry.
p = [f'[{96+i}]<{i}' for i in range(19)]
p += [f'[{i}]<{i}' for i in range(1, 20)]
p += [f'[{128+i}]<{48+i%10}' for i in range(20)]
p += [f'[{160+i}]<{i//10}' for i in range(10, 20)]
digits = 'ABCDEFGHJK'
p += [f'{r}<I' for r in digits] + ['M<I']
p += [f'[{300+i}]<I' for i in range(10)]
for i in reversed(range(10)):
    p += [f'M<[{300+i}]', f'S<[{digits[i]}+M]', 'T<[S+L]',
          f'[{300+i}]<[T+128]', 'L<[T+160]']
# Suppress leading zeroes, but always print the units digit.
p += ['[200]<0', '[201]<49', 'O<[L+200]', 'N<L', '[48]<0']
p += [f'[{i}]<{i}' for i in range(49, 58)]
for i in range(9):
    p += [f'A<[{300+i}]', '[N+48]<48', 'O<[A]', 'N<[A]']
p += ['O<[309]', 'Z<1']
save(2281, p)

# Counting sort. EOF reads update only an unused dummy counter.
p = [f'[{128+i}]<{max(0,i-1)}' for i in range(2, 6)]
p += [f'[{140+i}]<{i+1}' for i in range(6)]
p += [f'[{160+i}]<{48+i}' for i in range(10)]
p += [f'[{180+i}]<{i+1}' for i in range(10)]
p += ['[210]<1']
for _ in range(5):
    p += ['A<I', 'B<[A]', '[A]<[B+140]']
p += ['A<[D+48]', '[300]<[D+160]', '[A+300]<0', 'O<[300]',
      '[D+48]<[A+128]', '[320]<D', '[A+320]<[D+180]',
      'D<[320]', 'Z<[D+200]']
save(2282, p)
