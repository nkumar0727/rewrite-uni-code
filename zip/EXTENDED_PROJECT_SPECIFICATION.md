## Extended Specification

### Exit Codes

See [this link for some conventions](https://tldp.org/LDP/abs/html/exitcodes.html). 

> An update of /usr/include/sysexits.h allocates previously unused exit codes from 64 - 78

In this program, we will use the following exit codes:
- 0 - success
- 64 - cumulative file size is 0 bytes, no output written
- 65 - > 1000 files provided, no output written
- 66 - cumulative file size is > [1TB (1000 GB)](https://en.wikipedia.org/wiki/Byte#Multiple-byte_units), no output written
- 67 - one or more of the files could not be opened, no output written
- 68 - internal error ocurred, no output written

The phrase "no output written" here means that nothing in the caller's filesystem will be updated after program execution. IE, no partial processing will be written to any output stream.
