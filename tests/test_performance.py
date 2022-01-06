import timeit


# Tests the time it takes to write a new item to cookies
import pickle
import random
import string

def add_item_to_cookies(item, coef):
    user_id = random.randint(1, 10)
    user_cookies = None
    with open('test_cookies', 'rb') as tc:
        test_cookies = pickle.load(tc)
        user_cookies = test_cookies.get(user_id) or {} # sets the cookies to an empty dict if they are None
    if item not in user_cookies.keys():
        user_cookies[item] = coef
    else:
        user_cookies[item] += coef
    test_cookies[user_id] = user_cookies
    with open('test_cookies', 'wb') as pc:
        pickle.dump(test_cookies, pc)

cookies_test_time = timeit.timeit("add_item_to_cookies(''.join([random.choice(string.ascii_letters) for i in range(5)]), random.randint(-10, 10))", number=1000, setup='from __main__ import add_item_to_cookies; import random; import string; import pickle')
with open('test_cookies', 'wb') as tc:
    pickle.dump({}, tc)
print(cookies_test_time)