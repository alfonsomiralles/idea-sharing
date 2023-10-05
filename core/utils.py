def ensure_authenticated(user):
    if user.is_anonymous:
        raise Exception('Not logged in!')