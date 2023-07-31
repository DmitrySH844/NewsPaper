from django.forms import DateInput, RadioSelect
from django_filters import FilterSet, ModelMultipleChoiceFilter, DateTimeFilter, ChoiceFilter
from .models import Post, Category
from django import forms
from django.utils import timezone
from django_filters.rest_framework import filters

class PostFilter(FilterSet):
    text_type = ChoiceFilter(
        choices=Post.CHOICES,
        widget=RadioSelect,
        label='Category',
    )
    #category = ModelMultipleChoiceFilter(
        #field_name='postcategory__category',
        #queryset=Category.objects.all(),
        #label='Category',
        #conjoined=True,
    #)
    time = DateTimeFilter(
        field_name='creation_datetime',
        lookup_expr='gte',
        widget=DateInput(attrs={'type': 'date'}),
    )

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'text': ['icontains'],
            }
        
class CategoryFilter(FilterSet):
    categories = ModelMultipleChoiceFilter(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input',
        }),
        label="Категории",
    )

    class Meta:
        model = Post
        fields = ['categories']

class WeeklyPostFilter(FilterSet):
    date_published = filters.DateFilter(field_name='t_creation', method='filter_weekly_posts')

    def filter_weekly_posts(self, queryset, name, value):
        today = timezone.now().date()
        last_monday = today - timezone.timedelta(days=today.weekday(), weeks=1)
        last_monday = timezone.datetime.combine(last_monday, timezone.time.min)
        return queryset.filter(t_creation__gte=last_monday)

    class Meta:
        model = Post
        fields = ['date_published']