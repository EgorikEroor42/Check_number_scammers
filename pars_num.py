import requests
from bs4 import BeautifulSoup
import re
import random
num = str(input())
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
num_oper = ['intertelecom','kyivstar','lifecell','vodafone','3mob']
resp_1 = requests.get(f'https://callfilter.app/{num}')
resp_2 = requests.get(f'https://www.telefonnyjdovidnyk.com.ua/nomer/{num}',headers={'User-Agent':random.choice(list(us_ag.values()))})
resp_3 = ''
for oper in num_oper:
    resp_4 = requests.get(f'https://ua.whokla.com/{oper}/{num}', headers={'User-Agent':random.choice(list(us_ag.values()))})
    if resp_4.status_code == 200:
        resp_3 = resp_4
        break
htmlcheck1 = BeautifulSoup(resp_1.text,'html.parser')
htmlcheck2 = BeautifulSoup(resp_2.text,'html.parser')
htmlcheck3 = BeautifulSoup(resp_3.text,'html.parser')
txt_1 = htmlcheck1.find_all('span',class_="review_comment")
txt_2 = htmlcheck2.find_all('p',class_="comment-text")
txt_3 = htmlcheck3.find_all('div',class_="comment-content")
review_arr = []
for txt in txt_1:
    review_arr.append(txt.get_text(strip=True))
for txt in txt_2:
    review_arr.append(txt.get_text(strip=True))
for txt in txt_3:
    review_arr.append(txt.get_text(strip=True))
for filt in review_arr:
    i = review_arr.index(filt)
    filt = filt.lower()
    filt = re.sub(r'(' + '|'.join(map(re.escape, ['(програвався запис / робот)','(розмовляв чоловік)','(німий дзвінок / скидання)','Повідомлення від адміністратора сайту telefonnyjdovidnyk.com.ua«Допоможіть іншим відвідувачам сайту тим, що поділитеся з ними своїм досвідом спілкування з цим абонентом. Коли Вам з цього номеру телефонували і як часто? Що було предметом розмови, якщо Ви підняли трубку? Коментар, який Ви відіслали, буде показаний на цьому сайті.»','Оцінка:Шахрай','Оцінка:Спамер','Оцінка:Незрозуміло','Оцінка:Безпечно','Оцінка:Корисно'])) + r')','',filt,flags=re.IGNORECASE)
    filt = re.sub(re.compile("[""\U0001F600-\U0001F64F""\U0001F300-\U0001F5FF""\U0001F680-\U0001F6FF""\U0001F1E0-\U0001F1FF""\U00002700-\U000027BF""\U0001F900-\U0001F9FF""\U0001FA70-\U0001FAFF""\U00002600-\U000026FF""]+",flags=re.UNICODE),'',filt)
    filt = re.sub(r'https?://\S+','',filt)
    filt = re.sub(r'[\r\n]+', ' ', filt)
    filt = re.sub(r'\s+', ' ', filt).strip()
    filt = re.sub(r'[^a-za-я0-9\s]','',filt)
    if filt != '':
        review_arr[i] = filt