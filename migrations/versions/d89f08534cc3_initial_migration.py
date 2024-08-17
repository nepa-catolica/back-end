"""Initial migration.

Revision ID: d89f08534cc3
Revises: 
Create Date: 2024-07-17 10:39:54.112781

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd89f08534cc3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('permissao', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('aluno',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=255), nullable=False),
    sa.Column('matricula', sa.Integer(), nullable=False),
    sa.Column('curso', sa.String(length=255), nullable=False),
    sa.Column('data_ingresso', sa.DateTime(), nullable=False),
    sa.Column('telefone', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('permissao', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('matricula'),
    sa.UniqueConstraint('nome'),
    sa.UniqueConstraint('telefone')
    )
    op.create_table('professor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=255), nullable=False),
    sa.Column('matricula', sa.Integer(), nullable=False),
    sa.Column('curso', sa.String(length=255), nullable=False),
    sa.Column('telefone', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('aprovado', sa.Boolean(), nullable=False),
    sa.Column('permissao', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('matricula'),
    sa.UniqueConstraint('telefone')
    )
    op.create_table('edital',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=255), nullable=False),
    sa.Column('descricao', sa.String(length=255), nullable=False),
    sa.Column('data_criacao', sa.DateTime(), nullable=False),
    sa.Column('admin_id', sa.Integer(), nullable=False),
    sa.Column('edital_pdf', sa.String(length=255), nullable=False),
    sa.ForeignKeyConstraint(['admin_id'], ['admin.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('projeto',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=255), nullable=False),
    sa.Column('descricao', sa.String(length=255), nullable=False),
    sa.Column('data_criacao', sa.DateTime(), nullable=False),
    sa.Column('professor_id', sa.Integer(), nullable=False),
    sa.Column('aprovado', sa.Boolean(), nullable=False),
    sa.Column('edital_pdf', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['professor_id'], ['professor.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('aluno_projeto',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('aluno_id', sa.Integer(), nullable=False),
    sa.Column('projeto_id', sa.Integer(), nullable=False),
    sa.Column('aprovado', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['aluno_id'], ['aluno.id'], ),
    sa.ForeignKeyConstraint(['projeto_id'], ['projeto.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('aluno_projeto')
    op.drop_table('projeto')
    op.drop_table('edital')
    op.drop_table('professor')
    op.drop_table('aluno')
    op.drop_table('admin')
    # ### end Alembic commands ###