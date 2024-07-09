import uuid

from django.db import models
from django.db.models import SET_NULL
from django_softdelete.models import SoftDeleteModel


class Test(SoftDeleteModel):
    name = models.CharField(max_length=1500)
    description = models.CharField(max_length=1000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    random_order = models.BooleanField(null=True, default=False)
    isActive = models.BooleanField(default=True)
    public = models.BooleanField(default=False)
    hash = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, null=True)
    interpretation_type = models.CharField(null=True, max_length=100)

    def __str__(self) -> str:
        return f'{self.name}'


SINGLE, MULTIPLE, TEXT, MATCHING, SEQUENCE, PARAGRAPH, SYSTEM = range(7)
TYPES = (
    (SINGLE, "Single"),
    (MULTIPLE, "Multiple"),
    (TEXT, "Text"),
    (MATCHING, "Matching"),
    (SEQUENCE, "Sequence"),
    (PARAGRAPH, "Paragraph"),
    (SYSTEM, "System"),
)


class QuestionType(SoftDeleteModel):
    type = models.IntegerField(choices=TYPES, default=SINGLE)


class Question(SoftDeleteModel):
    name = models.CharField(max_length=1500)
    description = models.CharField(max_length=500, blank=True, null=True)
    explanation = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    test = models.ForeignKey(Test, on_delete=SET_NULL, null=True, related_name='questions')
    type = models.IntegerField(choices=TYPES, default=SINGLE)
    points = models.PositiveIntegerField(default=1)
    is_required = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'[Type: {TYPES[self.type][1]}] {self.name}'


class Answer(SoftDeleteModel):
    value = models.CharField(max_length=512, null=True)
    is_correct = models.BooleanField(default=False)
    point_value = models.FloatField(default=0)
    question = models.ForeignKey(Question, on_delete=SET_NULL, null=True, related_name='answers')
    type = models.IntegerField(choices=TYPES, default=SINGLE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self) -> str:
        return f'[ID: {self.pk}] [{TYPES[self.type][1]}] [{self.question}] [{self.is_correct}] {self.value}'
