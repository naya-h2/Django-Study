# Create your views here.
from django.http import HttpResponse, Http404
from django.template import loader
from django.shortcuts import render

from .models import Question #model 불러오기

def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    template = loader.get_template("polls/index.html") #templates 폴더에서 해당 파일(템플릿)을 찾는다.
    context = {
        "latest_question_list": latest_question_list,
    }
    return HttpResponse(template.render(context, request)) #template에 context를 전달하고, 해당 화면 렌더링

def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id) #question_id에 맞는 Question 인스턴스 찾기
    except Question.DoesNotExist: #존재하지 않는 경우에
        raise Http404("Question does not exist") #404 에러 던지기
    return render(request, "polls/detail.html", {"question": question})

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)