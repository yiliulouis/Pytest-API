
import logging as logger
import random
import string

def generate_random_email_and_password(domain=None,email_prefix=None):
    logger.debug("Generating random email and passwords")

    if not domain:
        domain = 'louisliu.com'
    if not email_prefix:
        email_prefix = 'testuser'

    random_email_string_length = 5
    random_string = ''.join(random.choices(string.ascii_lowercase, k=random_email_string_length))

    email = email_prefix + '_' + random_string + '@' + domain

    password_string_length = 8
    password_string = ''.join(random.choices(string.ascii_letters, k=password_string_length))

    random_info = {'email':email,'password':password_string}
    logger.debug(f"Randomly generate email and password:{random_info}")

    return random_info


def generate_random_string(length = 10,prefix = None, suffix = None):

    random_string = ''.join(random.choices(string.ascii_lowercase, k=length))

    if prefix:
        random_string = prefix + random_string
    if suffix:
        random_string = random_string +suffix

    return random_string

    