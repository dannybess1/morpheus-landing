def singleton(cls):
    """
    Simple decorator to create singleton classes
    """
    _instance = None

    def get_instance(*args, **kwargs):
        nonlocal _instance
        if _instance is None:
            _instance = cls(*args, **kwargs)
        return _instance

    return get_instance