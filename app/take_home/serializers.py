from take_home.models import BookReview
from rest_framework import serializers


class AuthorSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    birth_year = serializers.IntegerField()
    death_year = serializers.IntegerField()


class BookSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=400)
    authors = AuthorSerializer(many=True)
    languages = serializers.ListField()
    download_count = serializers.IntegerField()


class BookReviewSerializer(serializers.ModelSerializer):
    book_id = serializers.IntegerField()
    rating = serializers.IntegerField(min_value=0, max_value=5)
    review = serializers.CharField(max_length=1000)

    class Meta:
        model = BookReview
        fields = (
            'id',
            'book_id',
            'rating',
            'review',
        )


class BookDetailSerializer(BookSerializer):
    rating = serializers.FloatField()
    reviews = serializers.ListField()
