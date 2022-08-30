from parser import parse

if __name__ == '__main__':
    df = parse("de_en_dictionary.txt") # de_en_dictionary.txt is the name of the file containing the dict.cc dictionary
    print(df)
