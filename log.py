ENABLE_LOGGING = False


def set_logging(b):
    global ENABLE_LOGGING
    ENABLE_LOGGING = b


def log(s):
    if ENABLE_LOGGING:
        print(s)
