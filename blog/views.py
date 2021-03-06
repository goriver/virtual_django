# Shell Plus Model Imports
from .models import Post, NewsData, MoreData 

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.decorators import login_required
from django.utils.safestring import SafeString

# crawling code import
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import sys
from wordcloud import WordCloud

# wordcloud img
from PIL import Image

# mailing code import
from blog.mailing import EmailHTMLContent, EmailSender
from string import Template

# leejh
import blog.fbprophet_main as fbprophet_main

#jo


def post_list(request):
    req = requests.get('https://finance.naver.com/sise/lastsearch2.nhn')
    html = req.text

    status = req.status_code
    if status == 200:
        print('health')
    soup = BeautifulSoup(html, 'html.parser')

    name = soup.select('td > a.tltle ')
    stock_comp = []
    for na in name:
        stock_comp.append(na.text)
    count = soup.select('td:nth-child(3).number')
    cn_list = []

    for i in range(len(name)):
        temp = float(count[i].text.replace('%', ''))*100
        cn_list.append(int(temp))

    keyword = {}
    for i in range(len(cn_list)):
        keyword[stock_comp[i]] = cn_list[i]

    wc = WordCloud(font_path = 'C:\\Windows\\Fonts\\MALGUNSL.TTF', \
                background_color="white").generate_from_frequencies(keyword)
    im = wc
    im.to_file('static/bootstrap/img/wordcloud.jpg')

    posts = Post.objects.filter(published_date__isnull=False).order_by('-created_date')  # 수정된 부분
    context = {
        'posts': posts,
    }
    return render(request, 'blog/post_list.html', context)

def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    context={
        'post':post
    }
    return render(request, 'blog/post_detail.html', context)

def post_add(request):
    if request.method == 'POST':
        User = get_user_model()
        author = User.objects.get(username='nachwon')
        title = request.POST['title']
        content = request.POST['content']

        if title == '' or content == '':
            context = {
                'title': title,
                'content': content,
            }
            return render(request, 'blog/post_add.html', context)

        post = Post.objects.create(
            author=author,
            title=title,
            content=content,
        )

        try:
            if request.POST['publish'] == 'True':
                post.publish()
        except MultiValueDictKeyError:
            pass

        post_pk = post.pk

        return redirect(post_detail, pk=post_pk)

    elif request.method == 'GET':
        return render(request, 'blog/post_add.html')


def post_delete(request, pk):
    if request.method == 'POST':
        post = Post.objects.get(pk=pk)
        post.delete()
        return render(request, 'blog/post_delete.html')

    elif request.method == 'GET':
        return HttpResponse('잘못된 접근 입니다.')

def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

def graph(request):
    return render(request, 'blog/graph3.html')


def search(request):
    return render(request, 'blog/search.html')

def search_result(request):
    keyword = request.GET.get('search')


    title_list = []
    link_list = []
    img_list = []
    to_check = []
    text_list = []

    url = 'https://search.daum.net/search?w=news&nil_search=btn&DA=NTB&enc=utf8&cluster=y&cluster_page={0}&q={1}'.format(1, keyword)

    html = requests.get(url).text.strip()
    soup = BeautifulSoup(html, 'html5lib')
    news_link = soup.select('.coll_cont ul li a.f_link_b')


    for contents in news_link:
        link = contents.get('href')
        link_list.append(link)
        titles = contents.text
        title_list.append(titles)

    html = requests.get(url).text.strip() 
    soup = BeautifulSoup(html, 'html5lib')
    photos = soup.select("div.wrap_thumb div a img[src]")
    texts = soup.select("li > div.wrap_cont > div > p")

    for i in photos:
        img = i["src"]
        # print(len(img))
        img_list.append(img)

    for i in texts:
        text = i.get_text()
        text_list.append(text)

    for i in range(10):
        img = soup.select("#news_img_{0} > div > a > img[src]".format(i))
        to_check.append(img)

    for i, check in enumerate(to_check):
        if len(check) == 0:
            img_list.insert(i, "https://source.unsplash.com/bzVUPzDl9LQ/200x200")


    item_num = len(title_list)
    item_list = []
    for i in range(item_num):
        item_list.append(NewsData(title_list[i], img_list[i],text_list[i], link_list[i])) # title, image, summary, link

    context = {
        'default' : False,
        'keyword' : keyword,
        'items' : item_list,
        'length' : item_num

    }
    return render(request, 'blog/search_result.html', context)

def moreinfo(request):
    return render(request, 'blog/moreinfo.html')


