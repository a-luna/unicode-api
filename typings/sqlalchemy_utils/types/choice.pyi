from enum import Enum
from typing import Any, Self

from sqlalchemy import Dialect, types

from ..exceptions import ImproperlyConfigured
from .scalar_coercible import ScalarCoercible

class Choice:
    def __init__(self, code: str, value: Any): ...
    def __eq__(self, other: Self) -> bool: ...
    def __hash__(self) -> int: ...
    def __ne__(self, other: Self) -> bool: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...

class ChoiceType(ScalarCoercible, types.TypeDecorator):
    """
    ChoiceType offers way of having fixed set of choices for given column. It
    could work with a list of tuple (a collection of key-value pairs), or
    integrate with :mod:`enum` in the standard library of Python 3.

    Columns with ChoiceTypes are automatically coerced to Choice objects while
    a list of tuple been passed to the constructor. If a subclass of
    :class:`enum.Enum` is passed, columns will be coerced to :class:`enum.Enum`
    objects instead.

    ::

        class User(Base):
            TYPES = [
                ('admin', 'Admin'),
                ('regular-user', 'Regular user')
            ]

            __tablename__ = 'user'
            id = sa.Column(sa.Integer, primary_key=True)
            name = sa.Column(sa.Unicode(255))
            type = sa.Column(ChoiceType(TYPES))


        user = User(type='admin')
        user.type  # Choice(code='admin', value='Admin')

    Or::

        import enum


        class UserType(enum.Enum):
            admin = 1
            regular = 2


        class User(Base):
            __tablename__ = 'user'
            id = sa.Column(sa.Integer, primary_key=True)
            name = sa.Column(sa.Unicode(255))
            type = sa.Column(ChoiceType(UserType, impl=sa.Integer()))


        user = User(type=1)
        user.type  # <UserType.admin: 1>


    ChoiceType is very useful when the rendered values change based on user's
    locale:

    ::

        from babel import lazy_gettext as _


        class User(Base):
            TYPES = [
                ('admin', _('Admin')),
                ('regular-user', _('Regular user'))
            ]

            __tablename__ = 'user'
            id = sa.Column(sa.Integer, primary_key=True)
            name = sa.Column(sa.Unicode(255))
            type = sa.Column(ChoiceType(TYPES))


        user = User(type='admin')
        user.type  # Choice(code='admin', value='Admin')

        print user.type  # 'Admin'

    Or::

        from enum import Enum
        from babel import lazy_gettext as _


        class UserType(Enum):
            admin = 1
            regular = 2


        UserType.admin.label = _('Admin')
        UserType.regular.label = _('Regular user')


        class User(Base):
            __tablename__ = 'user'
            id = sa.Column(sa.Integer, primary_key=True)
            name = sa.Column(sa.Unicode(255))
            type = sa.Column(ChoiceType(UserType, impl=sa.Integer()))


        user = User(type=UserType.admin)
        user.type  # <UserType.admin: 1>

        print user.type.label  # 'Admin'
    """

    impl: types.TypeEngine
    cache_ok: bool

    def __init__(self, choices: list[tuple[str, Any]] | Enum, impl: types.TypeEngine | None = None): ...
    @property
    def python_type(self) -> Any: ...
    def _coerce(self, value: Any) -> Choice | Enum: ...
    def process_bind_param(self, value: Any, dialect: Dialect) -> Any: ...
    def process_result_value(self, value: Any, dialect: Dialect) -> Choice | Enum: ...

class ChoiceTypeImpl:
    """The implementation for the ``Choice`` usage."""

    choices_dict: dict[str, Any]

    def __init__(self, choices: list[tuple[str, Any]]): ...
    def _coerce(self, value: Any) -> Choice: ...
    def process_bind_param(self, value: Any, dialect: Dialect) -> Any: ...
    def process_result_value(self, value: Any, dialect: Dialect) -> Choice: ...

class EnumTypeImpl:
    """The implementation for the ``Enum`` usage."""

    def __init__(self, enum_class: Enum): ...
    def _coerce(self, value: Any) -> Enum: ...
    def process_bind_param(self, value: Any, dialect: Dialect) -> Any: ...
    def process_result_value(self, value: Any, dialect: Dialect) -> Enum: ...
