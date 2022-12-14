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


class LikeUnlikeTweetView(APIView):
    """
    Controller to create a new tweet.
    """

    def post(self, request: Request, tweet_id: int):
        """
        like tweet, if not already liked else, unlike the tweet.

        :param request: Data gained from client.
        :param tweet_id: ID of the tweet to update likes on.
        :return: updated tweet.
        """

        tweet = get_object_or_404(models.Tweet, id=tweet_id)

        if like := models.Like.objects.filter(tweet_id=tweet_id, author_id=request.user.id).first():
            like.delete()
            tweet.like_count -= 1
        else:
            models.Like(tweet_id=tweet_id, author=request.user).save()
            tweet.like_count += 1

        tweet.save()
        tweet_serializer = serializers.TweetSerializer(instance=tweet)

        return Response(tweet_serializer.data, status=status.HTTP_200_OK)


class LikesListView(ListAPIView):
    """
    Controller for listing all the likes with pagination, default pagination is 20.
    """

    serializer_class = serializers.LikeSerializer

    def get_queryset(self):
        """
        returns query, through which the List Data is created

        :return: Django Query
        """

        return models.Like.objects.filter(
            tweet_id=self.kwargs.get("tweet_id")
        ).order_by("-creation_datetime")


class RetweetView(APIView):
    """
    Controller to do a retweet
    """

    def post(self, request: Request, tweet_id: int):
        """
        Creates a retweet and binds it to the original post.

        :param request: Data gained from client.
        :param tweet_id: ID of the tweet to bind retweet to.
        :return: new retweet
        """

        retweet_tweet = get_object_or_404(models.Tweet, id=tweet_id)

        tweet_serializer = serializers.TweetSerializer(data=request.data)

        if tweet_serializer.is_valid():
            tweet_serializer.save(author=request.user, retweet=retweet_tweet)
            retweet_tweet.retweet_count += 1
            retweet_tweet.save()

            return Response(tweet_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(tweet_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetRetweetsListView(ListAPIView):
    """
    Controller for listing all the retweets for a particular tweet with pagination, default pagination is 20.
    """

    serializer_class = serializers.TweetSerializer

    def get_queryset(self):
        """
         returns query, through which the List Data is created

         :return: Django Query
         """

        return models.Tweet.objects.filter(
            retweet_id=self.kwargs.get("tweet_id")
        ).order_by("-creation_datetime")


class DeleteTweetView(APIView):
    """
    Deletes the tweet with given id.
    """

    def delete(self, request: Request, tweet_id: int):
        """
        Deletes the given tweet or retweet.
        In case of tweet, all its retweet too will be deleted.
        In case of retweet, the retweet count on the first one will be deleted.

        :param request: Data gained from client.
        :param tweet_id: Tweet to be deleted.
        :return: deleted tweet
        """

        tweet = get_object_or_404(models.Tweet, id=tweet_id)

        if tweet.retweet:
            tweet.retweet.retweet_count -= 1
        if tweet.thread:
            tweet.retweet.thread_count -= 1
        if tweet.retweet or tweet.thread:
            tweet.retweet.save()

        tweet.delete()

        return Response(serializers.TweetSerializer(instance=tweet).data, status=status.HTTP_200_OK)


class CreateThreadView(APIView):
    """
    Controller to create a thread.
    """

    def post(self, request: Request, tweet_id: int):
        """
        Creates a new post as a thread and binds it to the original post.

        :param request: Data gained from client.
        :param tweet_id: ID of the tweet to bind thread to.
        :return: new thread
        """

        thread_tweet = get_object_or_404(models.Tweet, id=tweet_id)

        tweet_serializer = serializers.TweetSerializer(data=request.data)

        if tweet_serializer.is_valid():
            tweet_serializer.save(author=request.user, thread=thread_tweet)
            thread_tweet.thread_count += 1
            thread_tweet.save()

            return Response(tweet_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(tweet_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetThreadsView(ListAPIView):
    """
    Controller for listing all the threads for a particular tweet with pagination, default pagination is 20.
    """

    serializer_class = serializers.TweetSerializer

    def get_queryset(self):
        """
         returns query, through which the List Data is created

         :return: Django Query
         """

        return models.Tweet.objects.filter(
            thread_id=self.kwargs.get("tweet_id")
        ).order_by("-creation_datetime")
