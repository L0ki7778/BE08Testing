from rest_framework import serializers
from forum_app.models import Like, Answer, Question

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'content', 'author', 'created_at']

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'question', 'created_at']
        read_only_fields = ['user']

    def validate(self, data):
        user = self.context['request'].user
        question = data['question']

        if Like.objects.filter(user=user, question=question).exists():
            raise serializers.ValidationError("You have already liked this question.")

        return data
    
class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'title', 'content', 'author', 'created_at', 'answers', 'likes']