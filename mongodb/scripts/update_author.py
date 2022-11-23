"""
    This script adds the missing fields to the author entity.
    The email is generated starting from the name and the surname.
    The bio is taken from another dataset and merged into the original one.
"""

import pandas as pd
import ast
import random

# Config
input_file_path = ""
output_file_path = ""
bio_file_path = ""
domains = ["@gmail.com", "@polimi.it", "@outlook.com", "@hotmail.com", "@yahoo.com", "@mit.edu", "@liberomail.com",
           "@123mail.org", "@fastmail.com"]
arabic = ['ء', 'ا', 'إ', 'أ', 'آ', 'ب', 'ة', 'ت', 'ث', 'ج', 'ح', 'خ', 'د', 'ذ', 'ر', 'ز', 'س', 'ش', 'ص', 'ض', 'ط', 'ظ',
          'ع', 'غ', 'ف', 'ق', 'ك', 'ل', 'م', 'ن', 'ه', 'ؤ', 'و', 'ى', 'ئ', 'ي']

if __name__ == "__main__":
    # Load the dataset
    df = pd.read_csv(input_file_path, encoding="UTF-8")
    df_bio = pd.read_csv(bio_file_path, encoding="UTF-8")

    all_papers_authors = df["authors"].apply(ast.literal_eval)
    bios = df_bio["about"]

    new_authors_content = []
    round_count = 1
    i = 0
    for author_list in all_papers_authors:

        for author in author_list:
            # Get author name
            author_name = str(author["name"])
            author_name = author_name.replace(" ", "").lower()

            # Generate and insert email
            email_string = author_name + random.choice(domains)
            email = {"email": email_string}

            author.update(email)

            # Remove arabic biographies
            while True:
                if (bios[i][1] in arabic) or (bios[i][10] in arabic):
                    i += 1
                else:
                    break

            # Insert bio
            author_bio = bios[i]
            bio = {"bio": author_bio}

            author.update(bio)

            i += 1

        round_count += 1

        new_author_list = author_list
        new_authors_content.append(new_author_list)

    df["authors"] = new_authors_content

    # Write the updated dataset
    df.to_csv(output_file_path, encoding="UTF-8", index=False, header=True, escapechar="|")

    print(f"Operation complete.")
