from rest_framework import serializers

from tweet import models
from user.serializer import UserSerializer


class TweetSerializer(serializers.ModelSerializer):
    """
    Serializes tweet for detail view and for update.
    """
    # To get the username of the author
    author_username = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = models.Tweet
        fields = (
            "id", "author", "like_count", "retweet_count", "author_username",
            "creation_datetime", "update_datetime", "tweet", "retweet_id", "thread_id",
        )
        read_only_fields = (
            "id", "author", "like_count", "retweet_count", "author_username",
            "creation_datetime", "update_datetime", "retweet_id", "thread_id",
        )


class TweetListViewSerializer(serializers.ModelSerializer):
    """
    Gets the list view of the tweet. Same as above but everything is un-editable in here.
    """

    author_username = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = models.Tweet
        fields = (
            "id", "author", "like_count", "retweet_count", "author_username",
            "creation_datetime", "update_datetime", "tweet", "retweet_id", "thread_id",
        )
        read_only_fields = (
            "id", "author", "like_count", "retweet_count", "author_username",
            "creation_datetime", "update_datetime", "tweet", "retweet_id", "thread_id",
        )


class TweetUpdateRequestParametersSerializer(serializers.Serializer):
    """
    Serializer to accept the parameters for updating the tweet.
    """

    tweet_id = serializers.IntegerField()
    tweet = serializers.CharField(
        max_length=281
    )

    # Requirement of the framework.
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class LikeSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = models.Like
        fields = ("creation_datetime", "tweet_id", "author")
