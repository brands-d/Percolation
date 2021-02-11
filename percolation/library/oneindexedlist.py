class OneIndexedList(list):
    def __getitem__(self, i):
        return super().__getitem__(i - 1)

    def __setitem__(self, i, value):
        return super().__setitem__(i - 1, value)
