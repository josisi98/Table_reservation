"""empty message

Revision ID: 01038cf599b3
Revises: 
Create Date: 2023-07-30 21:51:05.514686

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '01038cf599b3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('form_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('subject', sa.String(length=200), nullable=False),
    sa.Column('message', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reservation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nom', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('telephone', sa.String(length=20), nullable=False),
    sa.Column('date', sa.String(length=50), nullable=False),
    sa.Column('heure', sa.String(length=50), nullable=False),
    sa.Column('personnes', sa.Integer(), nullable=False),
    sa.Column('message', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('utilisateur',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('Nom', sa.String(length=40), nullable=False),
    sa.Column('prenom', sa.String(length=60), nullable=False),
    sa.Column('Nom_utilisateur', sa.String(length=60), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('mot_de_passe', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('Nom_utilisateur'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('utilisateur')
    op.drop_table('reservation')
    op.drop_table('form_data')
    # ### end Alembic commands ###