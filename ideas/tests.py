from django.test import TestCase
from users.models import User
from ideas.models import Idea
from graphene.test import Client
from core.schema import schema
import jwt
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class TestIdeaSchema(TestCase):

    def setUp(self):
        """
        Set up test environment.
        """
        self.user = User.objects.create_user(username='john', password='123')
        self.client = Client(schema)
        self.token = jwt.encode({"username": self.user.username}, settings.SECRET_KEY, algorithm='HS256')

    def _get_mock_context(self):
        """
        Returns a mock context object with a user attribute.
        """
        mock_context = type("", (), {})()
        mock_context.user = self.user
        return mock_context

    def test_resolve_my_ideas(self):
        """
        Test that resolve_my_ideas returns correct ideas for authenticated user.
        """
        Idea.objects.create(user=self.user, text="Test idea")

        query = '''
        {
            myIdeas {
                text
            }
        }
        '''

        headers = {
            "HTTP_AUTHORIZATION": f"JWT {self.token.decode('utf-8')}"
        }

        mock_context = self._get_mock_context()

        executed = self.client.execute(query, context_value=mock_context, headers=headers)
        logger.debug(executed)
        
        self.assertNotIn('errors', executed)
        self.assertEqual(executed['data']['myIdeas'][0]['text'], "Test idea")
