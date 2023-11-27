from django import forms
from .models import answer, question, comment, Tags, QuesComment
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class questionForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'style':'width: 49rem; border: 1px solid black;'}),label='Başlık:')
    context = forms.CharField(widget=CKEditorUploadingWidget(attrs={'class': 'form-control', 'style':'width: 100%; border: 1px solid black;'}), label='Soru Detayı:')
    tags = forms.ModelMultipleChoiceField(queryset=Tags.objects.all(), widget=forms.SelectMultiple(attrs={'class': 'selectpicker form-control', 'data-live-search': 'true', 'data-title': 'lütfen etiket seçiniz...'}), label='Etiketler:')

    class Meta:
        model = question
        fields = ['title', 'context', 'tags']


class answerForm(forms.ModelForm):
    answer = forms.CharField(widget=CKEditorUploadingWidget(attrs={'class': 'form-control', 'style':'width: 60rem; border: 1px solid black;'}), label='Cevabınız ')
    class Meta:
        model = answer
        fields = ('answer',)



class commentForm(forms.ModelForm):
    comment = forms.CharField(widget=CKEditorWidget(attrs={'class': 'form-control', 'style':'width: 60rem; border: 1px solid black;'}), label='Yorum ekle:')
    class Meta:
        model = comment
        fields = ('comment', )



class QuesCommentForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'style': 'border: 1px solid black;'}), label='Yorum :')
    class Meta:
        model = QuesComment
        fields = ('comment',)



