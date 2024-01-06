from datetime import datetime
from typing import Any
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, FormView, View
from .tasks import GenerateReport
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import Tags, AnswerComments, Questions, Answers, QuestionComments, Vote, Save
from .forms import answerForm, questionForm, AnswerCommentForm, QuestionCommentForm
from django.db.models import Count
from django.contrib import messages
from django.db.models import Q
from account.models import UserProfile
import locale

locale.setlocale(locale.LC_ALL, 'tr')

class IndexView(ListView):
    model = Questions
    template_name = "pages/index.html"
    context_object_name = 'questions'
    paginate_by = 10

    def get_queryset(self):
        filter_query = self.request.POST.get('search')
        if filter_query and filter_query != '':
            queryset = self.model.objects.filter(Q(title__icontains=filter_query) | Q(context__icontains=f"[{filter_query}]")).order_by('-published_date').annotate(
                ann_answer=Count('answers')).select_related('user').prefetch_related('tags')

            if '[' in filter_query:
                filter_query = filter_query.split('[')[1].split(']')[0]
                queryset = self.model.objects.filter(tags__name__icontains=filter_query)

            if 'kullanıcı:' in filter_query:
                filter_query = filter_query.split(':')[1]
                queryset = self.model.objects.filter(user__username__icontains=filter_query)
        else:
            queryset = self.model.objects.all().order_by('-published_date').annotate(ann_answer=Count('answers')).select_related('user').prefetch_related('tags')

        return queryset

    def post(self, request, **kwargs):
        context = {
            "questions": self.get_queryset(),
            "question_count": self.get_queryset().count()
        }
        return render(request, 'pages/index.html', context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question_count'] = self.get_queryset().count()
        context['tags'] = Tags.objects.all()
        return context



class QuestionDetailView(DetailView):
    model = Questions
    template_name = "pages/detail.html"

    def get_object(self, **kwargs):
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(Questions, id=pk)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()


        user_id = self.request.user.id
        session_key = f'{obj.id}{user_id}'
        if not self.request.session.get(session_key, False):
            obj.incrementViewCount()
            obj.save()
            self.request.session[session_key] = True


        saved_questions = Save.objects.filter(user=self.request.user.id).select_related('user').values_list('questions__id', flat=True)
        question_answers = Answers.objects.filter(answer_to_the_question=obj).order_by('-vote').select_related('answer_to_the_question', 'user')
        question_comments = QuestionComments.objects.filter(comment_question=obj).order_by('-published_date').select_related('comment_question', 'comment_user')
        tags = obj.tags.all()


        connect = self.model.objects.filter(~Q(id=obj.id) & Q(title__icontains=obj.title))
        related = self.model.objects.filter(tags__in=obj.tags.all()).exclude(id=obj.id)

        question_comment_form = QuestionCommentForm()
        answer_comment_form = AnswerCommentForm()
        form = answerForm()

        context['question'] = obj
        context['answers'] = question_answers
        context['saved_que'] = saved_questions
        context['question_comments'] = question_comments
        context['answer_count'] = question_answers.count()
        context['tags'] = tags
        context['connected'] = connect
        context['related'] = related
        context['queCommentForm'] = question_comment_form
        context['ansCommentForm'] = answer_comment_form
        context['form'] = form

        return context



class CreateCommentView(FormView):
    def get_form_class(self):
        comment_type = self.request.POST.get('comment_type')
        form_class = QuestionCommentForm if comment_type == 'questionComment' else AnswerCommentForm
        return form_class
    def get_object(self):
        pk = self.kwargs.get('pk')
        comment_type = self.request.POST.get('comment_type')
        model_object = get_object_or_404(Questions, id=pk) if comment_type == 'questionComment' else get_object_or_404(Answers, id=pk)
        return model_object
    def post(self, request, *args, **kwargs):
        this_object = self.get_object()
        form_class = self.get_form_class()
        form = form_class(data=request.POST, comment=this_object, user=request.user)

        if form.is_valid():
            comment = form.save()
            return self.get_success_response(comment)

    def get_success_response(self, item):
        response = {
            'status': 'success',
            'comment': item.comment,
            'commentUser': item.comment_user.username,
            'commentId': item.id,
            'commentDate': item.published_date.astimezone().strftime('%d %B %Y %H:%M'),
        }
        return JsonResponse(response)



class AskedQuestionFormView(FormView):
    template_name = 'forms/forms.html'
    form_class = questionForm
    success_url = '/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        item = form.save()
        form.save_m2m()
        return super().form_valid(item)



class AnswerQuestionFormView(FormView):
    form_class = answerForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['question'] = self.get_object()
        return kwargs

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy("question_detail", kwargs={"pk": pk})   
    
    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Questions, id=pk)
    
    def form_valid(self, form):
        item = form.save()
        return super().form_valid(item)



