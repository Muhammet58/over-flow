from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import Tags, comment, question, answer, saved, QuesComment
from .forms import answerForm, questionForm, commentForm,QuesCommentForm
from django.db.models import Count
from  django.db.models import Q


def index(request):
    filter_query = request.POST.get('search')
    data = {}

    if filter_query and filter_query != '':
        questions = question.objects.filter(Q(title__icontains=filter_query) | Q(context__icontains=filter_query)).order_by('-published_date').annotate(ann_answer=Count('answer')).values()
    else:
        questions = question.objects.all().order_by('-published_date').annotate(ann_answer=Count('answer')).values()

    for q in questions:
        q['tag_names'] = question.objects.get(id=q['id']).tags.values_list('name', flat=True)

    question_count = questions.count()
    data['questions'] = questions
    data['question_count'] = question_count

    return render(request, 'pages/index.html', data)


def question_detail(request, pk):
    obje = question.objects.get(id=pk)
    questions = get_object_or_404(question, id=pk)
    saved_que = saved.objects.filter(user=request.user.id).values_list('que__id', flat=True)

    session_key = f'{pk}_{request.user.id}' if request.user.is_authenticated else f'{pk}'

    if request.session.get(session_key, False):
        pass
    else:
        obje.increment_view_count()
        obje.save()
        request.session[session_key] = True
                                    
    question_answers = answer.objects.filter(answerToTheQuestion__id=pk).order_by('-published_date')
    question_comments = QuesComment.objects.filter(commentQues__id=pk).order_by('-PubDate')
    answer_count = question_answers.count()

    form = answerForm()
    return render(request, 'pages/detail.html', {'item': questions, 'answer': question_answers,
                                                  'saved_que': saved_que, 'answer_count': answer_count,
                                                  'question_comments': question_comments,
                                                  'form': form
                                                  })



def formPage(request):
    if request.method == 'POST':
        form = questionForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            form.save_m2m()

            return redirect('index')
        
    else:
        form = questionForm()
    return render(request, 'forms/forms.html', {'form': form})



def answer_question(request, pk):
    obje = question.objects.get(id=pk)
    if request.method == 'POST':
        form = answerForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.answerToTheQuestion = obje 
            item.save()
            return redirect('questionDetail', pk=pk)
    else:
        form = answerForm()
    return render(request, 'forms/answer_forms.html', {'form': form})




def update(request, pk):
    data = get_object_or_404(answer, id=pk)

    if request.method == 'POST':
        form = answerForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            related_question_pk = data.answerToTheQuestion.pk
            return redirect('questionDetail', pk=related_question_pk)
    
    form = answerForm(instance=data)
    return render(request, 'forms/answer_forms.html', {'form': form})
    

def my_saved(request):
    mySaved = saved.objects.filter(user=request.user.id).select_related('que')
    mySaved_answer_count = mySaved.annotate(answer_count=Count('que__answer'))
    return render(request, 'pages/saved.html', {'mySaved': mySaved_answer_count})



def save(request, pk):
    que = get_object_or_404(question, id=pk)
    save, created = saved.objects.get_or_create(user=request.user, que=que)

    if not created:
        save.delete()
    return redirect('questionDetail', pk=pk)



def delete_save(request, pk):
    que = get_object_or_404(question, id=pk)
    save, created = saved.objects.get_or_create(user=request.user, que=que)

    if not created:
        save.delete()
    return redirect('saved')



def comment_form(request, pk):
    this_answer = get_object_or_404(answer, id=pk)
    if request.method == "POST":
        form = commentForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.comment_answer = this_answer
            item.comments_user = request.user
            item.save()
            return redirect('questionDetail', pk=this_answer.answerToTheQuestion.id)
    form = commentForm()
    return render(request, 'forms/comment_form.html', {'form': form})



def comment_details(request, pk):
    answer_details = get_object_or_404(answer, id=pk)
    comments = comment.objects.filter(comment_answer=answer_details).order_by('-published_date')
    comment_count = comments.count()
    return render(request, 'pages/comments.html', {'answer': answer_details, 'comments': comments, 'comment_count' : comment_count})



def tags(request):
    data = {}
    data['tags'] = Tags.objects.all()

    if request.method == "POST":
        search = request.POST.get('Search')
        data['tags'] = Tags.objects.filter(name__icontains=search)
        if not data['tags']:
            data['error'] = 'Aramaya göre içerik bulunmamaktadır'
        
    return render(request, 'pages/tags.html', data)



def tagDetailView(request, name):
    data = {}

    queryset = question.objects.filter(tags__name=name)

    tags_of_question = Tags.objects.filter(name=name)
    data['tags_name'] = tags_of_question.first().name if tags_of_question.exists() else None
    data['tags_content'] = tags_of_question.first().content if tags_of_question.exists() else None

    data['queryset'] = queryset
    data['queryset_count'] = queryset.count()
    return render(request, 'pages/tags.html', data)



def ques_comment_form(request, pk):
    obje = get_object_or_404(question, id=pk)
    if request.method == 'POST':
        form = QuesCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.commentQues = obje
            comment.commentUser = request.user
            comment.save()
            return redirect('questionDetail', pk=pk)
    form = QuesCommentForm()
    return render(request, 'pages/quesCommentForm.html', {'form' :form})


def increase(request, question_id):
    to_increase = get_object_or_404(question, id=question_id)
    to_increase.user_vote(request.user, 1)

    return JsonResponse({"increase_vote": to_increase.votes})

def decrease(request, question_id):
    to_decrease = get_object_or_404(question, id=question_id)
    to_decrease.user_vote(request.user, -1)

    return JsonResponse({"decrease_vote": to_decrease.votes})





def answer_vote_increase(request, answer_id):
    to_increase = get_object_or_404(answer, id=answer_id)
    to_increase.user_answer_vote(request.user, 1)

    return JsonResponse({"increase_vote": to_increase.votes})

def answer_vote_decrease(request, answer_id):
    to_decrease = get_object_or_404(answer, id=answer_id)
    to_decrease.user_answer_vote(request.user, -1)

    return JsonResponse({"decrease_vote": to_decrease.votes})