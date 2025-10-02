import re
import pandas
from sklearn.model_selection import train_test_split,cross_val_score,GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor
import joblib
def ail(path_for_learn,path_for_save):
    r_inf = []
    with open(path_for_learn,encoding='UTF-8') as r:
        for row in r:
            m = re.match(r'^\s*(\d+(?:\.\d+)?)\s*-\s*(.+)$',row)
            sco = float(m.group(1))
            txt = m.group(2).lower()
            txt = re.sub(r'https?://\S+','<URL>',txt)
            txt = re.sub(r'[\r\n]+',' ',txt)
            txt = re.sub(r'\s+',' ', txt).strip()
            r_inf.append((sco,txt))
    fil_r = pandas.DataFrame(r_inf,columns=['Sco','Txt'])
    x = fil_r['Txt']
    y = fil_r['Sco']
    x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,random_state=42,stratify=y)
    pil = Pipeline([
        ('TF-IDF', TfidfVectorizer(ngram_range=(1,2),min_df=2)),
        ('RFR', RandomForestRegressor(n_estimators=500,random_state=42))
    ])
    pil.fit(x_train,y_train)
    y_pred = pil.predict(x_test)
    print('MSE:',mean_squared_error(y_test,y_pred))
    print('R^2:',r2_score(y_test,y_pred))
    joblib.dump(pil,f'{path_for_save}\AI.joblib')
ail(r'C:\Users\avdim\Desktop\MyApps\CheckNum\Ail\AIL.txt',r'C:\Users\avdim\Desktop\MyApps\CheckNum\Ail')