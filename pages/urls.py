from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('detail/<int:pk>/', views.QuestionDetailView.as_view(), name='question_detail'),
    path('comment-add/<int:pk>', views.CreateCommentView.as_view(), name='create_comment'),
    path('ask-question/', views.AskedQuestionFormView.as_view(), name='form_page'),
    path('answer-question/<int:pk>', views.AnswerQuestionFormView.as_view(), name='answer_question'),
    path('tags', views.TagView.as_view(), name='tags'),
    path('tag_detail/<str:name>', views.TagView.as_view(), name='tag_detail'),
    path('question-vote-ajax/<int:question_id>', views.QuestionVoteAjaxView.as_view(), name='question_vote_ajax'),
    path('answer-vote-ajax/<int:answer_id>', views.AnswerVoteAjaxView.as_view(), name='answer_vote_ajax'),
    path('delete-item/<str:item_type>/<int:pk>', views.DeleteItemView, name="delete_item"),
    path('timeline/<int:pk>', views.TimelineView.as_view(), name='timeline'),
    path('user-profile/<str:username>', views.UsersProfileView.as_view(), name='user_profile'),
    path('user-profile-activity/<str:username>', views.UsersProfileActivityView.as_view(), name='user_profile_activity'),
    path('user-profile-answers/<str:username>', views.UsersProfileAnswersView.as_view(), name='user_profile_answers'),
    path('user-profile-questions/<str:username>', views.UsersProfileQuestionsView.as_view(), name='user_profile_questions'),
    path('user-profile-tags/<str:username>', views.UsersProfileTagsView.as_view(), name='user_profile_tags'),
    path('get-report', views.GetReportView.as_view(), name='get_report'),
]
