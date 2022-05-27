# from django.test import TestCase

# # Create your tests here.
# import random
# import string
# ''.join(random.choices(string.ascii_uppercase + string.digits, k=17))
import string
import random
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
id_generator()