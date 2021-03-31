from bs4 import BeautifulSoup
import requests

def get_movement():
    url = 'https://nikkei225jp.com/nasdaq/'
    req = requests.get(url)
    html = req.text
    sp = BeautifulSoup(html, 'html.parser')
    sp2 = sp.find('div', class_='win2')
    sp3 = sp2.find('tr')
    sp4 = sp3.find('div', id='if_con')
    all_data = sp4.find('div', id='if_con22')
    datas = []
    if all_data ==None:
        return 'None'
    else:
        for tag in all_data.find_all('div', class_='if_box2'):
            price = tag.find('div', class_='if_cur')
            par = tag.find('div', class_='per')
            data = [price.get_text(), par.get_text()]
            datas.append(data)

        text = '現在のダウ平均株価は{}円です。\n{}の変化が起きました。'
        return text.format(datas[1][0], datas[1][1])
