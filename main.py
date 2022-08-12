import re
import pandas as pd

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

def apply_regex(string: str, regexes: list):
    """
    Extracts and removes substrings matching regexes from the list
    Returns a dictionary of the form regex: matches of the regex
    The last dictionary entry is final: string after all matches have been removed
    """

    matches = {}
    for regex in regexes:
        # extract substrings matching the regex
        matches[regex] = ", ".join(re.findall(regex, string))

        # remove substring from the original string
        string = re.sub(regex, "", string)
    matches["final"] = string
    return matches


def parse_dict(dictionary):
    dictionary_entry = {
        "Word": [],
        "Word abbreviations": [],
        "Word comments": [],
        "Word optional": [],
        "Word class definitions": [],
        "Word class": [],
        "Translation": [],
        "Translation abbreviations": [],
        "Translation comments": [],
        "Translation optional": [],
        "Translation class definitions": [],
        "Subjects": []

    }

    # open file
    with open(dictionary, "r", encoding="utf-8") as file:

        for line in file: # runs and ignores the licence header in the file
            if line[0] == "#":
                pass
            else:
                break

        # parse every line
        for line in file:
            # strip line of newline
            line = line.strip("\n")

            # transform any unicode codes into unicode characters
            line = re.sub(r'&#([0-9]+);', lambda x: chr(int(x.group(1), 10)), line)

            # split line after \t.
            # The resulting list will have four parts:
            #      -> line[0] contains the word with or without any additional brackets
            #      -> line[1] contains the translation of the word with or without any additional brackets
            #      -> line[2] contains the word class (eg. noun, verb, etc)
            #      -> line[3] may contain subject tags (eg. math. -> mathematics, chem. -> chemistry, etc)
            line = line.split(sep="\t")

            """
            The following brackets were taken from the dict.cc website (https://contribute.dict.cc/guidelines/)

            <angle> -> abbreviations/acronyms
            [square] -> visible comments
            (round) -> for optional parts
            {curly} -> word class definitions
            """

            # regexes for extracting the above mentioned brackets
            regexes = ["<.*>", "\[.*]", "\(.*\)", "\{.*}"]

            # Store all brackets found in the first field (the Word) in dictionary world_field
            word_field = apply_regex(line[0], regexes)

            # Append to correct lists
            dictionary_entry["Word"].append(word_field["final"])
            dictionary_entry["Word abbreviations"].append(word_field["<.*>"])
            dictionary_entry["Word comments"].append(word_field["\[.*]"])
            dictionary_entry["Word optional"].append(word_field["\(.*\)"])
            dictionary_entry["Word class definitions"].append(word_field["\{.*}"])

            # Same stuff but for the second field (the Translation)
            translation_field = apply_regex(line[1], regexes)
            dictionary_entry["Translation"].append(translation_field["final"])
            dictionary_entry["Translation abbreviations"].append(translation_field["<.*>"])
            dictionary_entry["Translation comments"].append(translation_field["\[.*]"])
            dictionary_entry["Translation optional"].append(translation_field["\(.*\)"])
            dictionary_entry["Translation class definitions"].append(translation_field["\{.*}"])

            dictionary_entry["Word class"].append(line[2])
            dictionary_entry["Subjects"].append(line[3])

    df = pd.DataFrame(dictionary_entry)
    df.to_csv("dictionary.csv")

    # remove leading and trailing whitespaces
    for col in df.select_dtypes('object'):
        df[col] = df[col].str.strip()

    return df

def timereps(reps, func, arg):
    from time import time
    start = time()
    for i in range(0, reps):
        func(arg)
    end = time()
    return (end - start) / reps

if __name__ == '__main__':
    df = parse_dict("de_en_dictionary.txt")
    #df = pd.read_csv("dictionary.csv")
    #df = df[df["Word class"] == "noun"]
    #print(df)
