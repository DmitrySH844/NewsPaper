from django import template

register = template.Library()



bad_words = ["редиска", "Редиски", "петух гамбургской", "Новохудоноссор"]

@register.filter()
def censor(value):
   for word in bad_words:
      if word.lower() in value.lower():
         value = value.replace(word[1:-2], '*' * (len(word)-1))
   return value


