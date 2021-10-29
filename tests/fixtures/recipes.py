from model_bakery.recipe import foreign_key

from .bases import Recipe
from .enums import BOOK_GENRES, BOOKS, USERS


def set_user_password(instances, recipe):
    for instance in instances:
        instance.set_password(recipe.attr_mapping["password"])
        instance.save()


BOOK_GENRE_RECIPES = {
    BOOK_GENRES.ROMMAN: Recipe(
        "core.BookGenre",
        # kwargs
        name="Romman",
    ),
    BOOK_GENRES.THRILLER: Recipe(
        "core.BookGenre",
        # kwargs
        name="Thriller",
    ),
    BOOK_GENRES.HORROR: Recipe(
        "core.BookGenre",
        # kwargs
        name="HORROR",
    ),
}


USER_RECIPES = {
    USERS.A: Recipe(
        "backend_auth.BackendUser",
        # kwargs
        username="A",
        email="A@email.com",
        password="pwd123Q!",
    ),
    USERS.B: Recipe(
        "backend_auth.BackendUser",
        # kwargs
        username="B",
        email="B@email.com",
        password="pwd123Q!",
    ),
    USERS.ADMIN_A: Recipe(
        "backend_auth.BackendUser",
        # kwargs
        username="ADMIN_A",
        email="ADMIN_A@email.com",
        password="pwd123Q!",
        is_staff=True,
    ),
}

BOOK_RECIPES = {
    BOOKS.A: Recipe(
        "core.Book",
        _quantity=15,
        # kwargs
        name="book1",
        writer=foreign_key(USER_RECIPES[USERS.A]),
        genre=foreign_key(BOOK_GENRE_RECIPES[BOOK_GENRES.THRILLER]),
        synopsis="this is synop1",
        price=300.0,
        release_date="2021-10-29T12:30:58.831431Z",
    ),
    BOOKS.B: Recipe(
        "core.Book",
        # kwargs
        name="book2",
        writer=foreign_key(USER_RECIPES[USERS.B]),
        genre=foreign_key(BOOK_GENRE_RECIPES[BOOK_GENRES.ROMMAN]),
        price=200.0,
        synopsis="this is synop2",
        release_date="2021-10-29T12:30:58.831431Z",
    ),
    BOOKS.C: Recipe(
        "core.Book",
        # kwargs
        name="book3",
        writer=foreign_key(USER_RECIPES[USERS.B]),
        genre=foreign_key(BOOK_GENRE_RECIPES[BOOK_GENRES.HORROR]),
        price=500.0,
        synopsis="this is synop3",
        release_date="2021-10-29T12:30:58.831431Z",
    ),
}

RECIPES = {
    USERS: USER_RECIPES,
    BOOKS: BOOK_RECIPES,
    BOOK_GENRES: BOOK_GENRE_RECIPES,
}
