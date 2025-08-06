from typing import cast
from django.urls import reverse
from django.contrib.auth.models import User
from django.test.client import Client
from rest_framework.test import APITestCase, APIClient  # type: ignore
from rest_framework import status  # type: ignore
from rest_framework.utils.serializer_helpers import ReturnList, ReturnDict  # type: ignore
from rest_framework.response import Response  # type: ignore
from .models import Question
from forum_app.api.serializers import QuestionSerializer
from django.http import HttpResponse

mock_data = {'title': 'test-question',
             'content': 'test-content', 'category': 'frontend'}


class LikeTest(APITestCase):

    def test_get_like(self) -> None:
        self.client: Client
        url: str = reverse('like-list')
        response: HttpResponse = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_static_url_like(self) -> None:
        url: str = 'http://127.0.0.1:8000/api/forum/likes/'
        response: HttpResponse = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_answers(self) -> None:
        url: str = reverse('answer-list-create')
        response: HttpResponse = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class QuestionTests(APITestCase):

    def xsetUp(self) -> None:
        self.user: User = User.objects.create_user(
            username="Testuser", password="1234")
        client = cast(APIClient, self.client)
        client.force_authenticate(user=self.user)  # type: ignore
        url: str = reverse('question-list')
        response: HttpResponse = self.client.post(
            url, data={**mock_data, 'author': self.user.pk})
        typed_response: Response = cast(Response, response)
        self.question_pk: int = typed_response.data['id']  # type: ignore

    def setUp(self) -> None:
        self.user: User = User.objects.create_user(
            username="Testuser", password="1234")
        self.question: Question = Question.objects.create(
            title="Test Question", content="Test Content", author=self.user, category="backend")

    def test_post_question(self) -> None:
        url: str = reverse('question-list')
        client = cast(APIClient, self.client)
        client.login(username="Testuser",password="1234")
        
        self.assertEqual(Question.objects.count(), 1)
        
        response: HttpResponse = self.client.post(
            url, data={**mock_data, 'author': self.user.pk}, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.count(), 2)
        
        client.logout()
        
        response: HttpResponse = self.client.post(
            url, data={**mock_data, 'author': self.user.pk}, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_question(self) -> None:
        url: str = reverse('question-detail', kwargs={'pk': self.question.pk})
        response: HttpResponse = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data: ReturnList | ReturnDict = QuestionSerializer(
            self.question).data
        self.assertEqual(response.data, expected_data)  # type: ignore
        self.assertDictEqual(response.data, expected_data)  # type: ignore
        self.assertJSONEqual(response.content, expected_data)
        self.assertContains(response, "title")
        self.assertNotContains(response, "titles")
