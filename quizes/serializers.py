from rest_framework import serializers
from .models import Quiz, Choice, Question


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ["id", "title", "description", "created_at"]


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ["id", "text", "is_correct"]


class QuestionDetailSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ["id", "text", "choices"]


class QuizDetailSerializer(serializers.ModelSerializer):
    questions = QuestionDetailSerializer(many=True, read_only=True)
    questions_count = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = [
            "id",
            "title",
            "description",
            "created_at",
            "questions",
            "questions_count",
        ]

    def get_questions_count(self, obj):
        return obj.questions.count()


class AnswerSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    choice_id = serializers.IntegerField()
