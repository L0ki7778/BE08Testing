from rest_framework import viewsets, generics, permissions # type:ignore
from forum_app.models import Like, Question, Answer
from typing import Any
from .serializers import QuestionSerializer, AnswerSerializer, LikeSerializer
from .permissions import IsOwnerOrAdmin, CustomQuestionPermission
from .throttling import QuestionGetThrottle,QuestionPostThrottle

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [CustomQuestionPermission]
    throttle_classes = [QuestionGetThrottle]

    def perform_create(self, serializer:QuestionSerializer):
        serializer.save(author=self.request.user) # type: ignore
        
    def get_throttles(self)->list[Any]:
        if self.action == 'list' or self.action == 'retrieve':
            return [QuestionGetThrottle()]
        if self.action == 'create' or self.action =='put':
            return [QuestionPostThrottle()]
        return []

class AnswerListCreateView(generics.ListCreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer: AnswerSerializer):
        serializer.save(author=self.request.user) # type: ignore
        
    def get_queryset(self):
        queryset =  Answer.objects.all()
        content_param = self.request.query_params.get('content',None)
        
        if content_param is not None:
            queryset =queryset.filter(content__icontains=content_param)
            
        author_param = self.request.query_params.get('author',None)
        if author_param is not None:
            queryset= queryset.filter(author__username=author_param)
            
        return queryset

class AnswerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsOwnerOrAdmin]


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsOwnerOrAdmin]

    def perform_create(self, serializer:LikeSerializer):
        serializer.save(user=self.request.user) # type: ignore
