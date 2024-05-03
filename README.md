# WEEK 1

🔗 [Writing your first Django app, part 1](https://docs.djangoproject.com/en/5.0/intro/tutorial01/)

## Django Project 생성

```
django-admin startproject mysite
```

- `mysite`라는 Project 생성
- Project: 하나의 큰 웹사이트를 의미

## development server 실행

```
py manage.py runserver
```

- 명령어 맨 뒤에 원하는 port 번호 추가 시, 변경 가능

## app 생성

```
py manage.py startapp APP_NAME
```

- Project는 여러 app들로 구성된다.
- 웹 사이트 내부 페이지 개념이라고 생각하면 될 듯!

## view 설정

```
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
```

- polls app의 view를 설정한다.

## url 매핑

```
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("polls/", include("polls.urls")),
    path("admin/", admin.site.urls),
]
```

- 위에서 설정한 view를 설정하기 위해서는 url을 연결해야한다.
- urls.py 파일에 url와 view의 매핑을 작성한다.
- 생성한 app dir 내부에 /urls.py 를 생성하고
- project dir의 urls.py에 url을 추가한다.
- include()
  - 다른 URLconf를 참조할 수 있게 도와주는 함수
  - admin.site.urls를 제외한 그 외 URL 패턴에는 반드시 사용해야한다.

## 결과 화면

![image](https://github.com/naya-h2/Django-Study/assets/103186362/dbda387b-da30-4513-a7ad-72d860cfd634)

- `/polls/` url에 접근했을 때 작성한 view가 보이는 것을 확인할 수 있다.
