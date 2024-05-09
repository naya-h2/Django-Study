# WEEK4

🔗 [Writing your first Django app, part 4](https://docs.djangoproject.com/en/5.0/intro/tutorial04/)

## Question(pk=1)에 대해 choice 데이터 추가

![image](https://github.com/naya-h2/Django-Study/assets/103186362/dcff5278-b4e0-4df6-b429-aa96af81389f)

- python shell 이용

## Form 생성하기 => POST 메소드 구현 (vote view)

![image](https://github.com/naya-h2/Django-Study/assets/103186362/842f3ffe-80a0-4599-9784-031c5a7cd72b)

- detail.html 파일에 form 태그 추가
- `{% csrf_token %}`
  - Django에서는 Cross Site Request Forgeries (CORS 에러인듯?!)를 위해서 자체 보호 시스템을 가지고 있다.
  - 내부 URL을 대상으로 하는 모든 POST 양식은 해당 템플릿 태그를 사용해야 한다.

## POST 메소드의 request 처리하기

- views.py의 vote view 코드 참고

## response에 따라 results view 업데이트

- views.py의 results view 코드 참고

## Generic views

```py
#urls.py
from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"), #question_id -> pk로 변경
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"), #ResultsView
    path("<int:question_id>/vote/", views.vote, name="vote"),
]
```

- 코드를 적게 만들어 보자! 는 전략
- 장고에서 기본적으로 제공하는 view 클래스
- 용도에 따라 종류가 다르다. 모두 View 클래스를 상속
  - ListView
  - DetailView
  - FormView
  - TemplateView
