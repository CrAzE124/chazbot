import requests
import time
from faker import Factory
from random import randint

fake = Factory.create()


def generate_email_address():
    return fake.email()


def get_random_user_agent():
    agents = (
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.5; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 SeaMonkey/2.7.1',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.3; Trident/7.0; .NET4.0E; .NET4.0C)',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)',
        'Mozilla/5.0 (X11; Linux i686; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 SeaMonkey/2.7.1'
    )

    return agents[randint(0, len(agents) - 1)]


def do_register(email):
    password = 'asdgasdfgasdf'

    req = requests.post('http://electriccircus.co.za/index.php/register/do_register/', {
        'rcID': '3598',
        'uEmail': email,
        'uPassword': password,
        'uPasswordConfirm': password,
        'Register': 'Register'
    }, headers={
        'user-agent': get_random_user_agent()
    })

    return req


def do_like(request, cookies):
    return requests.post('http://electriccircus.co.za/credits/like', data={
        'act': 'like',
        'pageID': '613'
    }, cookies=cookies, headers={
        'user-agent': get_random_user_agent()
    })


def do_unlike(request, cookies):
    pass


def run():
    email = generate_email_address()
    registration = do_register(email)

    registration_cookie_jar = None

    for hist in registration.history:
        if len(hist.cookies) > 0:
            registration_cookie_jar = hist.cookies

            break

    if registration_cookie_jar is None:
        return

    like = do_like(registration, registration_cookie_jar)

    if like.status_code == 200:
        print('Done a like with email %s' % email)
    else:
        print('Something went wrong with the like request...')


if __name__ == '__main__':
    for i in range(5):
        try:
            run()
            time.sleep(randint(5, 10))
        except requests.HTTPError as e:
            print(e)
        except requests.ConnectionError as e:
            print(e)
