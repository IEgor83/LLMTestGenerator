from django import forms


class TextInputForm(forms.Form):
    text = forms.CharField(label='Введите запрос', max_length=100)
    questions = forms.IntegerField(label='Количество вопросов', min_value=0, max_value=15)
