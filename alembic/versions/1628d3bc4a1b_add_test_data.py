"""add_test_data

Revision ID: 1628d3bc4a1b
Revises: f10b2c67d183
Create Date: 2025-03-22 13:08:21.577802

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1628d3bc4a1b'
down_revision: Union[str, None] = 'f10b2c67d183'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # Insert static data into the users_group table
    op.execute("INSERT INTO users_group (id, group_name) VALUES (1, 'test_group_1');")
    op.execute("INSERT INTO users_group (id, group_name) VALUES (2, 'test_group_2');")
    op.execute("INSERT INTO users_group (id, group_name) VALUES (3, 'test_group_3');")

    # Insert static data into the base_researchwork table
    op.execute(
        """
        INSERT INTO base_researchwork (id, name, description)
        VALUES (1, 'Диплом', 'Пишется на 8 семестре');
    """
    )
    op.execute(
        """
        INSERT INTO base_researchwork (id, name, description)
        VALUES (2, 'НИР', 'Пишется на протяжении 6-7 семестров');
    """
    )
    op.execute(
        """
        INSERT INTO base_researchwork (id, name, description)
        VALUES (3, 'УИР', 'Пишется на 5 семестре');
    """
    )
    op.execute(
        """
        INSERT INTO base_researchwork (id, name, description)
        VALUES (4, 'Зимняя практика', 'Пишется на 5 семестре');
    """
    )
    op.execute(
        """
        INSERT INTO base_researchwork (id, name, description)
        VALUES (5, 'Летняя практика', 'Пишется на 7 семестре');
    """
    )

    # Insert static data into the base_topic table
    op.execute(
        """
        INSERT INTO base_topic (id, name, research_work_id)
        VALUES (1, 'Задание', 1);
    """
    )
    op.execute(
        """
        INSERT INTO base_topic (id, name, research_work_id)
        VALUES (2, 'Расширенное содержание пояснительной записки', 1);
    """
    )
    op.execute(
        """
        INSERT INTO base_topic (id, name, research_work_id)
        VALUES (3, 'Пояснительная записка', 1);
    """
    )
    op.execute(
        """
        INSERT INTO base_topic (id, name, research_work_id)
        VALUES (4, 'Презентация', 1);
    """
    )
    op.execute(
        """
        INSERT INTO base_topic (id, name, research_work_id)
        VALUES (5, 'Задание', 2);
    """
    )
    op.execute(
        """
        INSERT INTO base_topic (id, name, research_work_id)
        VALUES (6, 'Расширенное содержание пояснительной записки', 2);
    """
    )
    op.execute(
        """
        INSERT INTO base_topic (id, name, research_work_id)
        VALUES (7, 'Пояснительная записка', 2);
    """
    )
    op.execute(
        """
        INSERT INTO base_topic (id, name, research_work_id)
        VALUES (8, 'Презентация', 2);
    """
    )
    op.execute(
        """
        INSERT INTO base_topic (id, name, research_work_id)
        VALUES (9, 'Задание', 3);
    """
    )
    op.execute(
        """
        INSERT INTO base_topic (id, name, research_work_id)
        VALUES (10, 'Расширенное содержание пояснительной записки', 3);
    """
    )
    op.execute(
        """
        INSERT INTO base_topic (id, name, research_work_id)
        VALUES (11, 'Пояснительная записка', 3);
    """
    )
    op.execute(
        """
        INSERT INTO base_topic (id, name, research_work_id)
        VALUES (12, 'Презентация', 3);
    """
    )
    op.execute(
        """
        INSERT INTO base_topic (id, name, research_work_id)
        VALUES (13, 'Задание', 4);
    """
    )
    op.execute(
        """
        INSERT INTO base_topic (id, name, research_work_id)
        VALUES (14, 'Расширенное содержание пояснительной записки', 4);
    """
    )
    op.execute(
        """
        INSERT INTO base_topic (id, name, research_work_id)
        VALUES (15, 'Пояснительная записка', 4);
    """
    )
    op.execute(
        """
        INSERT INTO base_topic (id, name, research_work_id)
        VALUES (16, 'Презентация', 4);
    """
    )
    op.execute(
        """
        INSERT INTO base_topic (id, name, research_work_id)
        VALUES (17, 'Дневник', 4);
    """
    )
    op.execute(
        """
        INSERT INTO base_topic (id, name, research_work_id)
        VALUES (18, 'Задание', 5);
    """
    )
    op.execute(
        """
        INSERT INTO base_topic (id, name, research_work_id)
        VALUES (19, 'Расширенное содержание пояснительной записки', 5);
    """
    )
    op.execute(
        """
        INSERT INTO base_topic (id, name, research_work_id)
        VALUES (20, 'Пояснительная записка', 5);
    """
    )
    op.execute(
        """
        INSERT INTO base_topic (id, name, research_work_id)
        VALUES (21, 'Презентация', 5);
    """
    )
    op.execute(
        """
        INSERT INTO base_topic (id, name, research_work_id)
        VALUES (22, 'Дневник', 5);
    """
    )

def downgrade():
    # Remove the static data
    op.execute("DELETE FROM users_group WHERE id IN (1, 2, 3);")
    op.execute("DELETE FROM base_researchwork WHERE id IN (1, 2, 3, 4, 5);")
    op.execute(
        "DELETE FROM base_topic WHERE id IN (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22);"
    )
