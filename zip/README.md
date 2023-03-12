# zip

TL;DR, write a `zip`-like utility that compresses ASCII files using a specified [Run-length encoding](https://en.wikipedia.org/wiki/Run-length_encoding) scheme and output to STDOUT.

## Change Log
- 2023-03-11: 
  - Added `e2e_test.py` for basic test cases
  - Added `2023-03-11-tested-zip.c` for implementation which passes basic test cases
- 2023-01-27: Refactored implementation for better legibility
- 2018: Original Implementation

## Upcoming Changes

1. [IN PROGRESS] Larger set of test cases for correctness
2. Writing to other output streams
3. Files which are too large to fit in memory
4. Supporting utf-8 or utf-16 encoding schemes. 
   - Look into [setlocale()](https://en.cppreference.com/w/c/locale/setlocale)
5. Memory safety
6. Performance. Look into [Valgrind](https://valgrind.org/). What about [perf](https://perf.wiki.kernel.org/index.php/Tutorial)?
   - Latency
   - Memory footprint
   - CPU instructions. Look into [gprof](https://sourceware.org/binutils/docs-2.37/gprof/index.html)
7. Unit tests using the [cmocka](https://cmocka.org/) testing framework.

## zip Program Iterations

### 2023-03-11-tested-zip

Improvements
- Returning proper exit code when cumulative file bytes is 0

### 2023-01-27-refactored-zip

Improvements:
- More detailed variable names for better readability
- Better spacing and grouping of logical code segments
- Replaced calls to `exit()` with `return`. [Difference between `exit()` and `return`](https://stackoverflow.com/questions/3463551/what-is-the-difference-between-exit-and-return):
  - It's bad practice to call `exit()` because it immediately stops the current process.
  - Only usecase is to end a child process started by `fork()`.
  - In `main()` for this case, it does nearly the identical thing as `return`.
  - C++ does much more work than C when exiting from functions (destructors of local objects going out of scope)
  - However `exit()` does seem to flish `FILE*` streams.
- Used [EXIT_SUCCESS and EXIT_FAILURE](https://en.cppreference.com/w/c/program/EXIT_status) instead of integer literals. This is more portable across platforms.

### Original 2018 Implementation

- Get all file sizes by reading file statistics
- Create a buffer in-memory with combined file sizes
- Load all files into the buffer
- Iterate through each char in the buffer and perform Run-length encoding
- Immediately write encodings to STDOUT; many calls to `puts` and `fwrite()`. No idea why I decided to use two different functions...

## Testing Iterations

- 2023-03-11: Using python script with `subprocess` to invoke the zip program. 
  - Using `NamedTemporaryFile` to avoid writing to disk. This allows the program to use the same filename.
  - Ran into issue where the python script opens the file, and the C program has to write to the file, and the python script has to read the file again. [On Windows this is a problem](https://docs.python.org/3/library/tempfile.html#tempfile.NamedTemporaryFile). Here is the [cross-platform solution I came up with](https://stackoverflow.com/questions/15169101/how-to-create-a-temporary-file-that-can-be-read-by-a-subprocess/15235559#15235559).