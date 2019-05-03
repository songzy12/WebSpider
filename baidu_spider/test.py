from utils import search_exactqa


def test_file(in_file, out_file):
    with open(in_file, encoding='utf8') as f:
        for line in f.readlines():
            try:
                text, tag = line.strip().split(',')
            except:
                continue
            answer = search_exactqa(text)
            if answer:
                try:
                    print(text, answer[0])
                except:
                    continue


if __name__ == '__main__':
    files = ['GeneralQA.txt', '定义类.txt']
    for file_ in files:
        test_file('data/' + file_, file_)