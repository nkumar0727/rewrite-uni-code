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

MAX_FILE_COUNT = 1000

# STATUS CODES
SUCCESS_EXIT_CODE = 0
NO_BYTES_EXIT_CODE = 64
TOO_MANY_FILES_EXIT_CODE = 65
MAX_TOTAL_FILE_BYTES_EXCEEDED = 66
FILE_CANNOT_BE_OPENED_EXIT_CODE = 67

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
    
    def test_WHEN_zeroFiles_THEN_exitCode64(self):
        script_args = [
            EXECUTABLE_NAME
        ]
        result = subprocess.run(args=script_args, timeout=60, stdout=self.output_file)

        self.assertEqual(NO_BYTES_EXIT_CODE, result.returncode)

        self.output_file.seek(0, os.SEEK_SET)
        file_size = os.stat(self.output_file.name).st_size

        self.assertEqual(0, file_size)
    
    def test_WHEN_allFilesHaveZeroBytes_THEN_exitCode64(self):
        script_args = [
            EXECUTABLE_NAME,
            os.path.join('', self.input_file_1.name), 
            os.path.join('', self.input_file_2.name)
        ]
        result = subprocess.run(args=script_args, timeout=60, stdout=self.output_file)

        self.assertEqual(NO_BYTES_EXIT_CODE, result.returncode)

        self.output_file.seek(0, os.SEEK_SET)
        file_size = os.stat(self.output_file.name).st_size

        self.assertEqual(0, file_size)
    
    def test_WHEN_totalFileCountExceedsInternalLimit_THEN_exitCode65(self):
        script_args = [EXECUTABLE_NAME] + (['a.txt'] * (MAX_FILE_COUNT + 1))
        print(f"TotalSize: {len(' '.join(script_args))}")

        result = subprocess.run(args=script_args, timeout=60, stdout=self.output_file)

        self.assertEqual(TOO_MANY_FILES_EXIT_CODE, result.returncode)

        self.output_file.seek(0, os.SEEK_SET)
        file_size = os.stat(self.output_file.name).st_size

        self.assertEqual(0, file_size)
    
    def test_WHEN_totalFileSizeExceedsInternalLimit_THEN_exitCode66(self):
        self.fail("TODO: Implement")

    @unittest.skip("Needs some research on best way to get file size in C...")
    def test_WHEN_oneFileCannotBeOpened_THEN_exitCode67(self):
        unopenable_file = tempfile.NamedTemporaryFile(mode='w')
        unopenable_file.write('aabbcc')
        unopenable_file.close()

        self.input_file_1.write('aabbcc')
        self.input_file_1.close()
        self.input_file_2.write('cddeef')
        self.input_file_2.close()

        script_args = [
            EXECUTABLE_NAME,
            os.path.join('', self.input_file_1.name), 
            os.path.join('', unopenable_file.name),
            os.path.join('', self.input_file_2.name)
        ]

        result = subprocess.run(args=script_args, timeout=60, stdout=self.output_file)

        self.assertEqual(FILE_CANNOT_BE_OPENED_EXIT_CODE, result.returncode)

        self.output_file.seek(0, os.SEEK_SET)
        file_size = os.stat(self.output_file.name).st_size

        self.assertEqual(0, file_size)
    
    def test_WHEN_twoFiles_THEN_outputCorrect(self):
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

        self.assertEqual(SUCCESS_EXIT_CODE, result.returncode)

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

        encoded_result = ''.join(char_list)

        self.assertEqual("2a2b3c2d2e1f", encoded_result)

if __name__ == "__main__":
    unittest.main()
