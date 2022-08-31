from django.urls import path
from tweet import views

app_name = "tweet"

urlpatterns = [
    path("create/", views.CreateTweet.as_view(), name="CreateTweet"),
    path("list/", views.TweetsListView.as_view(), name="TweetsListView"),
    # ...........<int:tweet_id>... accepts integer in its place and then passes it to the view as key-word argument.
    path("detail/<int:tweet_id>/", views.TweetDetailView.as_view(), name="TweetDetailView"),
    path("update/", views.TweetUpdateView.as_view(), name="TweetUpdateView"),
    path("like-unlike/<int:tweet_id>/", views.LikeUnlikeTweetView.as_view(), name="LikeUnlikeTweetView"),
    path("likes/<int:tweet_id>/", views.LikesListView.as_view(), name="LikesListView"),
]
