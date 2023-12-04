from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<int:pk>/', views.question_detail, name='questionDetail'),
    path('ask-question/', views.formPage, name='formPage'),
    path('answer-question/<int:pk>', views.answer_question, name='answer_question'),
    path('update/<int:pk>', views.update, name='update'),
    path('comment/<int:pk>', views.comment_form, name='comment_form'),
    path('tags', views.tags, name='tags'),
    path('tag_detail/<str:name>', views.tagDetailView, name='tag_detail'),
    path('ques-comment-form/<int:pk>', views.ques_comment_form, name='quesCommentForm'),
    path('increase/<int:question_id>', views.increase, name='increase'),
    path('decrease/<int:question_id>', views.decrease, name='decrease'),
    path('answer-vote-increase/<int:answer_id>', views.answer_vote_increase, name='answer_vote_increase'),
    path('answer-vote-decrease/<int:answer_id>', views.answer_vote_decrease, name='answer_vote_decrease'),
    path('question-delete/<int:pk>', views.que_delete, name='question_delete'),
    path('answer-delete/<int:pk>', views.ans_delete, name='answer_delete'),
    path('que-comments-delete/<int:pk>', views.queCommentDelete, name='question_comments_delete'),
    path('ans-comments-delete/<int:pk>', views.ansCommentDelete, name='answer_comments_delete'),
    path('timeline/<int:pk>', views.timeline, name='timeline')
]
