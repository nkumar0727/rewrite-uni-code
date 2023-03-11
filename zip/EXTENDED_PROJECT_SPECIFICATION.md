## Extended Specification

### Basic Cases

Number of files
- 0 files -> exit code 64
- 1 or more files where cumulative file size is 0-> exit code 64
- [> 32,767 files](https://stackoverflow.com/questions/3724369/limit-on-the-number-of-arguments-to-main-in-c) -> exit code 65

Size of files
- cumulative bytes 0 -> exit code 64
- cumulative bytes > [1 TB (1000 GB)](https://en.wikipedia.org/wiki/Byte#Multiple-byte_units) -> exit code 66

Content of files
- internal input file processing error -> exit code 68

Validity of files
- input file cannot be opened -> exit code 67

### Stress Cases

File Content:
- 5 files where subsequent characters are distinct (ex. 'ababab...) and totalling to 1TB, producing largest possible output
- 5 files totalling to 1TB where all characters are the same (ex. 'aaaa...), producing just a very small output
- File where consecutive frequency of character meets or exceeds [primitive type limits](https://en.wikipedia.org/wiki/C_data_types) (ex. char, unsigned int, signed int, long, etc...)

### Performance Cases

File Count Impact
- 1 file totalling to 1TB
- 10 files totalling to 1TB 
- 100 files totalling to 1TB
- 1000 files totalling to 1TB
- 10000 files totalling to 1TB
- 32767 files totalling to 1TB

Byte Count Impact
- 10 files totalling to 1 MB
- 10 files totalling to 10 MB
- 10 files totalling to 100 MB
- 10 files totalling to 1 GB
- 10 files totalling to 10 GB
- 10 files totalling to 100 GB

### Exit Codes

See [this link for some conventions](https://tldp.org/LDP/abs/html/exitcodes.html). 

> An update of /usr/include/sysexits.h allocates previously unused exit codes from 64 - 78

In this program, we will use the following exit codes:
- 0 - success
- 64 - cumulative file size is 0 bytes, no output written
- 65 - too many files, no output written
- 66 - cumulative file size is > [1TB (1000 GB)](https://en.wikipedia.org/wiki/Byte#Multiple-byte_units), no output written
- 67 - one or more of the files could not be opened, no output written
- 68 - internal error ocurred, no output written

The phrase "no output written" here means that nothing in the caller's filesystem will be updated after program execution. IE, no partial processing will be written to any output stream.
