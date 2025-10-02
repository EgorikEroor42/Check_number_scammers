import requests
from bs4 import BeautifulSoup
import re
from collections import Counter
cho = input('What you want: 1 - Add comments. 2 - Clear the file. :')
if cho == '1':
    while True:
        num = input('Enter phone number:')
        arr_1 = ['(програвався запис / робот)','(розмовляв чоловік)','(німий дзвінок / скидання)','Повідомлення від адміністратора сайту telefonnyjdovidnyk.com.ua«Допоможіть іншим відвідувачам сайту тим, що поділитеся з ними своїм досвідом спілкування з цим абонентом. Коли Вам з цього номеру телефонували і як часто? Що було предметом розмови, якщо Ви підняли трубку? Коментар, який Ви відіслали, буде показаний на цьому сайті.»','Оцінка:Шахрай','Оцінка:Спамер','Оцінка:Незрозуміло','Оцінка:Безпечно','Оцінка:Корисно']
        resp_1 = requests.get(f'https://callfilter.app/{num}')
        resp_2 = requests.get(f'https://www.telefonnyjdovidnyk.com.ua/nomer/{num}',headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ""AppleWebKit/537.36 (KHTML, like Gecko) ""Chrome/139.0.0.0 Safari/537.36","Accept-Language": "uk-UA,uk;q=0.9,en;q=0.8"})
        num = re.sub(r'\+','',num)
        num = re.sub('38','',num)
        if num[:3] == '094':
            oper = 'intertelecom'
        elif num[:3] in ['067','068','096','097','098']:
            oper = 'kyivstar'
        elif num[:3] in ['063','073','093']:
            oper = 'lifecell'
        elif num[:3] in ['050','066','095','099']:
            oper = 'vodafone'
        else:
            oper = '3mob'
        resp_3 = requests.get(f'https://ua.whokla.com/{oper}/{num}',headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ""AppleWebKit/537.36 (KHTML, like Gecko) ""Chrome/139.0.0.0 Safari/537.36","Accept-Language": "uk-UA,uk;q=0.9,en;q=0.8"})
        htmlcheck1 = BeautifulSoup(resp_1.text,'html.parser')
        htmlcheck2 = BeautifulSoup(resp_2.text,'html.parser')
        htmlcheck3 = BeautifulSoup(resp_3.text,'html.parser')
        us_1 = htmlcheck1.find_all('span',class_="review_comment")
        us_2 = htmlcheck2.find_all('p',class_="comment-text")
        us_3 = htmlcheck3.find_all('div',class_="comment-content")
        arr_2 = []
        for us in us_1:
            u = us.get_text(strip=True)
            arr_2.append(u)
        for us in us_2:
            u = us.get_text(strip=True)
            arr_2.append(u)
        for us in us_3:
            u = us.get_text(strip=True)
            arr_2.append(u)
        arr_3 = []
        for txt_1 in arr_2:
            u = txt_1
            for txt_2 in arr_1:
                u = u.replace(txt_2,'')
            if u != '':
                arr_3.append(u)
        with open(r'C:\Users\avdim\Desktop\MyApps\CN\Ail\AIL.txt', 'a', encoding="UTF-8") as file_par:
            print('0 - Обычный номер (Звонки или сообщения реальных представителей банка/компании/организации, комментарии положительные или нейтральные, нет навязчивости, угроз или попыток обмана.)\n0.5 - Подозрительный номер (Комментарии утверждают «мошенники», но без конкретики, бессмысленные оскорбления, признаки странного поведения (например, предлагают сразу заблокировать номер) без явной угрозы.)\n1 - Спам номер (Частые звонки или сообщения без причины, робот, автоответчик, записи звонков, опросы, реклама, массовая рассылка,нет явного мошенничества или угроз.)\n2 - Опасный номер (Предлагали кредиты, лотереи, казино, услуги с финансовыми последствиями, звонки, направленные на обман или получение выгоды (например, подписка без согласия), молчание, сброс трубки, попытка скрыть информацию, нет прямого требования денег или угроз.)\n3 - Высокоопасный номер (Представились банком/компанией/организацией с целью обмана, пытались узнать личные данные (паспорт, карты, коды),прямые угрозы, вымогательство денег, предлагали запрещённые услуги на территории Украины.)')
            print(f'Number of comments:{len(arr_3)}')
            for txt_3 in arr_3:
                txt_4 = ' '.join(txt_3.split())
                print(txt_4)
                try:
                    cate = float(input('Enter text category:'))
                    if cate in [0.0,0.5,1.0,2.0,3.0]:
                        file_par.write(f'{int(cate) if cate.is_integer() else cate} - {txt_4}\n')
                except ValueError:
                    pass
            answ = input('Do you want to finish? Y/N:')
            if answ.lower() == 'y':
                break
elif cho == '2':
    with (open(r'C:\Users\avdim\Desktop\MyApps\CN\Ail\TEST1.txt', 'r', encoding="UTF-8") as file_check):
        lines = file_check.readlines()
        counter = Counter(lines)
        line_arr = []
        with (open(r'C:\Users\avdim\Desktop\MyApps\CN\Ail\TEST2.txt', 'w', encoding="UTF-8") as file_filter):
            for cou in counter:
                    file_filter.write(cou)