# -*- coding: utf-8 -*-
"""
Created on Sun Oct  9 21:57:23 2022

@author: yousef walid
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import time
from urllib.request import urlopen
import urllib.parse
import plotly.express as px
def address(soup):
    city=[]
    gover=[]
    coun=[]
    titles=soup.find_all("span", attrs={"class":"css-5wys0k"})
    for ti in titles:
        te=ti.text
        li=te.split(',')
        for i in range(3):
            if len(li)==3:
            
                    if i==0 :
                        city.append(li[i])
                    elif i==1 :
                         gover.append(li[i])
                    elif i==2:
                          coun.append(li[i])
            else:
                    city.append(li[0])
                    gover.append(None)
                    coun.append(li[1])
                    break
    return city ,gover , coun
            
def lo(x):
    address = x +'%2Cegypt'
    url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'
    response = requests.get(url).json()
    return response[0]["lat"], response[0]["lon"]
def add_log(country_df) :
        long=[]
        att=[]
        country_df = pd.DataFrame(data=[country_df["city"].value_counts().index, country_df["city"].value_counts().values],index=['city','count']).T
        for ci in country_df["city"] :
                try :
                              x,y=lo(ci)
                              long.append(x)
                              att.append(y)
                except :
                                long.append(None)
                                att.append(None)
        country_df = pd.DataFrame(data=[country_df["city"].values, country_df["count"].values,long,att],index=['city','count','logutuid','atte']).T                    
        country_df['logutuid']=pd.to_numeric(country_df['logutuid'])
        country_df['atte']=pd.to_numeric(country_df['atte'])
        country_df['count']=pd.to_numeric(country_df['count'])
        return country_df
def name_com(soup):
    list=[]
    titles=soup.find_all("a", attrs={"class":"css-17s97q8"})
    for ti in titles:
        list.append(ti.text)
    return list
def type_job(soup):
    list=[]
    titles=soup.find_all("div", attrs={"class":"css-1lh32fc"})
    for ti in titles:
        ti.text.replace(" ","")
        list.append(ti.text)
    return list
def titles(soup):
    list=[]
    titles=soup.find_all("h2",attrs={"class":"css-m604qf"})
    for ti in titles:
        list.append(ti.text)
    return list
def dates(soup):
    list=[]
    titles=soup.find_all("div", attrs={"class":"css-do6t5g","class":"css-4c4ojb"})
    for ti in titles:
        list.append(ti.text)
    return list


# In[9]:


def skills(soup):
    list=[]
    typ=[]
    titles=soup.find_all("div", attrs={"class":"css-pkv5jc"})
    i=0
    for ti in titles:
        a=ti.find('div',attrs={"class":None})
        a=a.find_all('a')
        list.append([l.text for l in a])
        typ.append(list[i][0])
        del list[i][0]
        i+=1
    return list,typ


# In[10]:


def exp(soup):
    minn=[]
    maxx=[]
    titles=soup.find_all("div", attrs={"class":"css-pkv5jc"})
    for ti in titles:
        sk=ti.find('div',attrs={"class":None})
        try :
            data=sk.find("span")
            x=data.text
        except :
           x='0'
        try :
            x=x.split('-')
            x[1]=x[1].replace('Yrs of Exp',"")
            x[0]=x[0].replace('· ',"")
            minn.append(x[0])
            maxx.append(x[1])
        except :
            x[0]=x[0].replace('+ Yrs of Exp',"")
            x[0]=x[0].replace('Yrs of Exp',"")
            x[0]=x[0].replace('· ',"")
            minn.append(x[0])
            maxx.append(None)
    return minn ,maxx


# In[11]:


def links(soup):
    list=[]
    for a in soup.find_all('div',attrs={'class':'css-laomuu'}):
        lin='https://www.wuzzuf.net'+ a.find('h2').find('a')['href']
        lin = lin.replace(" ", "%20")
        list.append(lin)
    return list


# In[12]:


def desc(soup):
    desc_i=[]
    links1=links(soup)
    for i in links1:
            time.sleep(1)
            i = i.replace(" ", "%20")
            i = i.encode('ascii', 'ignore').decode('ascii')
            html=urlopen(i)
            soupi=BeautifulSoup(html.read(),'html.parser')
            description=[]
            desc=soupi.find('div',attrs={'class':'css-1uobp1k'}).find_all('p')
            for k in desc:
                description.append(str(k.text).strip())
            desc_i.append(description)
    return description


# In[13]:


def logo(soup):
    logos=[]
    hd={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}
    data=soup.find_all('div',{'class':'css-1gatmva e1v1l3u10'})
    for i in data:
        d=i.find('div',{'class':'css-pkv5jc'}).find_all('a')[0]
        if 'href' in d.attrs:
            l = d['href']
            l = l.replace(" ", "%20")
            l = l.encode('ascii', 'ignore').decode('ascii')
            lin = requests.get(l,timeout=4000,headers=hd).text
            soup2 = BeautifulSoup(lin)
            try :
                imgs=soup2.find('img',{'class':'css-qldhfy'})['src']
                logos.append(imgs)
            except :
                logos.append('None')
    return logos


# In[14]:


def trans(list1,list2):
    for li in list2:
        list1.append(li)
    return list1


# In[15]:


def pages(page_num,url) :
    title=[]
    date=[]
    name_comp=[]
    skillss=[]
    type_j=[]
    city=[]
    gov=[]
    count=[]
    minn=[]
    maxx=[]
    logos=[]
    lin=[]
    desc1=[]
    catg=[]
    url=f'?a=navbg&q={url}&start='
    url = url.replace(" ", "%20")
    hd={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}
    for i in range(page_num):
        time.sleep(10)
        resp = requests.get(f"https://www.wuzzuf.net/search/jobs/{url}{i}",timeout=4000,headers=hd).text
        soup = BeautifulSoup(resp)
        title=trans(title,titles(soup))
        date=trans(date,dates(soup))
        name_comp=trans(name_comp,name_com(soup))
        sk,ty=skills(soup)
        skillss=trans(skillss,sk)
        catg=trans(catg,ty)
        type_j=trans(type_j,type_job(soup))
        x,y,z=address(soup)
        city=trans(city,x)
        gov=trans(gov,y)
        count=trans(count,z)
        mi,mx=exp(soup)
        minn=trans(minn,mi)
        maxx=trans(maxx,mx)

    return title,date,name_comp,skillss,type_j,catg,city,gov,count,minn,maxx
import streamlit as st 
# "with" notation
with st.sidebar:
   st.header("Hi, I am youssef walid :wave:")
   st.header("search for your dream job and Analysis it" )
   title1=st.text_input('Name for a job', '')
   st.write('The current job title is', title1)

if  st.sidebar.button('search') :
      title,date,name_comp,skillss,type_j,catg,city,gov,count,minn,maxx=pages(8,title1)
      a={"Job Title": title,"Company_name": name_comp, "skills": skillss,"category":catg,'city':city,'goverment':gov,"country":count,"type_job":type_j,'min_exp':minn,"max_exp":maxx}
      df = pd.DataFrame.from_dict(a, orient='index')
      df = df.transpose()
  
      st.title(f"{title1}jobs visualization at wazzuf:")
      df
      @st.cache
      def convert_df(df):
          # IMPORTANT: Cache the conversion to prevent computation on every rerun
          return df.to_csv().encode('utf-8')

      csv = convert_df(df)

      st.download_button(
          label="Download data as CSV",
          data=csv,
          file_name='datast.csv',
          mime='text/csv',
      )
      country_df=add_log(df)
      st.subheader("visualization for city bubble map :")
      fig=px.scatter_mapbox(
     country_df,
      lat="logutuid",
      lon="atte",
      hover_name="city",
      size="count",
  ).update_layout(mapbox={"style": "carto-positron", "zoom": 4}, margin={"t":0,"b":0,"l":0,"r":0})
      st.plotly_chart(fig, use_container_width=True) 
      st.write("-----------------------------------------------------------------------")
      st.subheader("visualization for category :")
      cat = pd.DataFrame(data=[df["category"].value_counts().index, df["category"].value_counts().values],index=['category','count']).T
      fig = px.bar(cat, x='category', y='count',hover_data=['category', 'category'], color='category',height=400)
      st.plotly_chart(fig, use_container_width=True)       
      st.write("-----------------------------------------------------------------------")
      st.subheader("visualization for category Entry Level:")
     # ## visualization for category Entry Level:

      c=df[df['category']=='Entry Level']
      skills=[]
      for ski in c['skills'] :
            for s in ski :
                skills.append(s)
      ski=pd.DataFrame({'skills':skills})
      softskills=[' · English',' · Microsoft Office',' · MS Office','· MS excel','· Project management',' · Communication skills',' · Financial Management',' · Marketing',' · QA',
                   ' · Market Research',' · Research','Administration',' · Communication',' · IT/Software Development',' · Pharmaceutical'," · Customer Service",' · Quality Assurance',' · accountant'
                   ," · Customer Care", ' · Customer Service/Support',' · Quality'," · Microsoft Excel",' · Planning',' · Pharmaceutical Sciences',' · Bookkeeping'," · Marketing/PR/Advertising",' · R&D/Science',
                   ' · quality',' · Quality Control',' · Financial Reporting',' · Social Media',' · Presentation Skills',' · Accounts Payable',' · Logistics/Supply Chain',' · excel',' · Skills',
                ]

      list=[]
      for sk in ski['skills'] :
            if sk not in softskills :
                list.append(sk)
      ski=pd.DataFrame({'skills':list})
      c= pd.DataFrame(data=[ski['skills'].value_counts().index, ski['skills'].value_counts().values],index=['skills','count']).T
      c=c[c['count']>1]
      
      fig = px.bar(c, x='skills', y='count',
                   hover_data=['skills', 'count'], color='skills',
                   height=1000)
      st.plotly_chart(fig, use_container_width=True) 
      st.write("-----------------------------------------------------------------------")
      st.subheader("visualization for category Experienced :")
      c=df[df['category']=='Experienced']

      skills=[]
      for ski in c['skills'] :
            for s in ski :
                skills.append(s)
      ski=pd.DataFrame({'skills':skills})




      list=[]
      for sk in ski['skills'] :
         if sk not in softskills :
              list.append(sk)
      ski=pd.DataFrame({'skills':list})
      c1= pd.DataFrame(data=[ski['skills'].value_counts().index, ski['skills'].value_counts().values],index=['skills','count']).T
      c1=c1[c1['count']>5]
      fig = px.bar(c1, x='skills', y='count',
                  hover_data=['skills', 'count'], color='skills',
                  height=1000)
      st.plotly_chart(fig, use_container_width=True)      
      st.write("-----------------------------------------------------------------------") 
      c=df[df['category']=='Manager']
      skills=[]
      for ski in c['skills'] :
         for s in ski :
             skills.append(s)
      ski=pd.DataFrame({'skills':skills})

      list=[]
      for sk in ski['skills'] :
           if sk not in softskills :
                  list.append(sk)
      ski=pd.DataFrame({'skills':list})
      c3= pd.DataFrame(data=[ski['skills'].value_counts().index, ski['skills'].value_counts().values],index=['skills','count']).T
      c3=c3[c3['count']>1]
      st.subheader("visualization for category Manager :")
      fig = px.bar(c3, x='skills', y='count',
                                hover_data=['skills', 'count'], color='skills',
                                height=1000)
      st.plotly_chart(fig, use_container_width=True)      

      

