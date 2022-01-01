from django.shortcuts import render
import requests
from bs4 import BeautifulSoup as bs

# Create your views here.

def home(request):
    if request.method == 'POST':
        st = request.POST.get('search')
        if st:
            s_data=search(st)
            if len(s_data) > 0:
                return render(request,'index.html',{'datas':s_data})
            else:
                return render(request,'index.html')
        else:
            return render(request,'index.html',{'datas':scrapper()})
    else:
        return render(request,'index.html',{'datas':scrapper()})



#scrapped data from 
def scrapper():
    page = requests.get("https://www.weather-forecast.com/countries/Cameroon")
    soup = bs(page.content,'html.parser')

    content = soup.select('span.temp')
    degree = [con.get_text() for con in content]

    data = soup.select('span.b-list-table__item-name a')
    names = [t.get_text() for t in data]

    altText = soup.select('span.b-list-table__item-value div img')
    text = [t.get('alt').split()[0] for t in altText]
    alt = [t.get('alt') for t in altText]
    #print(text)

    dict = []

    for j in range(0,len(names)):
        dict1 ={'town':names[j],'degree':degree[j],'alt':alt[j],'sub_image':'images/'+text[j]+'.png','image':'images/'+text[j]+'.jpg'}
        dict.append(dict1)

    return dict

#give result according to user search
def search(str):
    dict = scrapper()
    k = []
    for t in dict:
        if t['town'] == str:
            k.append(t)
            break
    
    return k
