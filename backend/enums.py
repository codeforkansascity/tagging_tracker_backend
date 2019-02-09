import enum


class IterEnumMeta(enum.EnumMeta):
    def __iter__(self):
        return ((choice.name, choice.value) for choice in super().__iter__())


class IterEnum(enum.Enum, metaclass=IterEnumMeta):
    def __str__(self):
        return self.name
