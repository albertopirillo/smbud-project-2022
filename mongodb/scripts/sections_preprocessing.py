import pandas as pd
import random

# Config
main_df = pd.read_csv("")
photo_df = pd.read_csv("", sep='\t')
tweets_df = pd.read_csv("")
text_df = tweets_df.pop("")
paper_df = pd.read_csv("")


if __name__ == "__main__":
    id_df = main_df.pop("id")
    caption_df = photo_df.drop(columns=photo_df.columns[1], axis=1)
    url_df = photo_df.drop(columns=photo_df.columns[0], axis=1)

    i = 0
    j = 0
    data = []
    for index, row in id_df.iteritems():
        sections = []
        k = random.randint(2, 4)
        for a in range(1, k):
            section = {}
            text = ""
            temp = str(text_df.iloc[i]).replace('\n', ' ')
            temp = temp.replace('\'', ' ')
            temp = temp.replace('\"', ' ')
            section["id"] = a
            section["title"] = temp
            i = i + 1
            for b in range(0, 4):
                temp = str(text_df.iloc[i]).replace('\n', ' ')
                temp = temp.replace('\'', ' ')
                temp = temp.replace('\"', ' ')
                text = text + temp
                i = i + 1
            section["text"] = text
            subsections = []
            subsections_number = random.randint(1, 3)
            for c in range(1, subsections_number):
                subsection = {}
                text = ""
                temp = str(text_df.iloc[i]).replace('\n', ' ')
                temp = temp.replace('\'', ' ')
                temp = temp.replace('\"', ' ')
                subsection["id"] = c
                subsection["title"] = temp
                i = i + 1
                for b in range(0, 3):
                    temp = str(text_df.iloc[i]).replace('\n', ' ')
                    temp = temp.replace('\'', ' ')
                    temp = temp.replace('\"', ' ')
                    text = text + temp
                    i = i + 1
                subsection["text"] = text
                subsections.append(subsection)
            section["subsections"] = subsections
            figures = []
            figures_number = random.randint(2, 4)
            for c in range(1, figures_number):
                figure = {}
                temp = str(caption_df.iloc[j]).replace('\n', ' ')
                temp = temp.replace('\'', ' ')
                temp = temp.replace('\"', ' ')
                n = str(url_df.iloc[j]).replace('\n', ' ')
                n = n.replace('\'', ' ')
                n = n.replace('\"', ' ')
                figure["url"] = n
                figure["caption"] = temp
                j = j + 1
                figures.append(figure)
            section["figures"] = figures
            sections.append(section)
        data.append([row, sections])

    d = pd.DataFrame(data=data, columns=['id', 'sections'])

    paper_df = paper_df.merge(d, on='id', how='left')
    paper_df.to_csv("paper_dataset_final.csv", encoding="UTF-8", index=False, escapechar="|")
