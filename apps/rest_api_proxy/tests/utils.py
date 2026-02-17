def parametrize(names: str, entries: list[tuple]):
    def inner(func):
        def wrap(self):
            for entry in entries:
                func(self, **dict(zip(names.split(','), entry)))
        return wrap
    return inner


