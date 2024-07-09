from django.shortcuts import render
from django.views.generic.base import TemplateView

from .models import TYPES
from .services import response_to_llm, add_test_data

from test_generator.forms import TextInputForm


class TestGeneratorView(TemplateView):
    template_name = 'test_generate.html'

    def get(self, request, *args, **kwargs):
        form = TextInputForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = TextInputForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            questions = form.cleaned_data['questions']
            test_json = response_to_llm(questions, text)

            status = "Не удалось создать тест, проверьте запрос или попробуйте позже"
            test = None
            types = {label: value for value, label in TYPES}

            if test_json:
                try:
                    test = add_test_data(test_json)
                    status = 'ОК'
                except Exception as e:
                    status = e

            context = {
                'form': form,
                'text': text,
                'questions': questions,
                'status': status,
                'test': test,
                'types': types
            }
            return render(request, self.template_name, context)
        return render(request, self.template_name, {'form': form})
