from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.urls import reverse


class Author(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.CharField(max_length=255)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        author_article_rating = Post.objects.filter(author_id=self).aggregate(models.Sum('rating'))['rating__sum']
        author_comment_rating = Comment.objects.filter(post_id__author_id=self).aggregate(models.Sum('rating'))['rating__sum']
        post_ids = Post.objects.filter(author_id=self).values_list('id', flat=True)
        to_author_article_comment_rating = Comment.objects.filter(post_id__in=post_ids).aggregate(models.Sum('rating'))['rating__sum']

        if author_article_rating is None:
            author_article_rating = 0
        if author_comment_rating is None:
            author_comment_rating = 0
        if to_author_article_comment_rating is None:
            to_author_article_comment_rating = 0

        print(author_article_rating, author_comment_rating, to_author_article_comment_rating)
        self.rating = (int(author_article_rating) * 3) + int(author_comment_rating) + int(to_author_article_comment_rating)
        print(self.rating)
        self.save()

class Category(models.Model):
    name_category = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name_category



class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    CHOICES = [
        ('Article', (
            ('PL', 'Policy'),
            ('EC', 'Economic'),
            ('SP', 'Sport'),
            ('ED', 'Education'),
            ('CL', 'Culture'),
        )
         ),
        ('News', (
            ('PL', 'Policy'),
            ('EC', 'Economic'),
            ('SP', 'Sport'),
            ('ED', 'Education'),
            ('CL', 'Culture'),
        )
         ),
    ]
    title = models.CharField(max_length=300)
    text_type = models.CharField(max_length=300, choices=CHOICES)

    def _str_(self):
        return self.title

    category = models.ManyToManyField('Category', through='PostCategory')
    creation_datetime = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    rating = models.IntegerField(default=0, db_column='rating')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        content = self.text[:124]
        if len(self.text) > 124:
            content += '...'
        return content

    def get_absolute_url(self):
        return reverse('post_dtl', args=[str(self.pk)])


class PostCategory(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    comment_text = models.TextField()
    time_in = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0, db_column='rating')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

class Subscribers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, )





# Create your models here.
