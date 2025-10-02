import requests
from bs4 import BeautifulSoup
import re
import random

num = '380637674497'
num_rati = float(10)

resp_1 = requests.get(f'https://callfilter.app/{num}')

htmlcheck = BeautifulSoup(resp_1.text,'html.parser')

us_1 = str(htmlcheck.find('li',class_="active"))
us_2 = htmlcheck.find_all('h3')
us_3 = htmlcheck.find_all('span',class_="review_comment")

qua_revi = re.search(r'\d+',us_1)
qua_revi = qua_revi.group()
num_rati-=int(qua_revi)/10

for us in us_2:
    u = str(us.find('span',class_="reviewName"))
    find = re.search(r'\b(' + '|'.join(['Кинули трубку','Колектори','Телефонне шахрайство',"Реклама / нав'язування послуг",'Опитування','Фінансові послуги','Магазин','Компанія','Інша']) + r')\b',u)
    if find:
        if find.group() in ["Реклама / нав'язування послуг",'Опитування','Інша']:
            num_rati-=0.1
        elif find.group() in ['Кинули трубку','Колектори','Фінансові послуги','Магазин','Компанія']:
            num_rati-=0.2
        else:
            num_rati-=0.3

for us in us_3:
    find = re.search(r'\b(' + '|'.join(['Мовчали','Молчали','Тиша','Тишина','Солі','Соли','Спайси','Спайсы','Виграш','Выигрыш','Спам','Настирні','Настырные','Россиия','Росія','России','Росії','Курсы','Курси','Кредит','Кредитка','Заблокована карта','Заблокированная карта','Лохотрон','Развод']) + r')\b', str(us), flags=re.IGNORECASE)
    if find:
        if find.group() in ['Мовчали','Молчали','Тиша','Тишина','Спам','Настирні','Настырные']:
            num_rati-=0.1
        elif find.group() in ['Кредит','Кредитка','Курсы','Курси']:
            num_rati-=0.2
        else:
            num_rati-=0.3


us_ag = {
    1:"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
    2:"Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    3:"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
    4:"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:139.0) Gecko/20100101 Chrome/138.0.0.0 Safari/537.36",
    5:"Mozilla/5.0 (Macintosh; Intel Mac OS X 14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
    6:"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0",
    7:"Mozilla/5.0 (Windows NT 11.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0",
    8:"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:131.0) Gecko/20100101 Firefox/131.0",
    9:"Mozilla/5.0 (X11; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0",
    10:"Mozilla/5.0 (Macintosh; Intel Mac OS X 14.6; rv:131.0) Gecko/20100101 Firefox/131.0"
}

while True:
    resp_2 = requests.get(f'https://www.telefonnyjdovidnyk.com.ua/nomer/{num}',headers={'User-Agent':random.choice(list(us_ag.values()))})
    if resp_2.status_code == 200:
        break
print(resp_2)