from sqlmodel import SQLModel, create_engine, Session
from src.conf.db.settings import settings

class Database:
    _engine = None

    @classmethod
    def get_engine(cls):
        if cls._engine is None:
            # On utilise PyMySQL comme driver MySQL
            cls._engine = create_engine(
                f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}" +
                f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}",
                echo=True
            )
        return cls._engine

    @classmethod
    def get_session(cls):
        engine = cls.get_engine()
        with Session(engine) as session:
            yield session

    @classmethod
    def init_db(cls):
        engine = cls.get_engine()
        SQLModel.metadata.create_all(engine)

    
    @classmethod
    def recreate_db(cls):
        """
        SUPPRIME et RECRÉE toutes les tables (DANGEREUX en production)
        """
        engine = cls.get_engine()

        # Supprimer toutes les tables
        SQLModel.metadata.drop_all(engine)

        # Recréer toutes les tables
        SQLModel.metadata.create_all(engine)
