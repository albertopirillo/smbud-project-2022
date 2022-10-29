"""
    This script removes a set of characters that might be incompatible with the import function of a database.
    Its input is a textual file of any format.
    Its output is the file without such characters.
    The update is performed in-place and line-by-line to save memory.
"""
import fileinput

# Config
characters_to_remove = {"\\"}
file_path = ""

if __name__ == "__main__":
    with fileinput.FileInput(file_path, inplace=True, encoding="UTF-8") as file:
        for line in file:
            for char in characters_to_remove:
                line = line.replace(char, "")
            print(line, end='')

    print("Operation complete.")
