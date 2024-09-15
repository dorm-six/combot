"""initial revision

Revision ID: 3c5a2012ecae
Revises: 
Create Date: 2024-09-15 14:55:56.116686

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3c5a2012ecae"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "bot_chat_info",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("handle", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "bot_command_info",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("chat_id", sa.BigInteger(), nullable=True),
        sa.Column("from_id", sa.BigInteger(), nullable=True),
        sa.Column("command_msg_id", sa.BigInteger(), nullable=True),
        sa.Column("response_msg_id", sa.BigInteger(), nullable=True),
        sa.Column("answered", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("chat_id", "command_msg_id"),
        sa.UniqueConstraint("chat_id", "response_msg_id"),
    )
    op.create_table(
        "bot_media_group_message",
        sa.Column("chat_id", sa.BigInteger(), nullable=False),
        sa.Column("media_group_id", sa.String(length=255), nullable=False),
        sa.Column("msg_id", sa.BigInteger(), nullable=False),
        sa.Column("caption", sa.Text(), nullable=True),
        sa.Column("finalized", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("chat_id", "media_group_id", "msg_id"),
    )
    op.create_index(
        "ix_bot_mgm__finalized",
        "bot_media_group_message",
        ["chat_id", "media_group_id", "finalized"],
        unique=False,
    )
    op.create_table(
        "bot_pinned_msg",
        sa.Column("chat_id", sa.BigInteger(), nullable=False),
        sa.Column("message_id", sa.BigInteger(), nullable=False),
        sa.Column("pin_id", sa.String(), nullable=True),
        sa.Column("pinned", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("chat_id", "message_id"),
    )
    op.create_index(
        "ix_bot_pinned_msg__pined",
        "bot_pinned_msg",
        ["chat_id", "pin_id", "pinned"],
        unique=False,
    )
    op.create_index(
        op.f("ix_bot_pinned_msg_pin_id"), "bot_pinned_msg", ["pin_id"], unique=False
    )
    op.create_table(
        "bot_user_info",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=True),
        sa.Column("username", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "feed_forward_chat_feed",
        sa.Column("chat_id", sa.BigInteger(), nullable=False),
        sa.Column("feed_channel_id", sa.BigInteger(), nullable=False),
        sa.PrimaryKeyConstraint("chat_id", "feed_channel_id"),
    )
    op.create_index(
        op.f("ix_feed_forward_chat_feed_chat_id"),
        "feed_forward_chat_feed",
        ["chat_id"],
        unique=False,
    )
    op.create_table(
        "feed_forward_message_forwarded",
        sa.Column("chat_id", sa.BigInteger(), nullable=False),
        sa.Column("message_id", sa.BigInteger(), nullable=False),
        sa.PrimaryKeyConstraint("chat_id", "message_id"),
    )
    op.create_table(
        "xp_chat_jackpot_prob",
        sa.Column("chat_id", sa.BigInteger(), nullable=False),
        sa.Column("jackpot_prob", sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint("chat_id"),
    )
    op.create_table(
        "xp_table",
        sa.Column("chat_id", sa.BigInteger(), nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("last_user_name", sa.String(length=511), nullable=True),
        sa.Column("experience", sa.BigInteger(), nullable=True),
        sa.Column("last_exp_update", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("chat_id", "user_id"),
    )
    op.create_index(op.f("ix_xp_table_chat_id"), "xp_table", ["chat_id"], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_xp_table_chat_id"), table_name="xp_table")
    op.drop_table("xp_table")
    op.drop_table("xp_chat_jackpot_prob")
    op.drop_table("feed_forward_message_forwarded")
    op.drop_index(
        op.f("ix_feed_forward_chat_feed_chat_id"), table_name="feed_forward_chat_feed"
    )
    op.drop_table("feed_forward_chat_feed")
    op.drop_table("bot_user_info")
    op.drop_index(op.f("ix_bot_pinned_msg_pin_id"), table_name="bot_pinned_msg")
    op.drop_index("ix_bot_pinned_msg__pined", table_name="bot_pinned_msg")
    op.drop_table("bot_pinned_msg")
    op.drop_index("ix_bot_mgm__finalized", table_name="bot_media_group_message")
    op.drop_table("bot_media_group_message")
    op.drop_table("bot_command_info")
    op.drop_table("bot_chat_info")
    # ### end Alembic commands ###