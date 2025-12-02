import asyncio,google.genai.errors,joblib,json,math,random,re,requests
from bs4 import BeautifulSoup
from collections import Counter
from datetime import datetime
from dateutil.relativedelta import relativedelta
from fastapi import FastAPI
from google import genai
from impo.db import AllComments,Numbers,Session
from sqlalchemy import select
api = FastAPI(title='API for CN',description='API for transferring data from a mobile application to Python code.')
@api.get("/num/{num}")
async def search(num):
    num = str(num)
    async def all_num():
        async with Session() as session:
            chnum = await session.scalar(select(Numbers.created_at).where(Numbers.number == num))
            if chnum is not None:
                tim = chnum + str(relativedelta(months=2))
                tod = str(datetime.today().date())
                return True if tod > tim or tod == tim else False
            else:
                return False
    async def ret_num():
        async with Session() as session:
            retnum = await session.scalar(select(Numbers).where(Numbers.number == num))
            return {"number":retnum.number,"last_10_comments":retnum.last_10_comments,"answer_ai":retnum.answer_ai,"rating":retnum.rating,"created_at":retnum.created_at}
    async def ai_help():
            review_arr = set()
            us_ag = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36","Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36","Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36","Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:139.0) Gecko/20100101 Chrome/138.0.0.0 Safari/537.36","Mozilla/5.0 (Macintosh; Intel Mac OS X 14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36","Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0","Mozilla/5.0 (Windows NT 11.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0","Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:131.0) Gecko/20100101 Firefox/131.0","Mozilla/5.0 (X11; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0","Mozilla/5.0 (Macintosh; Intel Mac OS X 14.6; rv:131.0) Gecko/20100101 Firefox/131.0"]
            txt_1 = requests.get(f'https://callfilter.app/{num}',headers={'User-Agent':random.choice(us_ag)})
            if txt_1.status_code == 200:
                txt_1 = BeautifulSoup(txt_1.text,'html.parser').find_all('span',class_="review_comment")
                if txt_1 is not None:
                    for txt in txt_1:
                        review_arr.add(txt.get_text(strip=True))
            txt_2 = requests.get(f'https://www.telefonnyjdovidnyk.com.ua/nomer/{num}',headers={'User-Agent':random.choice(us_ag)})
            if txt_2.status_code == 200:
                txt_2 = BeautifulSoup(txt_2.text,'html.parser').find('span',id='count-comments')
                if txt_2 is not None:
                    txt_2 = math.ceil(float(re.sub('×','',txt_2.get_text(strip=True)))/12)
                for rev in range(1 if txt_2 == 1 else txt_2):
                    txt_3 = BeautifulSoup(requests.get(f'https://www.telefonnyjdovidnyk.com.ua/nomer/{num}/p/{rev}',headers={'User-Agent':random.choice(us_ag)}).text,'html.parser').find_all('p',class_="comment-text")
                    for txt in txt_3:
                        review_arr.add(txt.get_text(strip=True))
            if len(review_arr) >= 10:
                num_oper = ['intertelecom','kyivstar','lifecell','vodafone','3mob']
                for oper in num_oper:
                    txt_4 = requests.get(f'https://ua.whokla.com/{oper}/{num}',headers={'User-Agent':random.choice(us_ag)})
                    if txt_4.status_code == 200:
                        txt_4 = BeautifulSoup(txt_4.text,'html.parser').find_all('div',class_='comment-content')
                        for txt in txt_4:
                            review_arr.add(txt.get_text(strip=True))
                comment_score_arr = {}
                score_ai = joblib.load(r'C:\Users\avdim\Desktop\MyApps\CN\ail\AI.joblib')
                for filt in review_arr:
                    filt = filt.lower()
                    filt = re.sub(r'(' + '|'.join(map(re.escape, ['(програвався запис / робот)','(розмовляв чоловік)','(німий дзвінок / скидання)','Повідомлення від адміністратора сайту telefonnyjdovidnyk.com.ua«Допоможіть іншим відвідувачам сайту тим, що поділитеся з ними своїм досвідом спілкування з цим абонентом. Коли Вам з цього номеру телефонували і як часто? Що було предметом розмови, якщо Ви підняли трубку? Коментар, який Ви відіслали, буде показаний на цьому сайті.»','Оцінка:Шахрай','Оцінка:Спамер','Оцінка:Незрозуміло','Оцінка:Безпечно','Оцінка:Корисно'])) + r')','',filt,flags=re.IGNORECASE)
                    filt = re.sub(re.compile("[""\U0001F600-\U0001F64F""\U0001F300-\U0001F5FF""\U0001F680-\U0001F6FF""\U0001F1E0-\U0001F1FF""\U00002700-\U000027BF""\U0001F900-\U0001F9FF""\U0001FA70-\U0001FAFF""\U00002600-\U000026FF""]+",flags=re.UNICODE),'',filt)
                    filt = re.sub(r'https?://\S+','',filt)
                    filt = re.sub(r'[\r\n]+', ' ', filt)
                    filt = re.sub(r'\s+', ' ', filt).strip()
                    filt = re.sub(r'[^a-za-я0-9\s]','',filt)
                    if filt != '':
                        answai = float(score_ai.predict([filt])[0])
                        score = {0.0:5,0.5:4,1.0:3,2.0:2,3.0:1}
                        comment_score_arr[filt] = score.get(answai, 0)
                rep = Counter(comment_score_arr.values())
                scres = []
                for key,val in rep.items():
                    scres.append(key * val)
                client = genai.Client(api_key='AIzaSyBRdSK5BOr7oYjKbfFG_97BhxDCNxR_s0I')
                async with Session() as session:
                    async with session.begin():
                        for comm in comment_score_arr:
                            session.add(AllComments(comment=comm))
                        try:
                            resp_1 = client.models.generate_content(model='gemini-2.5-flash',contents=f'Проанализируй следующие комментарии, связанные с номером телефона:\n{list(comment_score_arr.keys())}\nОтветь строго одной цифрой:\n1 — если комментарии указывают, что номер телефона принадлежит, прикидывается или связан с организацией, банком, компанией или службой поддержки;\n0 — если комментарии говорят о чём-то другом.\nОтвет должен быть только цифрой, без пояснений.')
                            if resp_1:
                                comment_for_ai = []
                                for key,val in comment_score_arr.items():
                                    if val == 1.0 or 3.0:
                                        comment_for_ai.append(key)
                                resp_2 = client.models.generate_content(model='gemini-2.5-flash',contents=f'На основе комментариев, связанных с номером телефона:\n{comment_for_ai}\nСформулируй краткую рекомендацию на украинском языке: стоит ли доверять этому номеру телефона.\nПосле рекомендации приведи до 10 комментариев из списка, которые лучше всего подтверждают твой вывод.\nФормат вывода:\nРекомендация:\n<текст>\nПодтверждающие комментарии:\n1. <комментарий 1>\n2. <комментарий 2>\n...')
                            else:
                                resp_2 = client.models.generate_content(model='gemini-2.5-flash',contents=f'На основе комментариев, связанных с номером телефона:\n{comment_score_arr.keys()}\nСформулируй краткую рекомендацию на украинском языке: стоит ли доверять этому номеру телефона.\nПосле рекомендации приведи до 10 комментариев из списка, которые лучше всего подтверждают твой вывод.\nФормат вывода:\nРекомендация:\n<текст>\nПодтверждающие комментарии:\n1. <комментарий 1>\n2. <комментарий 2>\n...')
                            resp_3 = client.models.generate_content(model='gemini-2.5-flash',contents=f'На основе комментариев, относящихся к номеру телефона:\n{comment_score_arr.keys()}\nВыбери не более 10 комментариев, которые наиболее полно и точно характеризуют этот номер телефона. Ответ должен быть без твоего ответа просто комментарии.\nФормат вывода:1. <комментарий 1>\n2. <комментарий 2>\n...')
                            resp_2 = resp_2.text
                            resp_3 = resp_3.text
                            rating = round(sum(scres) / len(comment_score_arr.keys()), 1)
                            created_at = str(datetime.today().date())
                        except (google.genai.errors.ServerError,google.genai.errors.ClientError):
                            session.add(Numbers(number=num,last_10_comments='AI is overloaded, please try again later.',answer_ai='AI is overloaded, please try again later.',rating=round(sum(scres) / len(comment_score_arr.keys()),1),created_at=datetime.today().date()))
                        else:
                             session.add(Numbers(number=num,last_10_comments=resp_3,answer_ai=resp_2,rating=rating,created_at=created_at))
                        session.commit()
                    return {"number":num,"last_10_comments":resp_3,"answer_ai":resp_2,"rating":rating,"created_at":created_at}
            else:
                return {"Phone number details":"There is not enough data to rate the phone."}
    async def main():
        if await all_num() is True:
            return await ret_num()
        else:
            return await ai_help()
    return await main()