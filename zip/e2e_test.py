import sys
import os
import unittest
import tempfile
import subprocess
import struct
from typing import List

EXECUTABLE_NAME = "zip.exe"
EXPECTED_ZIP_ENCODING = "ascii"
BYTES_PER_UNSIGNED_INT = 4
BYTES_PER_CHARACTER = 1

class TestZipCases(unittest.TestCase):

    def setUp(self):
        self.output_file = tempfile.NamedTemporaryFile(mode='r+b', delete=False)
        self.input_file_1 = tempfile.NamedTemporaryFile(mode='r+t', delete=False)
        self.input_file_2 = tempfile.NamedTemporaryFile(mode='r+t', delete=False)

    def tearDown(self):
        self.output_file.close()
        os.remove(self.output_file.name)
        self.input_file_1.close()
        os.remove(self.input_file_1.name)
        self.input_file_2.close()
        os.remove(self.input_file_2.name)
    
    def test_happyCase(self):
        self.input_file_1.write('aabbcc')
        self.input_file_1.close()
        self.input_file_2.write('cddeef')
        self.input_file_2.close()

        script_args = [
            EXECUTABLE_NAME,
            os.path.join('', self.input_file_1.name), 
            os.path.join('', self.input_file_2.name)
        ]
        result = subprocess.run(args=script_args, timeout=60, stdout=self.output_file)

        self.output_file.seek(0, os.SEEK_SET)

        assert result.returncode == 0

        output_buffer = self.output_file.read()
        char_list = []

        for int_begin_offset in range(0, len(output_buffer), BYTES_PER_UNSIGNED_INT + BYTES_PER_CHARACTER):
            int_end_offset = int_begin_offset + BYTES_PER_UNSIGNED_INT

            frequency = struct.unpack("@I", output_buffer[
                int_begin_offset:int_end_offset
            ])[0]

            char_begin_offset = int_end_offset
            char_end_offset = char_begin_offset + BYTES_PER_CHARACTER

            char_as_bytes = output_buffer[
                char_begin_offset:char_end_offset
            ]
            char = char_as_bytes.decode(EXPECTED_ZIP_ENCODING)

            char_list.append(str(frequency))
            char_list.append(char)

        result = ''.join(char_list)

        assert result == "2a2b3c2d2e1f"

if __name__ == "__main__":
    unittest.main()
