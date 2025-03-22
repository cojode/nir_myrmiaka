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
    op.execute("""
        INSERT INTO base_researchwork (id, name, description)
        VALUES (1, 'Research on AI', 'A comprehensive study on artificial intelligence.');
    """)
    op.execute("""
        INSERT INTO base_researchwork (id, name, description)
        VALUES (2, 'Climate Change', 'Analyzing the impact of climate change on ecosystems.');
    """)
    op.execute("""
        INSERT INTO base_researchwork (id, name, description)
        VALUES (3, 'Quantum Computing', 'Exploring the potential of quantum computing.');
    """)

    # Insert static data into the base_topic table
    op.execute("""
        INSERT INTO base_topic (id, name, research_work_id)
        VALUES (1, 'Machine Learning', 1);
    """)
    op.execute("""
        INSERT INTO base_topic (id, name, research_work_id)
        VALUES (2, 'Natural Language Processing', 1);
    """)
    op.execute("""
        INSERT INTO base_topic (id, name, research_work_id)
        VALUES (3, 'Renewable Energy', 2);
    """)
    op.execute("""
        INSERT INTO base_topic (id, name, research_work_id)
        VALUES (4, 'Carbon Footprint', 2);
    """)
    op.execute("""
        INSERT INTO base_topic (id, name, research_work_id)
        VALUES (5, 'Qubits', 3);
    """)
    op.execute("""
        INSERT INTO base_topic (id, name, research_work_id)
        VALUES (6, 'Quantum Algorithms', 3);
    """)


def downgrade():
    # Remove the static data
    op.execute("DELETE FROM users_group WHERE id IN (1, 2, 3);")
    op.execute("DELETE FROM base_researchwork WHERE id IN (1, 2, 3);")
    op.execute("DELETE FROM base_topic WHERE id IN (1, 2, 3, 4, 5, 6);")