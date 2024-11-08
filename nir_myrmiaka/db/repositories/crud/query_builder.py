from sqlalchemy import func, or_, not_, select, update, delete
from sqlalchemy.sql import ClauseElement, Select
from typing import Union, Type, TypeVar, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")


class QueryBuilder:
    """
    A utility class for constructing flexible and complex SQLAlchemy queries.

    This class provides a fluent interface for chaining various SQL query conditions,
    including support for AND, OR, NOT filters, custom expressions, aggregations,
    grouping, ordering, distinct results, and pagination. It also allows the application
    of complex SQLAlchemy expressions directly to the query.

    Attributes:
        model (Type[T]): The SQLAlchemy model class the query is based on.
        _filters (List[ClauseElement]): Stores all filter conditions, including AND, OR, and NOT conditions.
        _expressions (List[ClauseElement]): Stores custom SQLAlchemy expressions.
        _selected_columns (Optional[List[ClauseElement]]): Columns selected for retrieval from the model.
        _aggregate (Optional[ClauseElement]): Aggregation function to apply (e.g., COUNT, SUM).
        _limit (Optional[int]): Limit for the number of results.
        _offset (Optional[int]): Offset for pagination.
        _order_by (List[ClauseElement]): Fields to order results by.
        _desc_order (bool): True if ordering in descending order.
        _group_by (Optional[List[ClauseElement]]): Columns for grouping results.
        _having (Optional[ClauseElement]): Condition for HAVING clause.
        _distinct (bool): True if DISTINCT should be applied to results.
    """

    def __init__(self, model: Type[T]):
        """
        Initialize a QueryBuilder instance for a specified SQLAlchemy model.

        :param model: The SQLAlchemy model to build queries for.
        """
        self.model = model
        self._filters: List[ClauseElement] = []
        self._expressions: List[ClauseElement] = []
        self._selected_columns: Optional[List[ClauseElement]] = None
        self._aggregate: Optional[ClauseElement] = None
        self._limit = None
        self._offset = None
        self._order_by = []
        self._desc_order = False
        self._group_by: Optional[List[ClauseElement]] = None
        self._having: Optional[ClauseElement] = None
        self._distinct = False

    def filter_by(self, **conditions) -> "QueryBuilder":
        """
        Apply AND filters to the query.

        :param conditions: Key-value pairs of model attributes and their values for filtering.
        :return: The QueryBuilder instance with updated filters.
        """
        for field, value in conditions.items():
            self._filters.append(getattr(self.model, field) == value)
        return self

    def or_filter_by(self, **conditions) -> "QueryBuilder":
        """
        Apply OR filters to the query.

        :param conditions: Key-value pairs of model attributes and their values for OR filtering.
        :return: The QueryBuilder instance with OR filters added.
        """
        or_conditions = [
            getattr(self.model, field) == value for field, value in conditions.items()
        ]
        self._filters.append(or_(*or_conditions))
        return self

    def not_filter_by(self, **conditions) -> "QueryBuilder":
        """
        Apply NOT filters to the query.

        :param conditions: Key-value pairs of model attributes and their values for NOT filtering.
        :return: The QueryBuilder instance with NOT filters added.
        """
        not_conditions = [
            not_(getattr(self.model, field) == value)
            for field, value in conditions.items()
        ]
        self._filters.extend(not_conditions)
        return self

    def add_expression(self, expression: ClauseElement) -> "QueryBuilder":
        """
        Add a custom SQLAlchemy expression to the query.

        :param expression: A SQLAlchemy expression (e.g., comparison or complex condition).
        :return: The QueryBuilder instance with the custom expression applied.
        """
        self._expressions.append(expression)
        return self

    def select_columns(self, *columns: str) -> "QueryBuilder":
        """
        Select specific columns from the model.

        :param columns: Names of the columns to include in the result.
        :return: The QueryBuilder instance with selected columns applied.
        """
        self._selected_columns = [getattr(self.model, column) for column in columns]
        return self

    def count(self, column: Optional[str] = None) -> "QueryBuilder":
        """
        Apply a COUNT aggregation to the query.

        :param column: Optional column to count; if omitted, counts all rows.
        :return: The QueryBuilder instance with COUNT aggregation.
        """
        self._aggregate = (
            func.count(getattr(self.model, column)) if column else func.count()
        )
        return self

    def sum(self, column: str) -> "QueryBuilder":
        """
        Apply a SUM aggregation to the query.

        :param column: Column to sum.
        :return: The QueryBuilder instance with SUM aggregation.
        """
        self._aggregate = func.sum(getattr(self.model, column))
        return self

    def avg(self, column: str) -> "QueryBuilder":
        """
        Apply an AVG aggregation to the query.

        :param column: Column to average.
        :return: The QueryBuilder instance with AVG aggregation.
        """
        self._aggregate = func.avg(getattr(self.model, column))
        return self

    def max(self, column: str) -> "QueryBuilder":
        """
        Apply a MAX aggregation to the query.

        :param column: Column to find maximum value.
        :return: The QueryBuilder instance with MAX aggregation.
        """
        self._aggregate = func.max(getattr(self.model, column))
        return self

    def min(self, column: str) -> "QueryBuilder":
        """
        Apply a MIN aggregation to the query.

        :param column: Column to find minimum value.
        :return: The QueryBuilder instance with MIN aggregation.
        """
        self._aggregate = func.min(getattr(self.model, column))
        return self

    def limit(self, count: int) -> "QueryBuilder":
        """
        Limit the number of results.

        :param count: Maximum number of rows to retrieve.
        :return: The QueryBuilder instance with limit applied.
        """
        self._limit = count
        return self

    def offset(self, count: int) -> "QueryBuilder":
        """
        Offset the results for pagination.

        :param count: Number of rows to skip.
        :return: The QueryBuilder instance with offset applied.
        """
        self._offset = count
        return self

    def order_by(self, *fields: str) -> "QueryBuilder":
        """
        Apply ascending order to the results by specified fields.

        :param fields: Names of the columns to order by.
        :return: The QueryBuilder instance with ordering applied.
        """
        self._order_by.extend(getattr(self.model, field) for field in fields)
        self._desc_order = False
        return self

    def order_desc(self, *fields: str) -> "QueryBuilder":
        """
        Apply descending order to the results by specified fields.

        :param fields: Names of the columns to order by in descending order.
        :return: The QueryBuilder instance with descending order applied.
        """
        self._order_by.extend(getattr(self.model, field) for field in fields)
        self._desc_order = True
        return self

    def group_by(self, *columns: str) -> "QueryBuilder":
        """
        Group the results by specified columns.

        :param columns: Names of the columns to group by.
        :return: The QueryBuilder instance with grouping applied.
        """
        self._group_by = [getattr(self.model, column) for column in columns]
        return self

    def having(self, condition: ClauseElement) -> "QueryBuilder":
        """
        Apply a HAVING clause condition to the grouped results.

        :param condition: SQLAlchemy expression for the HAVING clause.
        :return: The QueryBuilder instance with HAVING condition applied.
        """
        self._having = condition
        return self

    def distinct(self) -> "QueryBuilder":
        """
        Ensure that results are distinct (no duplicates).

        :return: The QueryBuilder instance with DISTINCT applied.
        """
        self._distinct = True
        return self

    def reset(self) -> "QueryBuilder":
        """
        Reset all filters, expressions, and settings for reuse of the QueryBuilder instance.

        :return: The QueryBuilder instance, reset to its initial state.
        """
        self._filters = []
        self._expressions = []
        self._selected_columns = None
        self._aggregate = None
        self._limit = None
        self._offset = None
        self._order_by = []
        self._desc_order = False
        self._group_by = None
        self._having = None
        self._distinct = False
        return self

    def apply_to(
        self, query: Union[select, update, delete]
    ) -> Union[select, update, delete]:
        """
        Apply filters, expressions, limits, offsets, ordering, grouping, and aggregation to a query.

        :param query: A SQLAlchemy query (select, update, delete).
        :return: The SQLAlchemy query with applied conditions.
        """
        if isinstance(query, Select):
            if self._distinct:
                query = query.distinct()
            if self._aggregate:
                query = query.with_only_columns(self._aggregate)
            elif self._selected_columns:
                query = query.with_only_columns(self._selected_columns)
            else:
                query = query.with_only_columns(self.model)

            if self._group_by:
                query = query.group_by(*self._group_by)

            if self._having:
                query = query.having(self._having)

        for condition in self._filters:
            query = query.where(condition)

        for expression in self._expressions:
            query = query.where(expression)

        if self._limit is not None:
            query = query.limit(self._limit)

        if self._offset is not None:
            query = query.offset(self._offset)

        for order_field in self._order_by:
            query = query.order_by(
                order_field.desc() if self._desc_order else order_field
            )

        return query

    def to_sql(self, session: AsyncSession) -> str:
        """
        Get the raw SQL query string with parameters substituted.

        :param session: SQLAlchemy session to compile the query.
        :return: String representation of the SQL query.
        """
        query = self.apply_to(select(self.model))
        return str(query.compile(session.bind, compile_kwargs={"literal_binds": True}))
