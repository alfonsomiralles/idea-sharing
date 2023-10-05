from django.test import TestCase
from users.models import User
from followers.models import FollowRequest
from graphene.test import Client
from core.schema import schema
import jwt
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class TestFollowerSchema(TestCase):

    def setUp(self):
        """
        Set up test environment.
        """
        self.user1 = User.objects.create_user(username='alice', password='123')
        self.user2 = User.objects.create_user(username='bob', password='123')
        self.client = Client(schema)
        self.token = jwt.encode({"username": self.user1.username}, settings.SECRET_KEY, algorithm='HS256')

    def _get_mock_context(self, user):
        """
        Returns a mock context object with a user attribute.
        """
        mock_context = type("", (), {})()
        mock_context.user = user
        return mock_context

    def test_resolve_follow_requests(self):
        """
        Test that resolve_follow_requests returns correct follow requests for authenticated user.
        """
        FollowRequest.objects.create(from_user=self.user2, to_user=self.user1)

        query = '''
        {
            followRequests {
                fromUser {
                    username
                }
                toUser {
                    username
                }
            }
        }
        '''

        headers = {
            "HTTP_AUTHORIZATION": f"JWT {self.token.decode('utf-8')}"
        }

        mock_context = self._get_mock_context(self.user1)

        executed = self.client.execute(query, context_value=mock_context, headers=headers)
        logger.debug(executed)
        
        self.assertNotIn('errors', executed)
        self.assertEqual(executed['data']['followRequests'][0]['fromUser']['username'], "bob")
        self.assertEqual(executed['data']['followRequests'][0]['toUser']['username'], "alice")

    def test_send_follow_request(self):
        """
        Test that send_follow_request mutation sends a follow request.
        """
        mutation = '''
        mutation {
            sendFollowRequest(usernameToFollow: "bob") {
                success
            }
        }
        '''

        headers = {
            "HTTP_AUTHORIZATION": f"JWT {self.token.decode('utf-8')}"
        }

        mock_context = self._get_mock_context(self.user1)

        executed = self.client.execute(mutation, context_value=mock_context, headers=headers)
        logger.debug(executed)

        self.assertNotIn('errors', executed)
        self.assertTrue(executed['data']['sendFollowRequest']['success'])

        follow_request_exists = FollowRequest.objects.filter(from_user=self.user1, to_user=self.user2).exists()
        self.assertTrue(follow_request_exists)
