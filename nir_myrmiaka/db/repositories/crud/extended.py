from typing import List, Optional, Any, Dict, TypeVar
from nir_myrmiaka.db.repositories.crud import CRUDRepository
from nir_myrmiaka.db.repositories.crud.query_builder import QueryBuilder


T = TypeVar("T")


class ExtendedCRUDRepository(CRUDRepository[T]):
    """
    Extended CRUD Repository with shortcut methods for common queries and aggregations.

    This class provides additional utility methods for CRUD operations, including:
    - Finding entities with filters.
    - Performing aggregations like count, sum, average, etc.
    - Paginating and ordering results.
    - Creating entities if they don't exist.
    - Retrieving distinct values for columns.

    These methods extend the functionality of the basic `CRUDRepository` and simplify common operations.

    Methods:
        find_all(**filters) -> List[T]: Retrieve all entities matching specified filters.
        find_by_id(item_id: int) -> Optional[T]: Retrieve an entity by its ID.
        count_all() -> int: Count all entities in the model.
        count_by_filter(**filters) -> int: Count entities matching specific filters.
        sum_column(column: str, **filters) -> Optional[float]: Sum the values of a column with optional filters.
        find_with_pagination(page: int = 1, per_page: int = 10, **filters) -> List[T]: Paginate results with filters.
        find_with_ordering(order_by: str, descending: bool = False, **filters) -> List[T]: Order results by a column.
        find_distinct(column: str, **filters) -> List[T]: Retrieve distinct values for a specific column.
        aggregate(aggregation: str, column: str, **filters) -> Optional[float]: Perform aggregation on a column (e.g., sum, avg).
        exists(**filters) -> bool: Check if any entity exists that matches the filters.
        find_or_create(defaults: Optional[Dict[str, Any]] = None, **filters) -> T: Find or create an entity.
        find_one(**filters) -> Optional[T]: Retrieve a single entity matching the filters.
        get_max_value(column: str, **filters) -> Optional[Any]: Get the maximum value of a column.
        get_min_value(column: str, **filters) -> Optional[Any]: Get the minimum value of a column.
        update_by_filter(fields: Dict[str, Any], **filters) -> int: Update entities based on filters.
        delete_by_filter(**filters) -> int: Delete entities matching the filters.
        paginate_with_ordering(page: int = 1, per_page: int = 10, order_by: str = "", descending: bool = False, **filters) -> List[T]: Paginate and sort results.
        find_by_inclusion(column: str, values: List[Any], **filters) -> List[T]: Find entities with a column value in a list.
        get_avg_value(column: str, **filters) -> Optional[float]: Get the average value of a column.
        get_sum_value(column: str, **filters) -> Optional[float]: Get the sum of a column's values.
        find_or_create_multiple(entities: List[Dict[str, Any]], defaults: Optional[Dict[str, Any]] = None) -> List[T]: Find or create multiple entities.
        find_and_count(**filters) -> Dict[str, Any]: Retrieve entities and count in one operation.
        distinct_columns(columns: List[str], **filters) -> List[T]: Retrieve distinct values for multiple columns.
    """

    async def find_all(self, **filters) -> List[T]:
        """
        Retrieve all entities that match the specified filters using the `read` method.

        Args:
            **filters: Field-value pairs to filter the results by.

        Returns:
            List[T]: A list of entities that match the filters.
        """
        builder = QueryBuilder(self.model).filter_by(**filters)
        return await self.read(builder=builder)

    async def find_by_id(self, item_id: int) -> Optional[T]:
        """
        Retrieve an entity by its primary key ID using the `read` method.

        Args:
            item_id (int): The primary key ID of the entity.

        Returns:
            Optional[T]: The entity if found, otherwise `None`.
        """
        return await self.read(
            builder=QueryBuilder(self.model).filter_by(id=item_id), only_first=True
        )

    async def count_all(self) -> int:
        """
        Count all entities in the model using the `read` method with aggregation.

        Returns:
            int: The total count of entities in the model.
        """
        builder = QueryBuilder(self.model).count()
        result = await self.read(builder=builder, only_first=True)
        return result

    async def count_by_filter(self, **filters) -> int:
        """
        Count the number of entities that match specific filters.

        Args:
            **filters: Field-value pairs to filter the results by.

        Returns:
            int: The number of entities matching the filters.
        """
        builder = QueryBuilder(self.model).filter_by(**filters).count()
        result = await self.read(builder=builder, only_first=True)
        return result

    async def sum_column(self, column: str, **filters) -> Optional[float]:
        """
        Calculate the sum of a specific column with optional filters.

        Args:
            column (str): The column to calculate the sum for.
            **filters: Optional filters to apply when calculating the sum.

        Returns:
            Optional[float]: The sum of the column values, or `None` if no result.
        """
        builder = QueryBuilder(self.model).filter_by(**filters).sum(column)
        result = await self.read(builder=builder, only_first=True)
        return result

    async def find_with_pagination(
        self, page: int = 1, per_page: int = 10, **filters
    ) -> List[T]:
        """
        Retrieve paginated results with optional filters.

        Args:
            page (int): The page number to retrieve (default is 1).
            per_page (int): The number of results per page (default is 10).
            **filters: Optional filters to apply to the query.

        Returns:
            List[T]: A list of entities for the specified page.
        """
        offset = (page - 1) * per_page
        builder = (
            QueryBuilder(self.model).filter_by(**filters).limit(per_page).offset(offset)
        )
        return await self.read(builder=builder)

    async def find_with_ordering(
        self, order_by: str, descending: bool = False, **filters
    ) -> List[T]:
        """
        Retrieve results ordered by a specific column with optional filters.

        Args:
            order_by (str): The column to order by.
            descending (bool): Whether to order results in descending order (default is `False`).
            **filters: Optional filters to apply to the query.

        Returns:
            List[T]: A list of entities ordered by the specified column.
        """
        builder = QueryBuilder(self.model).filter_by(**filters)
        if descending:
            builder = builder.order_desc(order_by)
        else:
            builder = builder.order_by(order_by)
        return await self.read(builder=builder)

    async def find_distinct(self, column: str, **filters) -> List[T]:
        """
        Retrieve distinct values for a specific column with optional filters.

        Args:
            column (str): The column to retrieve distinct values for.
            **filters: Optional filters to apply to the query.

        Returns:
            List[T]: A list of distinct values for the specified column.
        """
        builder = (
            QueryBuilder(self.model)
            .filter_by(**filters)
            .distinct()
            .select_columns(column)
        )
        return await self.read(builder=builder)

    async def aggregate(
        self, aggregation: str, column: str, **filters
    ) -> Optional[float]:
        """
        Perform an aggregation (e.g., sum, avg, max, min, count) on a specific column.

        Args:
            aggregation (str): The aggregation to perform (e.g., "sum", "avg", "max", "min", "count").
            column (str): The column to perform the aggregation on.
            **filters: Optional filters to apply to the query.

        Returns:
            Optional[float]: The result of the aggregation, or `None` if no result.
        """
        builder = QueryBuilder(self.model).filter_by(**filters)
        if aggregation == "sum":
            builder = builder.sum(column)
        elif aggregation == "avg":
            builder = builder.avg(column)
        elif aggregation == "max":
            builder = builder.max(column)
        elif aggregation == "min":
            builder = builder.min(column)
        elif aggregation == "count":
            builder = builder.count(column)
        return await self.read(builder=builder, only_first=True)

    async def exists(self, **filters) -> bool:
        """
        Check if any entity exists that matches the specified filters.

        Args:
            **filters: Field-value pairs to filter the results by.

        Returns:
            bool: `True` if any entity matches the filters, `False` otherwise.
        """
        builder = QueryBuilder(self.model).filter_by(**filters).limit(1)
        result = await self.read(builder=builder, only_first=True)
        return result is not None

    async def find_or_create(
        self, defaults: Optional[Dict[str, Any]] = None, **filters
    ) -> T:
        """
        Retrieve an entity that matches the filters, or create a new one with defaults.

        Args:
            defaults (Optional[Dict[str, Any]]): Default values to use when creating a new entity (optional).
            **filters: Field-value pairs to filter the results by.

        Returns:
            T: The found or newly created entity.
        """
        entity = await self.find_one(**filters)
        if entity:
            return entity
        return await self.create(**{**filters, **(defaults or {})})

    async def find_one(self, **filters) -> Optional[T]:
        """
        Retrieve a single entity that matches the specified filters.

        Args:
            **filters: Field-value pairs to filter the results by.

        Returns:
            Optional[T]: The matching entity if found, otherwise `None`.
        """
        return await self.read(
            builder=QueryBuilder(self.model).filter_by(**filters), only_first=True
        )

    async def get_max_value(self, column: str, **filters) -> Optional[Any]:
        """
        Get the maximum value of a specified column with optional filters.

        Args:
            column (str): The column to retrieve the maximum value for.
            **filters: Optional filters to apply to the query.

        Returns:
            Optional[Any]: The maximum value of the column, or `None` if no result.
        """
        return await self.aggregate("max", column, **filters)

    async def get_min_value(self, column: str, **filters) -> Optional[Any]:
        """
        Get the minimum value of a specified column with optional filters.

        Args:
            column (str): The column to retrieve the minimum value for.
            **filters: Optional filters to apply to the query.

        Returns:
            Optional[Any]: The minimum value of the column, or `None` if no result.
        """
        return await self.aggregate("min", column, **filters)

    async def update_by_filter(self, fields: Dict[str, Any], **filters) -> int:
        """
        Update entities that match the filters.

        Args:
            fields (Dict[str, Any]): The fields to update.
            **filters: Field-value pairs to filter the results by.

        Returns:
            int: The number of entities updated.
        """
        builder = QueryBuilder(self.model).filter_by(**filters)
        return await self.update(builder=builder, **fields)

    async def delete_by_filter(self, **filters) -> int:
        """
        Delete entities that match the filters.

        Args:
            **filters: Field-value pairs to filter the results by.

        Returns:
            int: The number of entities deleted.
        """
        builder = QueryBuilder(self.model).filter_by(**filters)
        return await self.delete(builder=builder)

    async def paginate_with_ordering(
        self,
        page: int = 1,
        per_page: int = 10,
        order_by: str = "",
        descending: bool = False,
        **filters
    ) -> List[T]:
        """
        Retrieve paginated and sorted results.

        Args:
            page (int): The page number to retrieve (default is 1).
            per_page (int): The number of results per page (default is 10).
            order_by (str): The column to order by.
            descending (bool): Whether to order results in descending order (default is `False`).
            **filters: Optional filters to apply to the query.

        Returns:
            List[T]: A list of entities for the specified page.
        """
        offset = (page - 1) * per_page
        builder = (
            QueryBuilder(self.model).filter_by(**filters).limit(per_page).offset(offset)
        )
        if order_by:
            if descending:
                builder = builder.order_desc(order_by)
            else:
                builder = builder.order_by(order_by)
        return await self.read(builder=builder)

    async def find_by_inclusion(
        self, column: str, values: List[Any], **filters
    ) -> List[T]:
        """
        Find entities where a column's value is in the provided list.

        Args:
            column (str): The column to check for inclusion.
            values (List[Any]): The list of values to include.
            **filters: Optional filters to apply to the query.

        Returns:
            List[T]: A list of entities where the column value is in the specified list.
        """
        builder = (
            QueryBuilder(self.model)
            .filter_by(**filters)
            .add_expression(getattr(self.model, column).in_(values))
        )
        return await self.read(builder=builder)

    async def get_avg_value(self, column: str, **filters) -> Optional[float]:
        """
        Get the average value of a specific column with optional filters.

        Args:
            column (str): The column to retrieve the average value for.
            **filters: Optional filters to apply to the query.

        Returns:
            Optional[float]: The average value of the column, or `None` if no result.
        """
        builder = QueryBuilder(self.model).filter_by(**filters).avg(column)
        result = await self.read(builder=builder, only_first=True)
        return result

    async def get_sum_value(self, column: str, **filters) -> Optional[float]:
        """
        Get the sum of a specific column with optional filters.

        Args:
            column (str): The column to retrieve the sum for.
            **filters: Optional filters to apply to the query.

        Returns:
            Optional[float]: The sum of the column values, or `None` if no result.
        """
        builder = QueryBuilder(self.model).filter_by(**filters).sum(column)
        result = await self.read(builder=builder, only_first=True)
        return result

    async def find_or_create_multiple(
        self, entities: List[Dict[str, Any]], defaults: Optional[Dict[str, Any]] = None
    ) -> List[T]:
        """
        Try to find multiple entities based on filters; if not found, create them.

        Args:
            entities (List[Dict[str, Any]]): The list of entities to search for or create.
            defaults (Optional[Dict[str, Any]]): Default values to apply when creating new entities.

        Returns:
            List[T]: The list of found or newly created entities.
        """
        created_entities = []
        for entity in entities:
            existing = await self.find_one(**entity)
            if not existing:
                created_entities.append(
                    await self.create(**{**entity, **(defaults or {})})
                )
            else:
                created_entities.append(existing)
        return created_entities

    async def find_and_count(self, **filters) -> Dict[str, Any]:
        """
        Retrieve entities and count in one operation.

        Args:
            **filters: Field-value pairs to filter the results by.

        Returns:
            Dict[str, Any]: A dictionary containing the `entities` (list of entities) and the `count` (total number of entities matching filters).
        """
        builder = QueryBuilder(self.model).filter_by(**filters)
        entities = await self.read(builder=builder)
        count = await self.count_by_filter(**filters)
        return {"entities": entities, "count": count}

    async def distinct_columns(self, columns: List[str], **filters) -> List[T]:
        """
        Retrieve distinct values for multiple columns.

        Args:
            columns (List[str]): The list of columns to retrieve distinct values for.
            **filters: Optional filters to apply to the query.

        Returns:
            List[T]: A list of distinct values for the specified columns.
        """
        builder = (
            QueryBuilder(self.model)
            .filter_by(**filters)
            .distinct()
            .select_columns(*columns)
        )
        return await self.read(builder=builder)
