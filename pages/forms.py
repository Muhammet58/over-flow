from django import forms
from .models import Answers, Questions, AnswerComments, Tags, QuestionComments
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib.auth.models import User


class questionForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 49rem; border: 1px solid black;'}), label='Başlık:')
    context = forms.CharField(widget=CKEditorUploadingWidget(attrs={'class': 'form-control', 'style': 'width: 100%; border: 1px solid black;'}), label='Soru Detayı:')
    tags = forms.ModelMultipleChoiceField(queryset=Tags.objects.all(), widget=forms.SelectMultiple(attrs={'class': 'selectpicker form-control', 'data-live-search': 'true', 'data-title': 'lütfen etiket seçiniz...'}), label='Etiketler:')

    class Meta:
        model = Questions
        fields = ['title', 'context', 'tags']

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(questionForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        question = super(questionForm, self).save(commit=False)
        question.user = self.user
        if commit:
            question.save()
        return question
    


class answerForm(forms.ModelForm):
    answer = forms.CharField(widget=CKEditorUploadingWidget(attrs={'class': 'form-control', 'style': 'width: 60rem; border: 1px solid black;'}), label='Cevabınız ')
    class Meta:
        model = Answers
        fields = ('answer',)

    def __init__(self, user=None, question=None, *args, **kwargs):
        self.user = user
        self.question = question
        super(answerForm, self).__init__(*args, **kwargs)
    
    def save(self, commit=True):
        answer = super(answerForm, self).save(commit=False)
        answer.user = self.user
        answer.answer_to_the_question = self.question
        if commit:
            answer.save()
        return answer
    



class AnswerCommentForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={'size': '10',
                                                           'class': 'form-control',
                                                           'style': 'border: 1px solid rgb(190, 190, 190); position: relative; left: 3rem; width: 45rem; height: 8rem; z-index: 3;', 'id': 'answerCommentField'}), label='Yorum ekle:')
    class Meta:
        model = AnswerComments
        fields = ('comment', )


    def __init__(self, comment=None, user=None, *args, **kwargs):
        super(AnswerCommentForm, self).__init__(*args, **kwargs)
        self.comment = comment
        self.user = user

    def save(self, commit=True):
        comment = super(AnswerCommentForm, self).save(commit=False)
        comment.comment_answer = self.comment
        comment.comment_user = self.user
        if commit:
            comment.save()
        return comment



class QuestionCommentForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={'size': '10',
                                                           'class': 'form-control',
                                                           'style': 'border: 1px solid rgb(190, 190, 190); position: absolute; top: 31rem; left: 36rem; width: 45rem; height: 8rem; z-index: 3;', 'id': 'questionCommentField'}), label='Yorum :', initial="1234567890")
    class Meta:
        model = QuestionComments
        fields = ('comment', )


    def __init__(self, comment=None, user=None, *args, **kwargs):
        super(QuestionCommentForm, self).__init__(*args, **kwargs)
        self.comment = comment
        self.user = user

    def save(self, commit=True):
        comment = super(QuestionCommentForm, self).save(commit=False)
        comment.comment_user = self.user
        comment.comment_question = self.comment
        if commit:
            comment.save()
        return comment
