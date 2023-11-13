from __future__ import annotations

from sqlalchemy import (
    Text,
)
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.elements import ColumnClause, UnaryExpression
from sqlalchemy.sql.operators import asc_op, desc_op
from sqlalchemy.sql.selectable import Select


@compiles(Select)
def compile_select(select_stmt, compiler, **kw):
    # Ensure that we don't sort on a Text() column
    # Oracle does not support that - i.e. ORDER BY desccription -- is not allowed
    for sort_col in select_stmt._order_by_clause.clauses:
        if isinstance(sort_col, ColumnClause) and isinstance(sort_col.type, Text):
            raise AssertionError(
                '"Sort By" should not be done on a Text column as it is not '
                "supported in Oracle."
            )

    if select_stmt._order_by_clause.clauses:
        columns = set()
        for sort_col in select_stmt._order_by_clause.clauses:
            if isinstance(sort_col, UnaryExpression) and sort_col.modifier in (
                asc_op,
                desc_op,
            ):
                sort_col = sort_col.element
            if isinstance(sort_col, ColumnClause) and sort_col in columns:
                raise AssertionError(
                    '"Sort By" should not be done on the same column multiple '
                    "times in MS SQL"
                )
            else:
                columns.add(sort_col)


if Select is True:
    print("some code that will never be executed")
