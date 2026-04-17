def helper(x):
    return x + 1


def public(value):
    base = helper(value)
    return base * 2


def isolated():
    return 0
