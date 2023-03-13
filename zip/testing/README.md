# Testing

## Methodology

Use a Python script to avoid learning how to unit tests C programs.
- Run the C program executable with the [`subprocess` module](https://docs.python.org/3/library/subprocess.html).
- For test case management, use the [`unittest` module](https://docs.python.org/3/library/unittest.html).
- For avoiding filesystem pollution, use the [`tempfile` module](https://docs.python.org/3/library/tempfile.html)
- To convert bytes into a structure (ex. unsigned int), use the [`struct` module](https://docs.python.org/3/library/struct.html).

## Basic Test Cases

Number of files
- 0 files -> exit code 64
- 1 or more files where cumulative file size is 0-> exit code 64
- [> 1000 files](https://stackoverflow.com/questions/3724369/limit-on-the-number-of-arguments-to-main-in-c) -> exit code 65

Size of files
- cumulative bytes 0 -> exit code 64
- cumulative bytes > [1 TB (1000 GB)](https://en.wikipedia.org/wiki/Byte#Multiple-byte_units) -> exit code 66

Content of files
- internal input file processing error -> exit code 68

Validity of files
- input file cannot be opened -> exit code 67

## Stress Test Cases

File Content:
- 5 files where subsequent characters are distinct (ex. 'ababab...) and totalling to 1TB, producing largest possible output
- 5 files totalling to 1TB where all characters are the same (ex. 'aaaa...), producing just a very small output
- File where consecutive frequency of character meets or exceeds [primitive type limits](https://en.wikipedia.org/wiki/C_data_types) (ex. char, unsigned int, signed int, long, etc...)

## Performance Test Cases 

File Count Impact
- 1 file totalling to 1TB
- 10 files totalling to 1TB 
- 100 files totalling to 1TB
- 1000 files totalling to 1TB

Byte Count Impact
- 10 files totalling to 1 MB
- 10 files totalling to 10 MB
- 10 files totalling to 100 MB
- 10 files totalling to 1 GB
- 10 files totalling to 10 GB
- 10 files totalling to 100 GB

## Interesting Findings

### 1. Limits on command size 

We will change the limits on the script to the following: Maxiumum 32,767 file -> 500 files in the input. We do this at least with the current style of invocation.

At least [on Windows, we have 32,767 max characters in the full command](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessa). If this is exceeded, we get this:

```shell
λ python e2e_test.py
ssTotalSize: 32788
Esss
======================================================================
ERROR: test_WHEN_totalFileCountExceedsInternalLimit_THEN_exitCode65 (__main__.TestZipCases)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\the_chosen_one\Documents\coding\rewrite-uni-code\zip\e2e_test.py", line 72, in test_WHEN_totalFileCountExceedsInternalLimit_THEN_exitCode65
    result = subprocess.run(args=script_args, timeout=60, stdout=self.output_file)
  File "C:\Users\the_chosen_one\AppData\Local\Programs\Python\Python310\lib\subprocess.py", line 501, in run
    with Popen(*popenargs, **kwargs) as process:
  File "C:\Users\the_chosen_one\AppData\Local\Programs\Python\Python310\lib\subprocess.py", line 966, in __init__
    self._execute_child(args, executable, preexec_fn, close_fds,
  File "C:\Users\the_chosen_one\AppData\Local\Programs\Python\Python310\lib\subprocess.py", line 1435, in _execute_child
    hp, ht, pid, tid = _winapi.CreateProcess(executable, args,
FileNotFoundError: [WinError 206] The filename or extension is too long
```

When the size was less than 32.767 characters:

```shell
λ python e2e_test.py
ssTotalSize: 32739
Fsss
======================================================================
FAIL: test_WHEN_totalFileCountExceedsInternalLimit_THEN_exitCode65 (__main__.TestZipCases)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\the_chosen_one\Documents\coding\rewrite-uni-code\zip\e2e_test.py", line 74, in test_WHEN_totalFileCountExceedsInternalLimit_THEN_exitCode65
    self.assertEqual(TOO_MANY_FILES_EXIT_CODE, result.returncode)
AssertionError: 65 != 64
```