def moreinfo_out(request):

    # post = MoreData.objects.create(
    #         email=email,
    #         content=content,
    # )
    # try:
    #     if request.POST['publish'] == 'True':
    #         post.register()
    # except MultiValueDictKeyError:
    #     pass

    email = request.GET.get('email')
    content = request.GET.get('content')
    published = request.GET.get('published')
    print(email)
    print(content)
    conv_content = conv_stock(content)
    print(conv_content)
    MoreData(email=email, content=content, published=conv_content).save()
    
    # code
    str_host = 'smtp.gmail.com'
    num_port = 587

    emailSender = EmailSender(str_host, num_port)

    str_subject = '안녕 디지몬' # e메일 제목
    template = Template("""<html>
                                <head></head>
                                <body>
                                    안녕 ${NAME}.<br>
                                    <img src="cid:my_image"> <br>
                                    내 꿈을 꾸면서 잠이 들래
                                </body>
                            </html>""")
    template_params = {'NAME':'디지몬'}
    str_image_file_name = 'static/bootstrap/img/post-bg.jpg'
    str_cid_name = 'my_image'
    emailHTMLContent = EmailHTMLContent(str_subject, str_image_file_name, template, template_params, str_cid_name)

    from_email_address =  'bziwnsizd@gmail.com' #발신자
    to_email_address = ['bziwnsizd@gmail.com','ka030202@kookmin.ac.kr','songteagyong@gmail.com','brttomorrow77@gmail.com'] #수신자리스트
    to_email_address.append(email)
    # 여기를 나중에 email로 append하기
    emailSender.send_message(emailHTMLContent, from_email_address, to_email_address)

    return render(request, 'blog/moreinfo_out.html')
def wordcloud(request):
    posts = Post.objects.filter(published_date__isnull=False).order_by('-created_date')  # 수정된 부분
    context = {
        'posts': posts,
        'defalut':False
    }
    return render(request, 'blog/wordcloud.html', context)



def sk_am(request):
    print("hello")
    am , pm = fbprophet_main.get_json()
    print(am, pm)
    print(am[0])
    context = {
        'day': SafeString(am),
        'corp':'sk',
    }
    return render(request, 'blog/chart_realtime.html', context)
def sk_pm(request):
    am , pm = fbprophet_main.get_json()
    context = {
        'day': SafeString(pm),
        'corp':'sk',
    }
    return render(request, 'blog/chart_realtime.html', context)

def kt_am(request):
    am , pm = fbprophet_main.get_json()
    context = {
        'day': SafeString(am),
        'corp':'kt',
    }
    return render(request, 'blog/chart_realtime.html', context)
def kt_pm(request):
    am , pm = fbprophet_main.get_json()
    context = {
        'day': SafeString(pm),
        'corp':'kt'
    }
    return render(request, 'blog/chart_realtime.html', context)
def lg_am(request):
    am , pm = fbprophet_main.get_json()
    print(am[0])
    context = {
        'day': SafeString(am),
        'corp':'lg',
    }
    return render(request, 'blog/chart_realtime.html', context)
def lg_pm(request):
    am , pm =fbprophet_main.get_json()
    context = {
        'day': SafeString(pm),
        'corp':'lg',
    }
    return render(request, 'blog/chart_realtime.html', context)
def kakao_am(request):
    am , pm =fbprophet_main.get_json()
    context = {
        'day': am,
        'corp':'kakao',
    }
    return render(request, 'blog/chart_realtime.html', context)
def kakao_pm(request):
    am , pm = fbprophet_main.get_json()
    context = {
        'day': SafeString(pm),
        'corp':'kakao',
    }
    return render(request, 'blog/chart_realtime.html', context)
def samsung_am(request):
    am , pm = fbprophet_main.get_json()
    context = {
        'day': SafeString(am),
        'corp':'samsung',
    }
    return render(request, 'blog/chart_realtime.html', context)
def samsung_pm(request):
    am , pm = fbprophet_main.get_json()
    context = {
        'day': SafeString(pm),
        'corp':'samsung',
    }
    return render(request, 'blog/chart_realtime.html', context)
def naver_am(request):
    am , pm =fbprophet_main.get_json()
    context = {
        'day': SafeString(am),
        'corp':'naver'
    }
    return render(request, 'blog/chart_realtime.html', context)
def naver_pm(request):
    am , pm = fbprophet_main.get_json()
    context = {
        'day': SafeString(pm),
        'corp':'naver'
    }
    return render(request, 'blog/chart_realtime.html', context)

def conv_stock(stock_name):
    content = stock_name
    url = 'https://search.daum.net/search?w=tot&DA=YZR&t__nil_searchbox=btn&sug=&sugo=&sq=&o=&q={0}'.format(content)
    html = requests.get(url).text.strip()
    soup = BeautifulSoup(html, 'html5lib')
    stock_num1 = soup.find("span", {"class":"txt_sub"}).get_text()
    stock_num = stock_num1[:6]
    #print(stock_num)
    
    return stock_num

    