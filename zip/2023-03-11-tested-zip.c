#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <limits.h>

#define LONGEST_POSSIBLE_CHARACTER_ENCODING_FREQUENCY (~0)
#define NULL_TERMINATOR ('\0')
#define MAX_FILE_COUNT (32767)

#define NO_BYTES_EXIT_CODE (64)
#define TOO_MANY_FILES_EXIT_CODE (65)

int main(int argc, char **argv) {

    struct stat file_statistics;
    size_t file_size_bytes_array[argc];
    size_t cumulative_size_bytes = 0;
    int last_file_index = argc;

    if (argc > MAX_FILE_COUNT + 1) {
        return TOO_MANY_FILES_EXIT_CODE; 
    }

    for (int i = 1; i < argc; ++i) {

        if (stat(argv[i], &file_statistics) == -1) {
            last_file_index = i;
            break;
        }

        file_size_bytes_array[i - 1] = file_statistics.st_size;
        cumulative_size_bytes += file_statistics.st_size;
    }

    if (cumulative_size_bytes == 0) {
        return NO_BYTES_EXIT_CODE;
    }

    char* memory_buffer_for_files = (char *) malloc(cumulative_size_bytes + sizeof(char));
    size_t next_byte_free_in_buffer = 0;

    for (int i = 1; i < last_file_index; ++i) {
        FILE* file_pointer = fopen(argv[i], "r");

        void* location_to_insert_in_buffer = (void*) (memory_buffer_for_files + next_byte_free_in_buffer);
        size_t file_size_bytes = file_size_bytes_array[i - 1];

        size_t fread_return_code = fread(location_to_insert_in_buffer, sizeof(char), file_size_bytes, file_pointer);

        fclose(file_pointer);

        if (!fread_return_code) {
            printf("Could not read properly\n");
            free(memory_buffer_for_files);
            return EXIT_FAILURE;
        }

        next_byte_free_in_buffer += file_size_bytes_array[i - 1];
    }

    memory_buffer_for_files[cumulative_size_bytes] = NULL_TERMINATOR;

    // perform RLE char by char
    char current_character = memory_buffer_for_files[0];

    char encoding_character = current_character;
    unsigned int encoding_character_frequency = 1;

    size_t current_byte = 1;

    while (current_byte < cumulative_size_bytes) {

        current_character = memory_buffer_for_files[current_byte];

        if (current_character != encoding_character) {
            fwrite(&encoding_character_frequency, sizeof(unsigned int), 1, stdout);
            putc(encoding_character, stdout);
            encoding_character = current_character;
            encoding_character_frequency = 1;

        } else if (encoding_character_frequency < LONGEST_POSSIBLE_CHARACTER_ENCODING_FREQUENCY) {
            encoding_character_frequency += 1;

        } else {
            fwrite(&encoding_character_frequency, sizeof(unsigned int), 1, stdout);
            putc(encoding_character, stdout);
            encoding_character_frequency = 0;
        }

        current_byte += 1;
    }

    if (cumulative_size_bytes == 1) {
        fwrite(&encoding_character_frequency, sizeof(unsigned int), 1, stdout);
        putc(encoding_character_frequency, stdout);

    } else if (encoding_character_frequency >= 1) {
        fwrite(&encoding_character_frequency, sizeof(unsigned int), 1, stdout);
        putc(encoding_character, stdout);
    }

    free(memory_buffer_for_files);

    return EXIT_SUCCESS;
}
