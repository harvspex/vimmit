def __validate_url(user_input: str, default_scheme='https') -> str:
    from urllib.parse import urlparse, urlunparse

    parsed = urlparse(user_input)

    if not parsed.scheme:
        parsed = urlparse(f"{default_scheme}://{user_input}")

    if not parsed.netloc:
        return None

    parsed = parsed._replace(path='/vault/')
    return urlunparse(parsed)


def input_base_url() -> str:
    print('Please enter base url (hint: vimm dot net):')
    while True:
        user_input = input('>> ').strip()
        base_url = __validate_url(user_input)
        if not base_url:
            print('Please enter valid url:')
            continue

        return base_url
