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
save(2279, ['[0]<1', 'A<I', 'O<A', 'Z<[A]'])

# The quotient table also supplies the complement needed for the remainder.
p = [f'[{c}]<{128-10*(c//10)}' for c in range(128)]
p += [f'[{128-10*q+140}]<49' for q in range(10,13)]
p += [f'[{128-10*q+256}]<{48+q%10}' for q in range(1,13)]
p += [f'[{128+i}]<{48+i}' for i in range(10)]
p += ['A<I', 'B<[A]', 'O<[B+140]', 'O<[B+256]', 'O<[A+B]', 'Z<1']
save(2280, p)

# Addition and output run in separate phases of a small state machine.
p = [f'[{96+i}]<{i}' for i in range(1,19)]
p += [f'[{128+i}]<{48+i%10}' for i in range(20)]
p += [f'[{160+i}]<{i//10}' for i in range(10, 20)]
p += ['[200]<128', '[201]<129', '[202]<160', '[203]<161']
p += [f'[{220+i}]<{i+1}' for i in range(21)]
p += ['[260]<153'] + [f'[{250+i}]<{144-i}' for i in range(11,21)]
p += ['[510]<1', '[280]<0', '[281]<49']
p += [f'[{i}]<{i}' for i in range(49,58)]
p += [f'[P+{309-i}]<I' for i in range(10)] + ['A<I']
p += [f'[P+{329-i}]<I' for i in range(10)] + ['P<40']
p += ['A<[X+300]', 'B<[X+320]', 'S<[A+B]', 'L<[C+200]',
      '[X+400]<[S+L]', 'L<[C+202]', 'C<[S+L]',
      '[X+420]<[C+280]', 'Q<[X+250]', 'A<[Q+276]',
      '[450]<48', '[N+450]<0', '[48]<[450]', '[X+28]<48', 'N<[A]',
      'O<N', 'X<[X+220]', 'Z<[X+489]']
save(2281, p)

# Counting sort. EOF reads update only an unused dummy counter.
p = [f'[{128+i}]<{max(0,i-1)}' for i in range(2, 6)]
p += [f'[{140+i}]<{i+1}' for i in range(6)]
p += ['[180]<48'] + [f'[{180+i}]<{i+1}' for i in range(48,58)]
p += ['[458]<1']
for _ in range(5):
    p += ['A<I', 'B<[A+256]', '[A+256]<[B+140]']
p += ['A<[D+256]', '[350]<D', '[A+350]<0', 'O<[350]',
      '[D+256]<[A+128]', '[370]<D', '[A+370]<[D+180]',
      'D<[370]', 'Z<[D+400]']
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
