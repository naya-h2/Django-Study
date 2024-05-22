# WEEK5

🔗 [Writing your first Django app, part 5](https://docs.djangoproject.com/en/5.0/intro/tutorial05/)

🔗 [Writing your first Django app, part 6](https://docs.djangoproject.com/en/5.0/intro/tutorial06/)

## automated testing

- 코드 작동을 확인하는 루틴
- 시스템에서 수행
- 테스트 코드를 추가해놓으면 코드를 변경할 때마다 직접 테스트해볼 필요가 없다.

## test가 필요한 이유

- 시간 절약
  - 프로젝트가 커졌을 때, 컴포넌트 하나로 인해 프로젝트 전체 동작이 망가질 수 있다.
  - automated test code를 작성한다면 잘못된 부분을 시스템 상에서 알아서 찾아낼 것!
  - 나중에 직접 문제의 원인을 파악하기 위해 디버깅하는 것보다 시간 절약
- 문제 예방
  - 자신의 코드가 정확히 무엇을 하고 있는지 직접 알아낼 필요 없이 테스트를 통해 알 수 있다.
- 신뢰도 상승
  - 테스트 없는 코드는 설계상 망가져 있는 것
  - 아무리 잘 만든 소프트웨어라도, 테스트가 없다면 신뢰도가 쌓이지 않는다.
- 협업 시 유리
  - 다른 사람이 작성한 코드를 나도 모르게 손상시켰는지 확인 가능

## Test 전략: TDD

- TDD(Test Driven Development)란?
  - 작은 단위의 (실패할) TC를 작성하고, 해당 TC를 해결하기 위한 코드를 작성
  - 위의 단계를 반복하여 구현
  - 짧은 개발 주기의 반복

## 버그가 존재한다!

```py
>>> import datetime
>>> from django.utils import timezone
>>> from polls.models import Question
>>> future_question = Question(pub_date=timezone.now() + datetime.timedelta(days=30)) #현재 날짜로부터 30일 뒤로 pub_date를 설정
>>> future_question.was_published_recently()
True #future_question의 pub_date가 미래인데도 불구하고 True를 return! => 에러!
```

- 현재 polls 어플리케이션의 Question.was_published_recently() 메소드에 버그가 있다!

## 버그를 알 수 있는 테스트 코드 작성하기

```py
#polls/tests.py

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30) #미래 시간대 생성
        future_question = Question(pub_date=time) #미래 시간대로 Question 생성
        self.assertIs(future_question.was_published_recently(), False) #False(정해진 정답)가 나오는지 확인
```

## 작성한 테스트 코드 실행하기

실행 방법

```shell
python manage.py test polls
```

실행 결과

```
self.assertIs(future_question.was_published_recently(), False) #False(정해진 정답)가 나오는지 확인
AssertionError: True is not False
```

- return값(True)이 우리가 지정한 답인 False가 아니라는 것을 Test 코드를 통해 바로 확인할 수 있다.

## View 테스트

- pub_date가 미래인 Question은 그때까지 화면에 보이지 않아야 한다.

## Django Test Client

- Django가 View 레벨에서 코드와 상호 작용하는 유저를 시뮬레이션하기 위해 Test Client Class인 `Client` 제공

```py
>>> from django.test.utils import setup_test_environment
>>> setup_test_environment() #템플릿 renderer 설치
```

- shell에서 테스트 환경을 구성해야 한다.
- 따로 테스트 DB를 설정하지 않기 때문에 기존 DB에 대해 테스트 실행

```py
>>> from django.test import Client
>>> # create an instance of the client for our use
>>> client = Client()
>>> # get a response from '/'
>>> response = client.get("/")
Not Found: /
>>> # we should expect a 404 from that address; if you instead see an
>>> # "Invalid HTTP_HOST header" error and a 400 response, you probably
>>> # omitted the setup_test_environment() call described earlier.
>>> response.status_code
404
>>> # on the other hand we should expect to find something at '/polls/'
>>> # we'll use 'reverse()' rather than a hardcoded URL
>>> from django.urls import reverse
>>> response = client.get(reverse("polls:index"))
>>> response.status_code
200
>>> response.content
b'\n<ul>\n  \n  <li><a href="/polls/3/">\xec\x9d\xb4\xeb\xa6\x84\xec\x9d\xb4 \xeb\xad\x90\xec\x95\xbc?</a></li>\n  \n  <li><a href="/polls/2/">\xec\xa7\x88\xeb\xac\xb82</a></li>\n  \n  <li><a href="/polls/1/">\xec\xa7\x88\xeb\xac\xb8\xec\x9d\x84 \xec\xa0\x81\xec\x9e\x90!</a></li>\n  \n</ul>\n\n'
>>> response.context["latest_question_list"] #최신순으로 정렬된 Question list
<QuerySet [<Question: 이름이 뭐야?>, <Question: 질문2>, <Question: 질문을 적자!>]>
```

---

## static file namespacing

- polls/static/polls 디렉토리 내에서 정적 파일 추가
- 장고는 이름이 일치하는 첫 번째 정적 파일 선택
- 다른 응용프로그램에 같은 이름이 있으면 구별을 못하니까 따로 디렉토리를 생성한다.
- static 파일에 .css, images 디렉토리(사진) 등을 만들수 있다.
