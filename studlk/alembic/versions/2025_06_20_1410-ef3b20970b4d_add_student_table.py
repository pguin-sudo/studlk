"""Add student table

Revision ID: ef3b20970b4d
Revises: 4a0bed8bbb1a
Create Date: 2025-06-20 14:10:45.746944

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "ef3b20970b4d"
down_revision: Union[str, Sequence[str], None] = "4a0bed8bbb1a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "student",
        sa.Column("uuid", sa.UUID(), nullable=False, comment="UUID PK"),
        sa.Column(
            "first_name", sa.String(length=64), nullable=False, comment="Имя студента"
        ),
        sa.Column(
            "last_name",
            sa.String(length=64),
            nullable=False,
            comment="Фамилия студента",
        ),
        sa.Column("birth_date", sa.Date(), nullable=False, comment="Дата рождения"),
        sa.Column(
            "status",
            sa.Enum(
                "ACTIVE",
                "ACADEMIC_LEAVE",
                "EXPELLED",
                "GRADUATED",
                "TRANSFERRED",
                name="studentstatus",
            ),
            nullable=False,
            comment="Статус студента",
        ),
        sa.Column(
            "contact_phone",
            sa.String(length=11),
            nullable=True,
            comment="Контактный телефон",
        ),
        sa.Column(
            "email", sa.String(length=50), nullable=True, comment="Электронная почта"
        ),
        sa.Column(
            "address", sa.String(length=128), nullable=True, comment="Адрес проживания"
        ),
        sa.Column(
            "scholarship", sa.Boolean(), nullable=False, comment="Получает стипендию"
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            comment="Record creation timestamp",
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=True,
            comment="Record update timestamp",
        ),
        sa.PrimaryKeyConstraint("uuid"),
        comment="Таблица студентов.",
    )
    op.create_index(
        op.f("ix_student_birth_date"), "student", ["birth_date"], unique=False
    )
    op.create_index(
        op.f("ix_student_contact_phone"), "student", ["contact_phone"], unique=False
    )
    op.create_index(op.f("ix_student_email"), "student", ["email"], unique=True)
    op.create_index(op.f("ix_student_status"), "student", ["status"], unique=False)
    op.create_index(op.f("ix_student_uuid"), "student", ["uuid"], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_student_uuid"), table_name="student")
    op.drop_index(op.f("ix_student_status"), table_name="student")
    op.drop_index(op.f("ix_student_email"), table_name="student")
    op.drop_index(op.f("ix_student_contact_phone"), table_name="student")
    op.drop_index(op.f("ix_student_birth_date"), table_name="student")
    op.drop_table("student")
    # ### end Alembic commands ###

    # Удаляем Enum studentstatus для успешной миграции
    conn = op.get_bind()
    conn.execute(sa.text("DROP TYPE IF EXISTS studentstatus"))
