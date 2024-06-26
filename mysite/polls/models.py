import datetime
from django.db import models
from django.utils import timezone

class Question(models.Model): #모델1
    question_text = models.CharField(max_length=200) #질문
    pub_date = models.DateTimeField("date published") #발행일
    def __str__(self): #객체의 표현을 편하게 보기 위해
        return self.question_text
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model): #모델2
    question = models.ForeignKey(Question, on_delete=models.CASCADE) #ForeignKey를 이용해 관계 설정
    choice_text = models.CharField(max_length=200) #CharField에서는 max_length 설정 필수
    votes = models.IntegerField(default=0) #선택적으로 default값 설정 가능
    def __str__(self):
        return self.choice_text