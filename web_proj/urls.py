"""web_proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
# from django.conf.urls import include, path
from blog.views import post_list
from django.conf.urls import url
from django.urls import path
from django.contrib.auth import views
from blog.views import post_list, post_detail, post_add, post_delete, post_publish, graph, wordcloud, search, search_result, moreinfo, moreinfo_out,\
     sk_am,sk_pm, lg_am,lg_pm, kt_am, kt_pm, kakao_am, kakao_pm, samsung_pm, samsung_am, naver_am, naver_pm
from django.urls import path


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', post_list, name = 'home'),  # url 객체를 만들어준다.
    url(r'^post/(?P<pk>\d+)/', post_detail), 
    url(r'^post/add/$', post_add, name='post_add'),
    url(r'^post/(?P<pk>\d+)/delete/$', post_delete, name='post_delete'),
    url(r'^post/(?P<pk>\d+)/publish/$', post_publish, name='post_publish'),
    url(r'^post/search/', search, name='search'),
    url(r'^post/search_result/', search_result, name='search_result'), # (?P<slug>[-\w]+) 문자열 
    url(r'^post/graph/', graph, name='graph'),
    url(r'^post/wordcloud/', wordcloud, name="wordcloud"),
    url(r'^post/moreinfo/', moreinfo, name="moreinfo"),
    url(r'^post/moreinfo_out/', moreinfo_out, name="moreinfo_out"),


    url(r'^post/wordcloud/sk_am/$', sk_am, name="sk_am"),
    url(r'^post/wordcloud/sk_pm/$', sk_pm, name="sk_pm"),
    url(r'^post/wordcloud/lg_am/$', lg_am, name="lg_am"),
    url(r'^post/wordcloud/lg_pm/$', lg_pm, name="lg_pm"),
    url(r'^post/wordcloud/kt_am/$', kt_am, name="kt_am"),
    url(r'^post/wordcloud/kt_pm/$', kt_pm, name="kt_pm"),
    url(r'^post/wordcloud/kakao_am/$', kakao_am, name="kakao_am"),
    url(r'^post/wordcloud/kakao_pm/$', kakao_pm, name="kakao_pm"),
    url(r'^post/wordcloud/samsung_am/$', samsung_am, name="samsung_am"),
    url(r'^post/wordcloud/samsung_pm/$', samsung_pm, name="samsung_pm"),
    url(r'^post/wordcloud/naver_am/$', naver_am, name="naver_am"),
    url(r'^post/wordcloud/naver_pm/$', naver_pm, name="naver_pm"),
    # # url(r'^post/search', Mynews.as_view(), name='main'), # as_view()함수는 클래스의 인스턴스를 생성하고, 인스턴스의 dispatch()메소드를 호출
    
]