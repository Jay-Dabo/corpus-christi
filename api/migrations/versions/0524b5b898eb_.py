"""empty message

Revision ID: 0524b5b898eb
Revises: 
Create Date: 2019-01-15 13:33:32.973273

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0524b5b898eb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('events_teams',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('groups_group',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('i18n_key',
    sa.Column('id', sa.String(length=32), nullable=False),
    sa.Column('desc', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('i18n_locale',
    sa.Column('code', sa.String(length=5), nullable=False),
    sa.Column('desc', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('code')
    )
    op.create_table('people_attributes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name_i18n', sa.String(length=5), nullable=True),
    sa.Column('type_i18n', sa.String(length=5), nullable=True),
    sa.Column('seq', sa.Integer(), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('people_role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name_i18n', sa.String(length=5), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('i18n_language',
    sa.Column('code', sa.String(length=2), nullable=False),
    sa.Column('name_i18n', sa.String(length=32), nullable=False),
    sa.ForeignKeyConstraint(['name_i18n'], ['i18n_key.id'], ),
    sa.PrimaryKeyConstraint('code')
    )
    op.create_table('i18n_value',
    sa.Column('key_id', sa.String(length=32), nullable=False),
    sa.Column('locale_code', sa.String(length=5), nullable=False),
    sa.Column('gloss', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['key_id'], ['i18n_key.id'], ),
    sa.ForeignKeyConstraint(['locale_code'], ['i18n_locale.code'], ),
    sa.PrimaryKeyConstraint('key_id', 'locale_code')
    )
    op.create_table('people_enumerated_value',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('attribute_id', sa.Integer(), nullable=True),
    sa.Column('value_i18n', sa.String(length=5), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['attribute_id'], ['people_attributes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('places_country',
    sa.Column('code', sa.String(length=2), nullable=False),
    sa.Column('name_i18n', sa.String(length=32), nullable=False),
    sa.ForeignKeyConstraint(['name_i18n'], ['i18n_key.id'], ),
    sa.PrimaryKeyConstraint('code')
    )
    op.create_table('places_area',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('country_code', sa.String(length=2), nullable=False),
    sa.ForeignKeyConstraint(['country_code'], ['places_country.code'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('places_address',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('address', sa.String(length=255), nullable=False),
    sa.Column('city', sa.String(length=64), nullable=False),
    sa.Column('area_id', sa.Integer(), nullable=False),
    sa.Column('country_code', sa.String(length=16), nullable=False),
    sa.Column('latitude', sa.Float(), nullable=True),
    sa.Column('longitude', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['area_id'], ['places_area.id'], ),
    sa.ForeignKeyConstraint(['country_code'], ['places_country.code'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('places_location',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=64), nullable=True),
    sa.Column('address_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['address_id'], ['places_address.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('events_asset',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.Column('location_id', sa.Integer(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['location_id'], ['places_location.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('events_event',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('start', sa.DateTime(), nullable=False),
    sa.Column('end', sa.DateTime(), nullable=False),
    sa.Column('location_id', sa.Integer(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['location_id'], ['places_location.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('groups_meeting',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('when', sa.DateTime(), nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=False),
    sa.Column('location_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['groups_group.id'], ),
    sa.ForeignKeyConstraint(['location_id'], ['places_location.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('people_person',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=64), nullable=False),
    sa.Column('last_name', sa.String(length=64), nullable=False),
    sa.Column('second_last_name', sa.String(length=64), nullable=True),
    sa.Column('gender', sa.String(length=1), nullable=True),
    sa.Column('birthday', sa.Date(), nullable=True),
    sa.Column('phone', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.Column('location_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['location_id'], ['places_location.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('groups_member',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('joined', sa.Date(), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=False),
    sa.Column('person_id', sa.Integer(), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['groups_group.id'], ),
    sa.ForeignKeyConstraint(['person_id'], ['people_person.id'], ),
    sa.ForeignKeyConstraint(['role_id'], ['people_role.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('people_account',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.Column('person_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['person_id'], ['people_person.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('people_person_attributes',
    sa.Column('person_id', sa.Integer(), nullable=False),
    sa.Column('attribute_id', sa.Integer(), nullable=False),
    sa.Column('enum_value_id', sa.Integer(), nullable=True),
    sa.Column('string_value', sa.String(length=5), nullable=True),
    sa.ForeignKeyConstraint(['attribute_id'], ['people_attributes.id'], ),
    sa.ForeignKeyConstraint(['enum_value_id'], ['people_enumerated_value.id'], ),
    sa.ForeignKeyConstraint(['person_id'], ['people_person.id'], ),
    sa.PrimaryKeyConstraint('person_id', 'attribute_id')
    )
    op.create_table('account_role',
    sa.Column('people_account_id', sa.Integer(), nullable=False),
    sa.Column('people_role_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['people_account_id'], ['people_account.id'], ),
    sa.ForeignKeyConstraint(['people_role_id'], ['people_role.id'], ),
    sa.PrimaryKeyConstraint('people_account_id', 'people_role_id')
    )
    op.create_table('groups_attendance',
    sa.Column('meeting_id', sa.Integer(), nullable=False),
    sa.Column('member_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['meeting_id'], ['groups_meeting.id'], ),
    sa.ForeignKeyConstraint(['member_id'], ['groups_member.id'], ),
    sa.PrimaryKeyConstraint('meeting_id', 'member_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('groups_attendance')
    op.drop_table('account_role')
    op.drop_table('people_person_attributes')
    op.drop_table('people_account')
    op.drop_table('groups_member')
    op.drop_table('people_person')
    op.drop_table('groups_meeting')
    op.drop_table('events_event')
    op.drop_table('events_asset')
    op.drop_table('places_location')
    op.drop_table('places_address')
    op.drop_table('places_area')
    op.drop_table('places_country')
    op.drop_table('people_enumerated_value')
    op.drop_table('i18n_value')
    op.drop_table('i18n_language')
    op.drop_table('people_role')
    op.drop_table('people_attributes')
    op.drop_table('i18n_locale')
    op.drop_table('i18n_key')
    op.drop_table('groups_group')
    op.drop_table('events_teams')
    # ### end Alembic commands ###
