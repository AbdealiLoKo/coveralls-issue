from __future__ import annotations

import pytest
from sqlalchemy import Column, Integer, Text, select
from sqlalchemy.dialects import mssql, mysql, oracle, sqlite


def dialect_parametrizer():
    return pytest.mark.parametrize(
        "dialect",
        [mysql.dialect(), mssql.dialect(), oracle.dialect(), sqlite.dialect()],
    )


@dialect_parametrizer()
def test_text_order_by(dialect):
    col = Column("col", Text())
    statement = select().add_columns(col).order_by(col)
    with pytest.raises(AssertionError):
        statement.compile(dialect=dialect)


@dialect_parametrizer()
def test_duplicates_in_order_by(dialect):
    col = Column("col", Integer())
    statement = select().add_columns(col).order_by(col, col)
    with pytest.raises(AssertionError):
        statement.compile(dialect=dialect)