class TagView(ListView):
    template_name = "pages/tags.html"
    model = Tags
    context_object_name = "tags"
    paginate_by = 8

    def get_queryset(self):
        queryset = Tags.objects.annotate(question_count=Count('questions')).order_by('-question_count').values('name', 'content', 'question_count')
        return queryset

    def get(self, request, *args, **kwargs):
        search = request.GET.get('Search')
        if search:
            tags = Tags.objects.filter(name__icontains=search).annotate(question_count=Count('questions')).values('name', 'content', 'question_count')
            if not tags.exists():
                return render(request, self.template_name, {'error': 'Aramaya göre içerik bulunmamaktadır'})
            return render(request, self.template_name, {'tags': tags})

        name = kwargs.get("name")
        if name:
            tag = get_object_or_404(Tags, name=name)
            queryset = Questions.objects.filter(tags__name=tag.name).annotate(ann_answer=Count('answers')).values('id', 'ann_answer', 'title', 'view', 'published_date', 'user__username')

            context = {
                'queryset': queryset,
                'queryset_count': queryset.count(),
                'tags_name': tag.name,
                'tags_content': tag.content,
            }
            return render(request, self.template_name, context)
        return super().get(request, *args, **kwargs)




class QuestionVoteAjaxView(View):
    def get(self, request, question_id, **kwargs):
        vote_type = request.GET.get('vote_type')
        data = {}
        question = get_object_or_404(Questions, id=question_id)
        value = 1 if vote_type == 'increase' else -1
        question.userVote(request.user, value)
        data["vote_count"] = question.vote

        return JsonResponse(data)



class AnswerVoteAjaxView(View):
    def get(self, request, answer_id, **kwargs):
        vote_type = request.GET.get('vote_type')
        data = {}
        question = get_object_or_404(Answers, id=answer_id)
        value = 1 if vote_type == 'increase' else -1
        question.userAnswerVote(request.user, value)
        data["vote_count"] = question.vote

        return JsonResponse(data)




def DeleteItemView(request, item_type, pk):
    models = {
        'question': Questions,
        'answer': Answers,
        'question_comment': QuestionComments,
        'answer_comment': AnswerComments,
    }

    model = models.get(item_type)
    item = get_object_or_404(model, id=pk)
    item.delete()

    if item_type in ['question', 'answer']:
        redirect_url = reverse('index')
        if item_type == 'answer':
            redirect_url = reverse('question_detail', kwargs={'pk': item.answer_to_the_question.id})
        return redirect(redirect_url)
    else:
        return JsonResponse({'message': 'success'})



class TimelineView(ListView):
    model = Questions
    template_name = "pages/timeline.html"
    context_object_name = "question_timeline"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question_timeline = self.get_queryset().get(id=self.kwargs.get("pk"))

        answer_timeline = Answers.objects.filter(answer_to_the_question=question_timeline).select_related('answer_to_the_question', 'user')
        comment_timeline = QuestionComments.objects.filter(comment_question=question_timeline).select_related('comment_question', 'comment_user')
        vote_timeline = Vote.objects.filter(question_vote=question_timeline).select_related('question_vote', 'user')

        timeline = []
        for ans in answer_timeline:
            timeline.append({
                "date": ans.published_date,
                "activity_type": "Cevap",
                "user": ans.user,
                "comment": '',
            })
        for cmnt in comment_timeline:
            timeline.append({
                "date": cmnt.published_date,
                "activity_type": "Yorum",
                "user": cmnt.comment_user,
                "comment": cmnt.comment,
            })
        for vote in vote_timeline:
            timeline.append({
                "date": vote.published_date,
                "activity_type": "Oy",
                "user": vote.user,
                "comment": '',
            })

        timeline = sorted(timeline, key=lambda x: x['date'], reverse=True)

        context["timeline"] = timeline
        context["question_timeline"] = question_timeline
        context["activity_count"] = sum([answer_timeline.count(), comment_timeline.count(), vote_timeline.count()])

        return context



