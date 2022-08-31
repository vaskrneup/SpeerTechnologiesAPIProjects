from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from tweet.models import Tweet


class SetupManagerMixin:
    refresh_token_url = reverse("user:GetRefreshToken")

    headers = {}
    access_token = None
    USERNAME = None
    PASSWORD = None
    client = None
    user = None

    def setup(self) -> None:
        self.user = get_user_model()(username=self.USERNAME)
        self.user.set_password(self.PASSWORD)
        self.user.save()

        response = self.client.post(self.refresh_token_url, {
            "username": self.USERNAME,
            "password": self.PASSWORD
        })
        self.access_token = response.data.get("access")
        self.headers["HTTP_AUTHORIZATION"] = f"Bearer {self.access_token}"


class TestCreateTweet(TestCase, SetupManagerMixin):
    create_tweet_url = reverse("tweet:CreateTweet")

    USERNAME = "admin"
    PASSWORD = "Testing@123"

    def setUp(self) -> None:
        self.setup()

    def test_create_tweet(self):
        response = self.client.post(
            self.create_tweet_url, data={
                "tweet": "Something New"
            },
            **self.headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_blank_tweet(self):
        response = self.client.post(
            self.create_tweet_url, data={
                "tweet": ""
            },
            **self.headers
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_authentication_tweet(self):
        response = self.client.post(
            self.create_tweet_url, data={
                "tweet": "New one, but wont make it!"
            },
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestTweetsListView(TestCase, SetupManagerMixin):
    get_tweet_list_url = reverse("tweet:TweetsListView")

    USERNAME = "admin1"
    PASSWORD = "Testing@123"

    def setUp(self) -> None:
        self.setup()

    def test_get_tweet(self):
        response = self.client.get(
            self.get_tweet_list_url,
            **self.headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_tweet_without_authorization(self):
        response = self.client.get(
            self.get_tweet_list_url,
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestTweetDetailView(TestCase, SetupManagerMixin):
    get_twitter_detail_url = None
    tweet = None

    USERNAME = "admin2"
    PASSWORD = "Testing@123"

    def setUp(self) -> None:
        self.setup()

        self.tweet = Tweet(tweet="This is something new!!", author=self.user)
        self.tweet.save()

        self.get_twitter_detail_url = reverse("tweet:TweetDetailView", kwargs={"tweet_id": self.tweet.id})

    def test_get_detail_tweet(self):
        response = self.client.get(
            self.get_twitter_detail_url,
            **self.headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_non_existence_detail_tweet(self):
        response = self.client.get(
            reverse("tweet:TweetDetailView", kwargs={"tweet_id": self.tweet.id + 912873}),
            **self.headers
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_detail_tweet_without_authorization(self):
        response = self.client.get(
            self.get_twitter_detail_url,
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestTweetUpdateView(TestCase, SetupManagerMixin):
    update_tweet_url = reverse("tweet:TweetUpdateView")
    tweet = None

    USERNAME = "admin2"
    PASSWORD = "Testing@123"

    def setUp(self) -> None:
        self.setup()

        self.tweet = Tweet(tweet="This is something new, next edition!!", author=self.user)
        self.tweet.save()

    def test_updated_tweet(self):
        response = self.client.post(
            self.update_tweet_url, data={
                "tweet_id": self.tweet.id,
                "tweet": "Looks like .. something has changed !!!"
            },
            **self.headers
        )
        self.assertEqual(response.data.get("tweet"), "Looks like .. something has changed !!!")

    def test_update_tweet(self):
        response = self.client.post(
            self.update_tweet_url, data={
                "tweet_id": self.tweet.id,
                "tweet": "Looks like .. something has changed !!!"
            },
            **self.headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_blank_tweet(self):
        response = self.client.post(
            self.update_tweet_url, data={
                "tweet_id": self.tweet.id,
                "tweet": ""
            },
            **self.headers
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_no_authentication_tweet(self):
        response = self.client.post(
            self.update_tweet_url, data={
                "tweet_id": self.tweet.id,
                "tweet": "Looks like .. something has changed !!!"
            },
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
