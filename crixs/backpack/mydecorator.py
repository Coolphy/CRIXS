def func_cache(func):
    func.cache = {}

    def wrapper(*args, **kwargs):
        key = tuple(
            (
                arg
                if isinstance(arg, tuple)
                else tuple(arg) if isinstance(arg, list) else arg
            )
            for arg in args
        ) + tuple(kwargs.items())
        if key in func.cache:
            return func.cache[key]
        else:
            try:
                result = func(*args, **kwargs)
                func.cache[key] = result
                return result
            except Exception as e:
                raise ValueError(f"[Error] in {func.__name__}: {e}")

    return wrapper
