# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.db.models import F

from .models import Question, Choice #model 불러오기

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
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"]) #POST 메소드에 제출된 "choice"의 value를 문자열로 return
    except (KeyError, Choice.DoesNotExist): #해당 question에 대해 제출된 choice가 없는 경우 -> KeyError 발생시킴
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html", #detail.html(/polls/1)로 다시 리다이렉트 => detail view를 다시 호출하는 것
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1 #vote 수를 1 증가시키고 얘를 id로 쓰는 셈
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,))) #"/polls/3/results/" 를 return => results view를 call