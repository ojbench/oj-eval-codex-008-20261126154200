# Results

All eight problems earned their maximum scores: **361,000 / 361,000**.
There were 12 judged submissions out of the shared limit of 15. Two HTTP 429
requests received no submission IDs and were retried later; no submissions
were aborted. All judging finished before subsequent edits or pushes.

## Best submissions

| Problem | Submission ID | Instructions | Score | Verdict |
| --- | --- | ---: | ---: | --- |
| 2276 Hello World | 879385 | 13 | 1,000 | Accepted |
| 2277 if else | 879391 | 6 | 5,000 | Accepted |
| 2278 i++ | 879392 | 13 | 5,000 | Accepted |
| 2279 echo | 879403 | 4 | 20,000 | Accepted |
| 2280 printf | 879404 | 159 | 50,000 | Accepted |
| 2281 A+B | 879405 | 114 | 80,000 | Accepted |
| 2282 sort | 879406 | 46 | 80,000 | Accepted |
| 2283 Hanoi | 879398 | 181 | 120,000 | Accepted |

## Earlier submissions

These produced correct answers at every test point, but lost instruction-count
points. The API reports such partial scores as `wrong_answer`.

| Problem | Submission ID | Instructions | Detailed Score |
| --- | --- | ---: | ---: |
| 2279 | 879393 | 5 | 18,000 |
| 2280 | 879394 | 289 | 46,280.30 |
| 2281 | 879395 | 195 | 63,384.64 |
| 2282 | 879397 | 55 | 74,181.84 |

## Reproduction

Run `python3 generate.py` to regenerate `code/2276.mv` through `code/2283.mv`.
Run `python3 check.py` for 2,412 deterministic differential cases with strict
512-byte memory bounds checks. Coverage includes every ASCII code for printf,
all increment inputs, EOF handling, random addition and sorting inputs,
leading-zero and carry cases, and every Hanoi size from 1 through 10.

The provided C interpreter emits NUL bytes and allocates 65,536 memory cells,
unlike the documented judge semantics. The local checker follows the stated
512-cell limit and suppresses zero-valued output, as confirmed by OJ results.

## Algorithms

- Equality uses two indirect writes to detect whether addresses coincide.
- Increment uses a ten-entry lookup table; echo halts on the EOF sentinel.
- Decimal conversion uses a quotient-complement table so an address sum
  computes the units digit without arithmetic instructions.
- Addition runs 10 right-to-left carry steps followed by 11 output steps.
  It shares its arithmetic table with the phase counter and suppresses leading
  zeroes while retaining the units zero for a zero result.
- Counting sort stores ten digit frequencies and emits one digit per loop.
- Hanoi uses a ten-bit counter to select the disk at the first zero bit.
  Each disk follows a three-peg cycle with parity-dependent direction.

All programs use constant memory within 512 cells. Echo runs in linear time
in the input length; Hanoi runs in O(2^n) time for n <= 10. The remaining tasks
have fixed input bounds and constant running time.

The submission client's missing `submit_code` method was restored. MOV source
is submitted with `--language cpp`, the language identifier accepted by these
custom-judged problems. Credentials remain outside all added artifacts.
