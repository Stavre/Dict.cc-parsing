# Dict.cc parser

### About
Simple parser for Dict.cc dictionary. It was tested with DE<>EN, DE<>LA, DE<>NL, EN<>ES, and EN<>FR dictionaries but should work for all dict.cc dictionaries.

### How to use it

1. Download the dictionary of your choice from Dict.cc. For more details visit https://www.dict.cc/?s=about%3Awordlist
2. Download and run the function
3. Use the pandas dataframe returned by the function as you like (provided you respect dict.cc terms of use)

### Function description
parse(dictionary: str, multiprocessing: bool = False, cores: int = mp.cpu_count())


dictionary -> string. path to txt file containing the dictionary

multiprocessing -> boolean value. If true, the dictionary is split into chunks and each chunk is processed by a separate core. If false, the dictionary is parsed without any multiprocessing. Multiprocessing should be set to true only for large dictionaries.

cores -> integer. Number of cores used. By default it is set to the number of cores present in the hardware. If cores <= 0 then cores=mp.cpu_count()

### If multiprocessing is True, then the function must be used with if __name__ == '__main__': guard.

![fig](https://user-images.githubusercontent.com/31391614/187764703-e5aa984f-ef0f-4965-998e-484c48cafc07.png)

