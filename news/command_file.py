from django.contrib.auth.models import User
from news.models import Author
from news.models import Category
from news.models import Post
from news.models import Comment

new_user_1 = User.objects.create_user('Person1')
author_1 = Author.objects.create(full_name='John Grant', user=new_user_1)

new_user_2 = User.objects.create_user('Person2')
author_2 = Author.objects.create(full_name='Joe Lee', user=new_user_2)

new_user_3 = User.objects.create_user('Person3')
author_3 = Author.objects.create(full_name='Michael Black', user=new_user_3)

new_user_4 = User.objects.create_user('Person4')
author_4 = Author.objects.create(full_name='George Sweem', user=new_user_4)

Category.objects.bulk_create([Category(name_category='policy'), Category(name_category='economic'), Category(name_category='sport'), Category(name_category='education'), Category(name_category='culture')])

news_1 = '''More than 3,500 people, including hundreds of Turkish nationals, have arrived in Ethiopia after fleeing heavy fighting in Sudan, an official from the UN’s International Organization for Migration told AFP.'''

article_1 = '''Newly appointed female Saudi ambassadors to the European Union and Finland presented their credentials to the presidents of their respective missions, Saudi Arabia’s foreign ministry announced on Monday.
Ambassadors Haifa al-Jedea and Nesreen al-Shebel were appointed to their new positions in January in a move by the Kingdom that further boosted the presence of Saudi female diplomats in the international arena. '''

article_2 = '''Elections will be held in the semi-autonomous Kurdistan region of northern Iraq on Nov. 18, the regional government spokesman said on Sunday.
Iraqi Kurdistan President Nechirvan Barzani issued a decree on Sunday and approved the date, KRG spokesman Dilshad Shahab told a news conference.
The vote should elect both a parliament and a president for Kurdish regions which have gained self-rule in 1991.'''

post_1 = Post.objects.create(text_type='News',title='More than 3,500 have fled Sudan for Ethiopia: UN', text=news_1, author=author_3).category.add(*Category.objects.filter(name_category__in=['Policy']))

post_2 = Post.objects.create(text_type='News',title='Newly appointed female Saudi ambassadors to EU, Finland present credentials', text=article_1, author=author_3).category.add(*Category.objects.filter(name_category__in=['Policy']))

post_3 = Post.objects.create(text_type='Article',title='Iraq’s Kurdistan region to hold elections on Nov. 18', text=article_2, author=author_4).category.add(*Category.objects.filter(name_category__in=['Policy']))

comment_1 = Comment.objects.create(comment_text='Stop war!!!', post=post_1, user=author_4)



