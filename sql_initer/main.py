from sqlalchemy import Engine, create_engine, text
from sqlalchemy.engine import URL, Connection

from config import Config


def create_user(conn: Connection, username: str, password: str):
    """Создать пользователя, если он не существует."""
    user_exists_query = text(
        "SELECT 1 FROM pg_catalog.pg_user WHERE usename = :username"
    )
    create_user_query = text(f"CREATE USER {username} WITH PASSWORD :password")
    if not conn.execute(user_exists_query, {"username": username}).fetchone():
        _ = conn.execute(
            create_user_query,
            {"password": password},
        )
        print(f"Пользователь '{username}' создан.")
    else:
        print(f"Пользователь '{username}' уже существует.")


def create_database(conn: Connection, db_name: str, db_owner: str):
    """Создать базу данных, если она не существует."""
    db_exists_query = text("SELECT 1 FROM pg_database WHERE datname = :db_name")
    create_db_query = text(f"CREATE DATABASE {db_name} OWNER {db_owner}")
    if not conn.execute(db_exists_query, {"db_name": db_name}).fetchone():
        _ = conn.execute(create_db_query)
        print(f"База данных '{db_name}' создана.")
    else:
        print(f"База данных '{db_name}' уже существует.")


def main():
    config = Config()  ## pyright: ignore[reportCallIssue]
    print(config.model_dump_json(indent=2))

    connect_config = config.connect_config
    url = URL.create(
        drivername=f"postgresql+{connect_config.dialect}",
        username=connect_config.db_user,
        password=connect_config.db_password.get_secret_value(),
        host=connect_config.db_host,
        port=connect_config.db_port,
        database=connect_config.db_name,
    )
    engine: Engine = create_engine(
        url=url,
        echo=config.connect_config.sql_command_echo,
    )

    with engine.connect() as conn:
        _ = conn.execution_options(isolation_level="AUTOCOMMIT")

        for project_conf in config.db_projects_configs:
            create_user(
                conn=conn,
                username=project_conf.username,
                password=project_conf.password.get_secret_value(),
            )
            create_database(
                conn=conn,
                db_name=project_conf.database_name,
                db_owner=project_conf.username,
            )

    print("Инициализация завершена.")


if __name__ == "__main__":
    main()
