from rest_framework import status
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from tweet import models
from tweet import serializers


class CreateTweet(APIView):
    """
    Controller to create a new tweet.
    """

    def post(self, request: Request):
        """
        create new tweet and return the tweet data.

        :param request: Data gained from client.
        :return: Newly created tweet.
        """

        tweet_serializer = serializers.TweetSerializer(data=request.data)

        if tweet_serializer.is_valid():
            tweet_serializer.save(author=request.user)
            return Response(tweet_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(tweet_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TweetsListView(ListAPIView):
    """
    Controller for listing all the tweets with pagination, default pagination is 20.
    """
    queryset = models.Tweet.objects.all()
    serializer_class = serializers.TweetListViewSerializer


class TweetDetailView(APIView):
    """
    Controller for getting the detail view of a single tweet. Tweet ID must be passed in the url itself.
    """

    def get(self, request: Request, tweet_id: int):
        """
        returns tweet, if exists else 404

        :param request: Data gained from client.
        :param tweet_id: Tweet ID to get data of.
        :return: Detailed tweet data.
        """

        tweet = get_object_or_404(models.Tweet, id=tweet_id)
        tweet_serializer = serializers.TweetSerializer(instance=tweet)

        return Response(tweet_serializer.data, status=status.HTTP_200_OK)


class TweetUpdateView(APIView):
    """
    Controller to update a tweet. Data will be passed in POST request.
    """

    def post(self, request: Request):
        """
        checks for ownership, updates the tweet if found and returns the updated tweet data.

        :param request: Data gained from client.
        :return: Updated tweet data.
        """

        update_parameters_serializer = serializers.TweetUpdateRequestParametersSerializer(
            data=request.data
        )

        if not update_parameters_serializer.is_valid():
            return Response(
                update_parameters_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        tweet = get_object_or_404(
            models.Tweet,
            id=update_parameters_serializer.validated_data.get("tweet_id")
        )

        # Check if current user is the one, who posted the tweet.
        if request.user.id != tweet.author_id:
            return Response({
                "detail": "Can't modify other users tweet."
            }, status=status.HTTP_401_UNAUTHORIZED)

        tweet.tweet = update_parameters_serializer.validated_data.get("tweet")
        tweet.save()

        return Response(
            serializers.TweetSerializer(instance=tweet).data,
            status=status.HTTP_200_OK
        )
