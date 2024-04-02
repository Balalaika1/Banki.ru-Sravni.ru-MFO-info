import re
import requests
from datetime import datetime
import lxml

from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st

from sravni import sravni_excel


st.markdown('<h2>Рейтинг МФО на сайтах Banki.ru и Sravni.ru</h2>', unsafe_allow_html=True)
my_bar = st.progress(0)
progress_text = "Коллега, возможно тебе покажется, что сайт долго обновляется, но это все равно быстрее чем твой компьютер! 😉"
if st.button('Refresh'):
    my_bar = st.progress(0, text=progress_text)

current_datetime = datetime.now().strftime('%Y-%m-%d')

def extract_digits(s): # Функция, убирает из строки все кроме цифр и точки
    return re.sub(r'[^\d.]', '', s)

# Перечисляем список компаний и ссылку для подстановки
companies = ['ekapusta', 'moneyman', 'zaymer', 'webbankir', 'carmoney', 'bistrodengi', 'lime_zaim', 'kvatro', 'boostra', 'revotekhnologii', 'medium_score', 'zaymigo', 'dengi_srazu', 'cashdrive', 'turbozajm', 'joymoney', 'privsosed', 'centrofinans', 'oneclickmoney', 'migkredit', 'maxcredit', 'cash_u', 'sammit', 'pliskov', 'bystrozaym', 'moneza', 'umnye_nalichnye', 'smsfinance', 'creditter', 'svoi_ludi', 'otlichnye_nalichnye', 'budgett', 'krediska', 'paylate', 'kangaria', 'payps', 'microdengi', '495credit', 'kredito24', 'ezaem', 'konga', 'mobicredit', 'belkacredit', 'beriberu', 'strana_express', 'denga', 'fastmoney', 'vivus', 'caranga', 'otp_finance', 'celfin', 'grinmani', 'dengi_na_dom', 'micro_klad', 'zaimy_rf', 'creditstar', 'chestnoye_slovo', 'alizaim', 'rosdengi', 'uralsibfinance', 'knopkadengi', 'erck', 'vsegdazaem', 'finterra', 'finmoll', 'vivadengi', 'creditplus', 'webzaim', 'zaim_express', 'kupi_ne_kopi', 'air_loanse', 'a_dengi', 'fin5', 'srochno_dengi', 'do_zarplati', 'ykky', 'moneyfaktura', 'daem_zaem', 'credit_smile', 'ren_express', 'express_dengi', 'buro_zaimov', 'sovazaem', 'platiza', 'express_zaimy', 'fast-finance', 'galiciya']
url = 'https://www.banki.ru/microloans/responses/companies/'

# Создаем словарь да добавления данных
table_names = {'company_name':[],'main_rait':[],'position':[],'review':[],'answer':[],'positive_reviews':[],'negative_reviews':[],'fast_issuance':[],'good_employee':[],'transparent_conditions':[],'convenience_application':[],'date':[]}

n = 1
# Создаем цикл для перечислени явсех компаний
for i in companies:
    print(f'{n} / {len(companies)}')
    data = requests.get(f'{url}{i}')
    site = data.text
    site = BeautifulSoup(site,'lxml')

    # выгружаем название компании
    company_name = site.find(class_ = 'CompanyHeadstyled__TextHeaderInnerStyled-sc-1co238g-4 gcdYkQ')
    table_names['company_name'].append(company_name.text.replace('Отзывы клиентов МФО ',''))

    # Основной рейтинг
    main_rait = site.find(class_ = 'TextResponsive__sc-hroye5-0 cvpJFV RatingsBadgestyled__StyledBadgeTitle-sc-13iioj7-1 hdjwXJ')
    table_names['main_rait'].append(float(main_rait.text))

    # Место
    position = site.find_all(class_ = 'TextResponsive__sc-hroye5-0 yFKzy')
    table_names['position'].append(int(extract_digits(position[0].text)))

    # Отзывы
    review = site.find_all(class_ = 'TextResponsive__sc-hroye5-0 yFKzy')
    table_names['review'].append(int(extract_digits(review[1].text)))

    # Ответы
    answer = site.find_all(class_ = 'TextResponsive__sc-hroye5-0 yFKzy')
    table_names['answer'].append(int(extract_digits(answer[2].text)))

    # Позитивные отзывы
    positive_reviews = site.find_all(class_ = 'TextResponsive__sc-hroye5-0 fuLnVY')
    table_names['positive_reviews'].append(float(extract_digits(positive_reviews[0].text)))

    # Негативные отзывы
    negative_reviews = site.find_all(class_ = 'TextResponsive__sc-hroye5-0 hsovst')
    table_names['negative_reviews'].append(float(extract_digits(negative_reviews[0].text)))

    # Быстрая выдача
    fast_issuance = site.find_all(class_ = 'TextResponsive__sc-hroye5-0 bILYor')
    table_names['fast_issuance'].append(float(extract_digits(fast_issuance[0].text)))

    # Вежливые сотрудники
    good_employee = site.find_all(class_ = 'TextResponsive__sc-hroye5-0 bILYor')
    table_names['good_employee'].append(float(extract_digits(good_employee[1].text)))

    # Прозрачные условия
    transparent_conditions = site.find_all(class_ = 'TextResponsive__sc-hroye5-0 bILYor')
    table_names['transparent_conditions'].append(float(extract_digits(transparent_conditions[2].text)))

    # Удобство приложения, сайта
    convenience_application = site.find_all(class_ = 'TextResponsive__sc-hroye5-0 bILYor')
    table_names['convenience_application'].append(float(extract_digits(convenience_application[3].text)))

    # Дата выгрузки
    table_names['date'].append(current_datetime)

    my_bar.progress(n, text=progress_text)

    n = n+1

df = pd.DataFrame(table_names)


df.to_excel(f'banki_ru.xlsx')


df2 = sravni_excel()

#df.to_excel(f'banki_ru_{current_datetime}.xlsx')

my_bar.empty()

st.dataframe(df)
with open("banki_ru.xlsx", "rb") as file:
                btn = st.download_button(
                    label="Download excel banki.ru",
                    data=file,
                    file_name="banki_ru.xlsx"
                )
st.dataframe(df2)
with open("sravni_ru.xlsx", "rb") as file:
                btn2 = st.download_button(
                    label="Download excel sravni.ru",
                    data=file,
                    file_name="sravni_ru.xlsx"
                )
