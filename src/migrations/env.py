import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from src.core.database import Base
from src.app.services.user.models import UserModel
from src.app.services.mailing.models import MailingModel
from src.app.services.message.models import MessageModel

config = context.config
fileConfig(config.config_file_name)

target_metadata = Base.metadata

server = os.getenv("POSTGRES_SERVER")
password = os.getenv("POSTGRES_PASSWORD")
user = os.getenv("POSTGRES_USER")
db = os.getenv("POSTGRES_DB")

if os.getenv("IS_IN_DOCKER", False):
    server = server
else:
    server = "localhost:5432"

config.set_main_option("sqlalchemy.url", f"postgresql://{user}:{password}@"
                                         f"{server}/{db}")


def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
