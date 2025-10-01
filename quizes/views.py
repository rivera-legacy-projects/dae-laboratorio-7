from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Quiz, Question, Choice
from .serializers import QuizSerializer, QuizDetailSerializer, AnswerSerializer


class QuizViewSet(viewsets.ModelViewSet):

    queryset = Quiz.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return QuizDetailSerializer
        return QuizSerializer

    @action(detail=True, methods=["post"])
    def validate(self, request, pk=None):
        quiz = self.get_object()

        serializer = AnswerSerializer(data=request.data.get("answers", []), many=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        answers = serializer.validated_data
        results = []

        for answer in answers:
            question_id = answer["question_id"]
            choice_id = answer["choice_id"]

            try:
                question = Question.objects.get(id=question_id, quiz=quiz)
                choice = Choice.objects.get(id=choice_id, question=question)

                results.append(
                    {
                        "question_id": question_id,
                        "choice_id": choice_id,
                        "correct": choice.is_correct,
                        "question_text": question.text,
                        "choice_text": choice.text,
                    }
                )
            except (Question.DoesNotExist, Choice.DoesNotExist):
                results.append(
                    {
                        "question_id": question_id,
                        "error": "Question or choice not found ❌",
                    }
                )

        correct_answers = sum(1 for r in results if r.get("correct", False))
        total_answers = len(results)
        percentage = (
            int((correct_answers / total_answers) * 100) if total_answers else 0
        )

        return Response(
            {
                "quiz_id": quiz.id,
                "quiz_title": quiz.title,
                "score": f"{correct_answers}/{total_answers}",
                "percentage": percentage,
                "grade": "🏆"
                if percentage >= 80
                else "👍"
                if percentage >= 60
                else "📚",
                "results": results,
            }
        )