class UsersProfileView(ListView):
    model = UserProfile
    template_name = "pages/user-profile.html"
    context_object_name = "user_profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get("username")
        user_profile = self.get_queryset().get(user__username=username)

        answered_questions_count = Answers.objects.filter(user__username=username).select_related('user').count()
        user_question = Questions.objects.filter(user__username=username).select_related('user').order_by('-vote', '-view')
        tags = Tags.objects.filter(questions__in=user_question)
        used_tags = tags.annotate(question_count=Count('questions')).order_by('-question_count')

        context["user_profile"] = user_profile
        context["answered_questions_count"] = answered_questions_count
        context["asked_questions_count"] = user_question.count()
        context["user_question"] = user_question
        context["order_tags"] = used_tags

        return context



class UsersProfileActivityView(ListView):
    model = Questions
    template_name = 'pages/user_profile_activity.html'
    context_object_name = 'user_questions'

    def get_queryset(self):
        username = self.kwargs['username']
        user_questions = Questions.objects.filter(user__username=username).select_related('user').order_by('-vote')
        return user_questions

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get('username')
        user_profile = UserProfile.objects.select_related('user').get(user__username=username)
        user_answer = Answers.objects.filter(user__username=username).select_related('user').order_by('-vote')

        tags = Tags.objects.filter(questions__in=self.get_queryset())
        used_tags = tags.annotate(que_count=Count('questions')).order_by('-que_count')

        que_votes = sum(context['user_questions'].values_list('vote', flat=True))
        ans_votes = sum(user_answer.values_list('vote', flat=True))
        all_votes = que_votes + ans_votes

        context["user_question"] = self.get_queryset()
        context["user_profile"] = user_profile
        context["user_answer"] = user_answer
        context["order_tags"] = used_tags
        context["all_votes"] = all_votes
        context["que_votes"] = que_votes
        context["ans_votes"] = ans_votes

        return context



class UsersProfileAnswersView(ListView):
    model = UserProfile
    template_name = "pages/user_profile_answers.html"
    context_object_name = "user_profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get("username")
        user_profile = self.get_queryset().select_related('user').get(user__username=username)
        user_answer = Answers.objects.filter(user__username=username).select_related('answer_to_the_question').order_by('-vote').annotate(answered_questions_count=Count('id'))

        context["user_profile"] = user_profile
        context["user_answer"] = user_answer
        context["answered_questions_count"] = user_answer.count()

        return context



class UsersProfileQuestionsView(ListView):
    model = UserProfile
    template_name = "pages/user_profile_question.html"
    context_object_name = "user_profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get("username")
        user_profile = UserProfile.objects.select_related('user').get(user__username=username)
        user_question = Questions.objects.filter(user__username=username).select_related('user').prefetch_related('tags').order_by('-vote').annotate(ans_count=Count('answers'))

        context["user_profile"] = user_profile
        context["asked_questions"] = user_question
        context["asked_questions_count"] = user_question.count()

        return context



class UsersProfileTagsView(ListView):
    model = UserProfile
    template_name = "pages/user_profile_tags.html"
    context_object_name = "user_profile"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get("username")

        user_profile = UserProfile.objects.get(user__username=username)
        user_question = Questions.objects.filter(user__username=username).select_related('user').prefetch_related('tags')
        tags = Tags.objects.filter(questions__in=user_question)
        used_tags = tags.annotate(que_count=Count('questions')).order_by('-que_count')

        context["user_profile"] = user_profile
        context["tag_count"] = used_tags.count()
        context["order_tags"] = used_tags

        return context




class GetReportView(View):
    template_name = 'pages/get_report.html'
    http_method_names = ['get', 'post']

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        if request.method == 'POST':
            selected_date = request.POST.get('selected_date')

            if selected_date:
                que = Questions.objects.filter(user=request.user, published_date__date=selected_date).select_related('user')
                selected_datetime = datetime.strptime(selected_date, '%Y-%m-%d')
                GenerateReport.delay(user_id=request.user.id, selected_date=selected_datetime)
                if not que.exists():
                    messages.error(request, f"{selected_datetime.strftime('%d %B %Y')} tarihine ait soru bulunamadı !")
                else:
                    messages.success(request, f"{selected_datetime.strftime('%d %B %Y')} tarihine ait sorularınız e-posta adresinize gönderilmiştir.")
            else:
                GenerateReport.delay(user_id=request.user.id)
                messages.success(request, f"Sorularınız e-posta adresinize gönderilmiştir.")

        return render(request, self.template_name)
