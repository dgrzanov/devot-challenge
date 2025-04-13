from sqlmodel import Session, create_engine, func, select

from config import settings

from auth.auth_models import User
from categories.categories_models import Category

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI), echo=True)


def init_db(session: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next lines
    from sqlmodel import SQLModel

    # This works because the models are already imported and registered from app.models
    SQLModel.metadata.create_all(engine)

    # Create initial data
    count_categories = session.exec(select(func.count()).select_from(Category)).one()
    if count_categories == 0:
        session.add_all(
            [
                Category(name="Food"),
                Category(name="Transport"),
                Category(name="Entertainment"),
                Category(name="Health"),
                Category(name="Education"),
                Category(name="Housing"),
                Category(name="Clothing"),
                Category(name="Utilities"),
                Category(name="Insurance"),
                Category(name="Miscellaneous"),
            ]
        )
        session.commit()
