import json
import os

from openai import OpenAI
from test_generator.models import Test, Question, Answer, SINGLE, MULTIPLE, TEXT
from django.core.exceptions import ValidationError
from django.db import transaction


TYPE_MAPPING = {
    "single": SINGLE,
    "multiple": MULTIPLE,
    "open": TEXT,
}


def response_to_llm(questions_count, prompt):
    client = OpenAI(
        api_key=os.getenv('AI_API_KEY'),
        base_url="https://api.proxyapi.ru/openai/v1",
    )

    system_settings = (
        "Ты помощник, который помогает создавать тесты по различным темам."
        "Тебе приходит какой-то промпт (описание), а ты должен по этим входным данным (теме) придумать тест"
        "Включи в тест следующие типы вопросов: "
        "1. Вопросы с выбором одного ответа из нескольких. "
        "2. Вопросы с выбором нескольких ответов. "
        "3. Вопросы с вводом ответа. "
        f"Всего должно быть {questions_count} вопросов"
        "Формат ответа только в JSON: {'title': 'название теста', 'questions': [{'type': 'single/multiple/open', 'question': "
        "'текст вопроса', 'options': ['вариант1', 'вариант2'], 'correct_answers': ['правильный ответ']}]}. "
        "В JSON-ответе используй двойные кавычки. Если в промпте содержится непонятный текст, нет темы или мало данных верни пустой JSON "
    )

    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_settings},
            {"role": "user", "content": f'Сделай тест по этой теме: {prompt}'}
        ],
    )

    try:
        test_json = json.loads(chat_completion.choices[0].message.content)
        return test_json
    except json.JSONDecodeError as e:
        print("Ошибка при парсинге JSON:", e)
        print("Ответ модели:", chat_completion.choices[0].message.content)
        return {}


def add_test_data(data):
    with transaction.atomic():
        # Создание объекта Test
        test = Test.objects.create(name=data['title'])

        # Обработка вопросов
        for question_data in data['questions']:
            question_type = TYPE_MAPPING.get(question_data['type'])
            if question_type is None:
                raise ValidationError(f"Unknown question type: {question_data['type']}")

            question = Question.objects.create(
                name=question_data['question'],
                test=test,
                type=question_type
            )

            # Обработка ответов (вариантов ответов)
            if 'options' in question_data:
                for option in question_data['options']:
                    is_correct = option in question_data['correct_answers']
                    Answer.objects.create(
                        value=option,
                        is_correct=is_correct,
                        question=question,
                        type=question_type
                    )

            # Если вопрос типа "open" (текстовый ответ), добавляем правильный ответ как Answer
            if question_type == TEXT and 'correct_answers' in question_data:
                for correct_answer in question_data['correct_answers']:
                    Answer.objects.create(
                        value=correct_answer,
                        is_correct=True,
                        question=question,
                        type=question_type
                    )

        return test
