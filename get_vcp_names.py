import requests
from bs4 import BeautifulSoup
import tqdm


def main():
    vclp_names = []
    print('ボカロpの名前を取得中...')
    #ページ数が1~50まで
    for i in tqdm.tqdm(range(1,51)):
        #urlの末尾がページ数になってる
        url = 'http://nicodb.jp/v/bgm/alllist/' + str(i)
        #urlの情報を取る
        r = requests.get(url)
        soup = BeautifulSoup(r.text,'html.parser')
        [tag.extract() for tag in soup(string='n')]

        for j in range(1,101):
            #{}の中にjを入れる
            elems = soup.select('#SortTable > tbody > tr:nth-of-type({}) > td:nth-of-type(3) > a > span'.format(str(j)))
            name = elems[0].text
            name = name.replace('\n','')
            vclp_names.append(name.strip())
    return vclp_names


if __name__ == '__main__':
    main()
