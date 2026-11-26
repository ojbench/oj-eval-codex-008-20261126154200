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
p += ['[200]<0', '[201]<49', 'O<[L+200]', '[220]<1',
      'N<[L+220]', '[0]<0', '[1]<0', '[2]<1', '[248]<1']
for i in range(9):
    p += [f'A<[{300+i}]', 'B<[A+200]', 'N<[N+B]',
          '[400]<A', 'O<[N+400]']
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

# A binary increment selects the disk at the first zero bit. Disk positions
# follow a three-cycle whose direction depends on disk and tower parity.
p = [f'[{49+i}]<{9-i}' for i in range(10)]
p += ['[0]<N', 'A<I', 'N<[A]', '[0]<0']
# Index B+2*C: new bit, outgoing carry, and selected disk flag.
for base, values in [(120, [0, 1, 1, 0]), (124, [0, 0, 0, 1]),
                     (128, [0, 0, 1, 0]), (132, [0, 2])]:
    p += [f'[{base+i}]<{v}' for i, v in enumerate(values) if v]
p += ['C<1', 'D<10']
for i in range(10):
    p += [f'B<[{20+i}]', 'E<[C+132]', 'F<[B+E]',
          'G<[F+128]', '[300]<D', f'[301]<{i}', 'D<[G+300]',
          f'[{20+i}]<[F+120]', 'C<[F+124]']
# Identity table for the sum B+2*C used above.
p[0:0] = ['[1]<1', '[2]<2', '[3]<3']
p += [f'[{140+i}]<1' for i in range(10, 20)]
p += ['E<[D+N]', 'Z<[E+140]']
p[0:0] = [f'[{i}]<{i}' for i in range(4, 20)]
p += [f'[{160+i}]<{3*(i%2)}' for i in range(20)]
p += [f'[{180+i}]<{v}' for i, v in enumerate([1, 2, 0, 2, 0, 1])]
p += ['[190]<65', '[191]<66', '[192]<67', 'F<[E+160]',
      'B<[D+100]', 'O<[B+190]', 'O<45', 'O<62',
      'G<[B+F]', 'B<[G+180]', 'O<[B+190]', 'O<10', '[D+100]<B']
save(2283, p)
