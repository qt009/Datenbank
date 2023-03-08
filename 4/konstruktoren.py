from sqlalchemy import Column, Integer, String, ForeignKeyConstraint, ForeignKey, Table, Date
from sqlalchemy.dialects.postgresql import Any
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()





class Studio(Base):
    __tablename__ = 'studio'

    def __init__(self, name, country, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.name = name
        self.country = country

    name = Column(String, primary_key=True)
    country = Column(String, nullable=False)
    movies = relationship('Movie', backref='studio')

movie_genre_association_table = Table(
    "movie_genre_association_table",
    Base.metadata,
    Column('movie_imdb_id', String, ForeignKey('movie.imdb_id'), primary_key=True),
    Column('genre_genre', String, ForeignKey('genre.genre'), primary_key=True)
)
class Movie(Base):
    __tablename__ = 'movie'

    def __init__(self, imdb_id, title, year, producer_studio, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.imdb_id = imdb_id
        self.title = title
        self.year = year
        self.producer_studio = producer_studio

    imdb_id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    year = Column(Date, nullable=False)
    producer_studio = Column(String, ForeignKey('studio.name'))
    genres = relationship('Genre', secondary=movie_genre_association_table)


class Genre(Base):
    __tablename__ = 'genre'

    def __init__(self, genre, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.genre = genre

    genre = Column(String, primary_key=True)

