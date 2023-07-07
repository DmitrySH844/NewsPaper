from django.forms import DateInput, RadioSelect
from django_filters import FilterSet, ModelMultipleChoiceFilter, DateTimeFilter, ChoiceFilter
from .models import Post, Category


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