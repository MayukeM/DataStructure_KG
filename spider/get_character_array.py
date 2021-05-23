import codecs


def get_character():
    f = codecs.open('../raw_data/relation.csv', 'r', 'gbk')
    data = []
    for line in f.readlines():
        array = line.strip("\n").split(",")
        arr = [array[0], array[1]]
        data.extend(arr)

    return data
