"""Better agent config control

Revision ID: 09ac195ca9c7
Revises: 690687d71334
Create Date: 2019-04-16 02:00:52.988269

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "09ac195ca9c7"
down_revision = "690687d71334"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    agent_script_table = op.create_table(
        "agent_script",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.bulk_insert(agent_script_table, [{"id": 1, "name": "default"}])

    op.create_index(op.f("ix_agent_script_name"), "agent_script", ["name"], unique=True)
    op.add_column("agent_config", sa.Column("hostTimeout", sa.Integer(), nullable=True))
    op.add_column("agent_config", sa.Column("noPing", sa.Boolean(), nullable=True))
    op.add_column("agent_config", sa.Column("osScanLimit", sa.Boolean(), nullable=True))
    op.add_column(
        "agent_config", sa.Column("scriptTimeout", sa.Integer(), nullable=True)
    )
    with op.batch_alter_table("agent_config", recreate="always") as bop:
        bop.alter_column(
            column_name="defaultScripts",
            new_column_name="enableScripts",
            existing_type=sa.Boolean,
        )

    newColumns = {
        "hostTimeout": 600,
        "noPing": False,
        "osScanLimit": False,
        "scriptTimeout": 60,
    }
    for col_name, col_def in newColumns.items():
        new_col = sa.table("agent_config", sa.Column(col_name))
        op.execute(new_col.update().values(**{col_name: col_def}))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("agent_config") as bop:
        bop.alter_column(
            "enableScripts", new_column_name="defaultScripts", existing_type=sa.Boolean
        )
        bop.drop_column("scriptTimeout")
        bop.drop_column("osScanLimit")
        bop.drop_column("noPing")
        bop.drop_column("hostTimeout")
    op.drop_index(op.f("ix_agent_script_name"), table_name="agent_script")
    op.drop_table("agent_script")
    # ### end Alembic commands ###
