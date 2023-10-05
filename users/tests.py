from django.test import TestCase
from users.models import User
from graphene.test import Client
from core.schema import schema
import jwt
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class UserGraphQLTestCase(TestCase):

    def setUp(self) -> None:
        """
        Setup test environment.
        """
        self.user: User = User.objects.create_user(username='testuser', password='testpass')
        self.client: Client = Client(schema)
        self.token: str = jwt.encode({"username": self.user.username}, settings.SECRET_KEY, algorithm='HS256').decode('utf-8')

    def _get_mock_context(self):
        """
        Returns a mock context object with a user attribute.
        """
        mock_context = type("", (), {})()
        mock_context.user = self.user
        return mock_context

    def test_search_users(self):
        """
        Test if searchUsers query returns correct data.
        """
        headers = {
            "HTTP_AUTHORIZATION": f"JWT {self.token}"
        }

        mock_context = self._get_mock_context()

        query = '''
        query {
            searchUsers(searchText: "test") {
                username
                email
                following
                followers
            }
        }
        '''
        executed = self.client.execute(query, context_value=mock_context, headers=headers)
        logger.debug(executed)

        self.assertNotIn('errors', executed, "Query should not return errors")
        self.assertIn('data', executed, "Query should return data")
        self.assertIn('searchUsers', executed['data'], "Query should return searchUsers field")
        users = executed['data']['searchUsers']
        self.assertIsInstance(users, list, "Should return a list of users")
        for user in users:
            self.assertIn('username', user)
            self.assertIn('email', user)
            self.assertIn('following', user)
            self.assertIn('followers', user)
