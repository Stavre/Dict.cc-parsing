import numpy as np
import pandas as pd
import multiprocessing as mp

from main import timereps


def parse_function(df: pd.DataFrame):
    # transform any unicode codes into unicode characters
    for col in ["word", "translation", "grammar", "field"]:
        df[col] = df[col].str.replace(r'&#([0-9]+);', lambda x: chr(int(x.group(1), 10)), regex=True)

    # extract tags

    df["word abbreviation"] = df["word"].str.extract(pat="(<.*>)")
    df["word comment"] = df["word"].str.extract(pat="(\[.*])")
    df["word optional"] = df["word"].str.extract(pat="(\(.*\))")
    df["word definition"] = df["word"].str.extract(pat="(\{.*})")
    df["translation abbreviation"] = df["translation"].str.extract(pat="(<.*>)")
    df["translation comment"] = df["translation"].str.extract(pat="(\[.*])")
    df["translation optional"] = df["translation"].str.extract(pat="(\(.*\))")
    df["translation definition"] = df["translation"].str.extract(pat="(\{.*})")

    # remove tags from original columns
    regexes = ["<.*>", "\[.*]", "\(.*\)", "\{.*}"]

    for col in ["word", "translation"]:
        for regex in regexes:
            df[col] = df[col].replace(regex, '', regex=True)

    # remove leading and trailing whitespaces
    for col in df.select_dtypes('object'):
        df[col] = df[col].str.strip()

    return df


def parse(dictionary: str, multiprocessing: bool = False, cores: int = mp.cpu_count()):
    skip_lines = 0
    # open file
    with open(dictionary, "r", encoding="utf-8") as file:
        for line in file:  # runs and ignores the licence header in the file
            if line[0] == "#":
                pass
            else:
                break
            skip_lines = skip_lines + 1

    df = pd.read_csv(dictionary, names=["word", "translation", "grammar", "field"], delimiter="\t", skiprows=skip_lines)
    # Evey row should have four parts:
    #      -> first column contains the word with or without any additional brackets
    #      -> second column contains the translation of the word with or without any additional brackets
    #      -> third column contains the word class (eg. noun, verb, etc)
    #      -> fourth column may contain subject tags (eg. math. -> mathematics, chem. -> chemistry, etc)
    # Every column may contain different elements contained in a set of brackets
    # A summary of the brackets can be found below

    """
    The following brackets were taken from the dict.cc website (https://contribute.dict.cc/guidelines/)

    <angle> -> abbreviations/acronyms
    [square] -> visible comments
    (round) -> for optional parts
    {curly} -> word class definitions
    """
    if multiprocessing is False:
        r = parse_function(df)
    else:
        if cores <= 0:  # if the number of cores is invalid, set it to the number of hardware cores present
            cores = mp.cpu_count()

        # split the dataframe into multiple chunks
        chunks = np.array_split(df, cores, axis=0)

        # create Pool
        pool = mp.Pool(cores)

        # store the list of results
        results = pool.map(parse_function, chunks)

        pool.close()

        r = pd.concat(results, axis=0)

    return r
