"""
    This script removes a set of characters that might be incompatible with the import function of a database.
    Its input is a .csv file.
    Its output is a .csv file without such characters
"""

# Config
characters_to_remove = {"\\"}
in_file_path = ""
out_file_path = ""

if __name__ == "__main__":
    with open(in_file_path, 'r', encoding="UTF-8") as in_file, open(out_file_path, 'w', encoding="UTF-8") as out_file:
        data = in_file.read()
        for char in characters_to_remove:
            data = data.replace(char, "")
        out_file.write(data)
