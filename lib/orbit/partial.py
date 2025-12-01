class partial:
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.pre_args = args
        self.pre_kwargs = kwargs

    def __call__(self, *args, **kwargs):
        # Merge saved and new args
        new_kwargs = self.pre_kwargs.copy()
        new_kwargs.update(kwargs)
        return self.func(*self.pre_args, *args, **new_kwargs)
