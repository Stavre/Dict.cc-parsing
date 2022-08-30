import numpy as np
import pandas as pd
import multiprocessing as mp

from main import timereps

def parse_function(df : pd.DataFrame):
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


def parse(dictionary : str, cores=mp.cpu_count()):

    skip_lines = 0
    # open file
    with open(dictionary, "r", encoding="utf-8") as file:
        for line in file:  # runs and ignores the licence header in the file
            if line[0] == "#":
                pass
            else:
                break
            skip_lines = skip_lines + 1

    df = pd.read_csv(dictionary, names=["word", "translation", "grammar", "field"] , delimiter="\t", skiprows=skip_lines)

    if cores <= 0:
        cores = 1


    chunks = np.array_split(df, cores, axis=0)
    pool = mp.Pool(mp.cpu_count())


    results =  pool.map(parse_function, chunks)

    pool.close()


    r = pd.concat(results, axis=0)

    return r



if __name__ == '__main__':
    #print(timereps(10, parse, "de_en_dictionary.txt"))
    df = parse("de_en_dictionary.txt")
    df.to_csv("new.csv", index=False)

