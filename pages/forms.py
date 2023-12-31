from django import forms
from .models import Answers, Questions, AnswerComments, Tags, QuestionComments
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib.auth.models import User


class questionForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'style':'width: 49rem; border: 1px solid black;'}),label='Başlık:')
    context = forms.CharField(widget=CKEditorUploadingWidget(attrs={'class': 'form-control', 'style':'width: 100%; border: 1px solid black;'}), label='Soru Detayı:')
    tags = forms.ModelMultipleChoiceField(queryset=Tags.objects.all(), widget=forms.SelectMultiple(attrs={'class': 'selectpicker form-control', 'data-live-search': 'true', 'data-title': 'lütfen etiket seçiniz...'}), label='Etiketler:')

    class Meta:
        model = Questions
        fields = ['title', 'context', 'tags']


class answerForm(forms.ModelForm):
    answer = forms.CharField(widget=CKEditorUploadingWidget(attrs={'class': 'form-control', 'style':'width: 60rem; border: 1px solid black;'}), label='Cevabınız ')
    class Meta:
        model = Answers
        fields = ('answer',)



class commentForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={'size': '10', 
                                                           'class': 'form-control',
                                                           'style':'border: 1px solid rgb(190, 190, 190); position: relative; left: 3rem; width: 45rem; height: 8rem; z-index: 3;', 'id': 'ansCommentId'}), label='Yorum ekle:')
    class Meta:
        model = AnswerComments
        fields = ('comment', )



class QuesCommentForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={'size': '10',
                                                           'class': 'form-control', 
                                                           'style': 'border: 1px solid rgb(190, 190, 190); position: absolute; top: 31rem; left: 36rem; width: 45rem; height: 8rem; z-index: 3;', 'id': 'queCommentId'}), label='Yorum :')
    class Meta:
        model = QuestionComments
        fields = ('comment', )




