"""empty message

Revision ID: 654c984ce579
Revises: 35160eba026e
Create Date: 2019-04-08 19:46:29.480277

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '654c984ce579'
down_revision = '35160eba026e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('events_eventgroup',
    sa.Column('event_id', sa.Integer(), nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['event_id'], ['events_event.id'], ),
    sa.ForeignKeyConstraint(['group_id'], ['groups_group.id'], ),
    sa.PrimaryKeyConstraint('event_id', 'group_id')
    )
    op.drop_constraint('images_image_path_key', 'images_image', type_='unique')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('images_image_path_key', 'images_image', ['path'])
    op.drop_table('events_eventgroup')
    # ### end Alembic commands ###