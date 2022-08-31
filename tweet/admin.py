from django.contrib import admin
from tweet import models


@admin.register(models.Tweet)
class TweetAdmin(admin.ModelAdmin):
    """
    Admin page for Tweet Model. Better styling for the fields.
    """

    @staticmethod
    def author_username(tweet):
        return tweet.author.username

    fieldsets = (
        ("Ownership", {
            "fields": ("author", "tweet")
        }),
    )

    list_display = ("author_username", "striped_tweet", "creation_datetime", "update_datetime")
    search_fields = ("tweet", "get_author_username")
    list_filter = ("creation_datetime", "update_datetime")
    autocomplete_fields = ("author",)
