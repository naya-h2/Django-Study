# WEEK3

🔗 [Writing your first Django app, part 3](https://docs.djangoproject.com/en/5.0/intro/tutorial03/)

## View

- 특정 기능을 제공하고, 특정 템플릿을 가진 웹 페이지의 type이다.
- app의 로직을 넣는 부분
- model에서 필요한 정보를 받아와서 -> 템플릿에 전달
- 각 view는 Python 함수로 표현된다.

## View 추가하기

```py
#polls/views.py

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
```

- question_id는 URL의 query라고 생각하면 된다.

```py
#polls/urls.py

urlpatterns = [
    # ex: /polls/
    path("", views.index, name="index"),
    # ex: /polls/5/
    path("<int:question_id>/", views.detail, name="detail"),
    # ex: /polls/5/results/
    path("<int:question_id>/results/", views.results, name="results"),
    # ex: /polls/5/vote/
    path("<int:question_id>/vote/", views.vote, name="vote"),
]
```

- 각 URL에 맞는 view가 매핑될 수 있게 url에 등록

## View의 역할

- 요청된 페이지의 내용이 담긴 HttpResponse 객체를 return
- Http404 같은 예외를 발생
- 이외에도 PDF 생성, XML 출력, ZIP 파일 생성 등도 가능하지만 위의 2가지를 수행하도록 다루는 게 편리!

```py
#polls/views.py

def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5] #최근 생성된 Question 인스턴스 5개를 불러온다.
    output = ", ".join([q.question_text for q in latest_question_list]) #각 인스턴스의 question_text를 ,로 연결
    return HttpResponse(output)
```

### 실행 결과

![image](https://github.com/naya-h2/Django-Study/assets/103186362/04796d10-fa49-459a-a518-7c81f8254674)

## Template

- View에서는 로직을 담당하게 하고, Template에서 디자인을 담당하도록 역할을 분리한다.
- Template이 렌더링을 담당하게 되는 것 !

```py
#polls/views.py

def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    template = loader.get_template("polls/index.html") #templates 폴더에서 해당 파일(템플릿)을 찾는다.
    context = {
        "latest_question_list": latest_question_list,
    }
    return HttpResponse(template.render(context, request)) #template에 context를 전달하고, 해당 화면 렌더링
```

```py
#polls/templates/polls/index.html

{% if latest_question_list %}
<ul>
  {% for question in latest_question_list %}
  <li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
  {% endfor %}
</ul>
{% else %}
<p>No polls are available.</p>
{% endif %}
```

- 위처럼 html 파일이 렌더링된다.

## render()

-

```py
#polls/views.py

from django.shortcuts import render

def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context) #이런식으로 작성하면 loader와 HttpResponse를 가져오지 않아도 된다.
```

- render(request 객체, 템플릿 이름, context 객체(optional))
- return값: context로 표현된 템플릿의 HttpResponse 객체

## 404 에러 일으키기

```py
def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id) #question_id에 맞는 Question 인스턴스 찾기
    except Question.DoesNotExist: #존재하지 않는 경우에
        raise Http404("Question does not exist") #404 에러 던지기
    return render(request, "polls/detail.html", {"question": question})
```

### 실행 결과

![image](https://github.com/naya-h2/Django-Study/assets/103186362/9c696a29-5a74-4a6d-aa35-b3526ed8fe31)

- id값이 4인 Question 데이터가 없으므로 404 에러

## get_object_or_404()

```py
from django.shortcuts import get_object_or_404, render

from .models import Question

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id) #바로 model과 찾는 조건 전달
    return render(request, "polls/detail.html", {"question": question})
```

- 객체가 존재하지 않을 때 get()을 사용해 Http404 예외를 발생시키는 shortcut
- 비슷하게 `get_list_or_404()` 함수도 존재

## 하나의 Project에 여러 app이 있는 경우

```py
app_name = "polls"
```

- 각 app의 urls.py에 namespace를 추가
