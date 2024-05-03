# WEEK2

## DB 설치

```py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

- mysite/settings.py
  - Django 설정을 모듈 변수로 표현한 모듈
  - 기본적으로 SQLite 사용
  - 사용하는 DB 종류에 따라 해당 파일의 위 부분을 바꿔준다.
  - SQLite 이외의 DB를 사용하는 경우, 따로 환경 설정이 필요하다.
  - `TIME_ZONE = 'KST'` 시간대를 바꾼다.

```
py manage.py migrate
```

- DB Table을 만든다.
  - 적용되지 않은 migration들을 모두 수집해서 이를 반영시킴
- migrate
  - INSTALLED_APPS 설정을 보고, DB 설정 및 DB Table을 생성한다.
  - (SQLite) `.tables` 명령어로 생성된 Table 확인 가능

## Model 생성

```py
class Question(models.Model):
    question_text = models.CharField(max_length=200) #질문
    pub_date = models.DateTimeField("date published") #발행일
```

- Model
  - 부가적인 메타데이터를 가진 DB의 구조
  - Field명(question_text, pub_date 등)을 컬럼명으로 사용한다.
    - Field명은 주로 기계가 읽기 좋은 형식으로 설정
      - ex. pub_date
    - But, 생성자의 첫 번째 parameter로 사람이 읽기 좋은 형식(설명하는 용도)을 설정할 수 있다.
      - ex. "date published"

## Model 반영

- Django는 모델을 가지고 다음을 생성한다.
  - DB 스키마
  - 각 모델의 객체에 접근하기 위한 API

```py
INSTALLED_APPS = [
    'polls.apps.PollsConfig', #polls 앱 관련 설정 추가
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

- `polls.apps.PollsConfig`
  - /polls/apps.py 내부에 있는 PollsConfig 클래스를 참조하라는 의미
- 이렇게 settings.py 파일에 설정을 추가해야, Django가 polls 라는 앱이 존재한다는 것을 알 수 있다.

```
py manage.py makemigrations polls

//결과
Migrations for 'polls':
  polls\migrations\0001_initial.py
    - Create model Question
    - Create model Choice
```

- migration
  - Django가 model의 변경사항을 Disk에 저장하는 방법
- 따라서 위 명령어는 우리가 수행한 model의 생성/변경을 migration으로 저장하고 싶다는 것!

- `makemigrations`를 통해 migration들을 만들어 놓고,
  - 약간의 commit 개념과 비슷
- `migrate` 명령어로 변경사항을 DB에 적용

## Python shell 실행

```
py manage.py shell
```

##

```shell
>>> from polls.models import Choice, Question #model 가져오기
>>> Question.objects.all()
<QuerySet []>
>>> from django.utils import timezone
>>> q = Question(question_text="질문을 적자!", pub_date=timezone.now()) #새로운 Question 인스턴스 생성
>>> q.save() #q 저장
>>> q.id
1
>>> q.question_text #q의 컬럼 별 내용 확인
'질문을 적자!'
>>> q.pub_date
datetime.datetime(2024, 5, 3, 8, 45, 38, 170840, tzinfo=datetime.timezone.utc)
>>> q.qeustion_text = "질문 변경해볼게" #q의 question_text 변경
>>> q.question_text #save 하기 전까지는 반영 x
'질문을 적자!'
>>> q.save() #save()를 명시적으로 호출해야 DB에 저장된다.
>>> q.qeustion_text #value가 바뀐 것을 확인 가능
'질문 변경해볼게'
>>>
```

## 관리자 생성

```
py manage.py createsuperuser
```

- username, email, password 입력 후 유저 생성 완료

## 관리 사이트에 model 등록

```py
#polls/admin.py
from django.contrib import admin

from .models import Question

admin.site.register(Question)
```

### 등록 결과

![image](https://github.com/naya-h2/Django-Study/assets/103186362/a7c506fe-99ec-4292-81d9-893c52f1b303)

- 각 속성값 변경 가능
  ![image](https://github.com/naya-h2/Django-Study/assets/103186362/126ce35f-e789-4c1b-a66e-6d19d13d961f)

- History 탭에서 변경 history 확인 가능
  - username
  - timestamp
