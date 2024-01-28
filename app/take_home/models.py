from django.db import models


class BaseModel(models.Model):
    created = models.DateTimeField(null=True, auto_now_add=True)
    last_modified = models.DateTimeField(null=True, auto_now=True)

    class Meta:
        abstract = True


class Book(BaseModel):
    id = models.PositiveIntegerField(primary_key=True, unique=True, editable=False)
    rating_sum = models.PositiveIntegerField()
    rating_count = models.PositiveIntegerField()


class BookReview(BaseModel):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review = models.CharField(max_length=1000)
