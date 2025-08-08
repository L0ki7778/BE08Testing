from rest_framework import viewsets, generics, permissions, filters, pagination  # type:ignore
from forum_app.models import Like, Question, Answer
from django_filters.rest_framework import DjangoFilterBackend # type:ignore
from typing import Any
from .serializers import QuestionSerializer, AnswerSerializer, LikeSerializer
from .permissions import IsOwnerOrAdmin, CustomQuestionPermission
from .throttling import QuestionGetThrottle, QuestionPostThrottle


from rest_framework.views import APIView # type:ignore
from rest_framework.response import Response # type:ignore
from rest_framework import status # type:ignore

from .serializers import FileUploadSerializer

class FileUploadView(APIView):
    def post(self, request, format=None):  # type:ignore 
        serializer = FileUploadSerializer(data=request.data)  # type:ignore
        if serializer.is_valid():
            serializer.save()  # type:ignore
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [CustomQuestionPermission]
    throttle_classes = [QuestionGetThrottle]

    def perform_create(self, serializer: QuestionSerializer):
        serializer.save(author=self.request.user)  # type: ignore

    def get_throttles(self) -> list[Any]:
        if self.action == 'list' or self.action == 'retrieve':
            return [QuestionGetThrottle()]
        if self.action == 'create' or self.action == 'put':
            return [QuestionPostThrottle()]
        return []


class AnswerListCreateView(generics.ListCreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend,
        filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author__username', 'content']
    search_fields = ['content']
    ordering_fields = ['content', 'author__username']
    ordering = ['content']

    def perform_create(self, serializer: AnswerSerializer):
        serializer.save(author=self.request.user)  # type: ignore

    # def get_queryset(self):
    #     queryset =  Answer.objects.all()
    #     content_param = self.request.query_params.get('content',None)

    #     if content_param is not None:
    #         queryset =queryset.filter(content__icontains=content_param)

    #     author_param = self.request.query_params.get('author',None)
    #     if author_param is not None:
    #         queryset= queryset.filter(author__username=author_param)

    #     return queryset


class AnswerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsOwnerOrAdmin]


class LargeResultsSetPagination(pagination.PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100
    page_query_param = 'p'


class CustomLimitOffsetPagination(pagination.LimitOffsetPagination):
    default_limit = 10
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit=100
    
    
class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsOwnerOrAdmin]
    pagination_class = CustomLimitOffsetPagination

    def perform_create(self, serializer:LikeSerializer):
        serializer.save(user=self.request.user) # type: ignore
