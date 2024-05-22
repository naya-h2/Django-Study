# WEEK6

📆 24/05/22

🔗 [Writing your first Django app, part 7](https://docs.djangoproject.com/en/5.0/intro/tutorial07/)

🔗 [Writing your first Django app, part 8](https://docs.djangoproject.com/en/5.0/intro/tutorial08/)

## 관리자 form 커스텀하기

```py
class QuestionAdmin(admin.ModelAdmin):
    fields = ["pub_date", "question_text"] #pub_date가 question_text보다 먼저 오도록 순서 설정
```

- 모델의 관리자 옵션을 변경하고자 한다면, `admin.site.register()`에 두 번째 인수로 전달하면 된다.
- field가 많아질수록 순서를 잘 관리하는 게 중요하다.

![결과이미지](https://docs.djangoproject.com/ko/5.0/_images/admin07.png)

## 폼을 fieldset으로 나눠서 관리

```py
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}), #각 튜플의 첫 번째 요소는 fieldset의 제목
        ("Date information", {"fields": ["pub_date"]}),
    ]

admin.site.register(Question, QuestionAdmin)
```

![결과이미지](https://docs.djangoproject.com/ko/5.0/_images/admin08t.png)

## Choice도 관리자 페이지에서 관리할 수 있게 하기

```py
#polls/admin.py에 추가
admin.site.register(Choice) #Choice도 관리자 페이지에 등록
```

## Question 객체 생성할 때 Choice 객체도 한 번에 추가할 수 있게 하기

```py
class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3 #기본적으로 choice 추가할 수 있는 3개 제공

```

- Question 객체의 fieldset 밑에 Choice 추가할 수 있는 form 추가

```py
class ChoiceInline(admin.TabularInline): ...
```

- 위의 코드로 바꾸면 Choice 객체가 1줄로 나타나게 UI를 바꿀 수 있음.
- 화면 공간 절약 가능!

## pub_date를 이용해 필터링 기능 추가

```py
#polls/models.py
@admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )

#polls/admin.py에 추가
list_filter = ["pub_date"]
```

## 검색 기능 추가

```py
#polls/admin.py에 추가
search_fields = ["question_text"]
```
