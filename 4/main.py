import datetime

from sqlalchemy import *
from sqlalchemy.orm import Session
from konstruktoren import Studio, Movie, Genre, Base
from konstruktoren import movie_genre_association_table

user = ""
pwd = ""
database = ""
server = ""

engine = create_engine(f"postgresql+psycopg2://{user}:{pwd}@{server}/{database}", echo=False)
connection = engine.connect()
metadata = MetaData()
#movie_genre_association_table.create(engine)


Base.metadata.create_all(engine)
session = Session(engine)


def db_fill():
    studio1 = Studio('Universal Pictures', 'United States')
    studio2 = Studio('Warner Bros', 'United States')

    movie1 = Movie('tt1323594', 'Despicable Me', datetime.date(2010, 6, 19), 'Universal Pictures')
    movie2 = Movie('tt0107290', 'Jurassic Park', datetime.date(1993, 9, 2), 'Universal Pictures')
    movie3 = Movie('tt0232500', 'Fast and Furious', datetime.date(2001, 10, 18), 'Universal Pictures')
    movie4 = Movie('tt0241527', 'Harry Potter', datetime.date(2001, 11, 22), 'Warner Bros')
    movie5 = Movie('tt0133093', 'The Matrix', datetime.date(1999, 6, 17), 'Warner Bros')
    movie6 = Movie('tt7286456', 'Joker', datetime.date(2019, 10, 10), 'Warner Bros')

    genre1 = Genre('Komödie')
    genre2 = Genre("Animation")
    genre3 = Genre("Science-Fiction")
    genre4 = Genre("Aktion")

    studio1.movies.append(movie1)
    studio1.movies.append(movie2)
    studio1.movies.append(movie3)
    studio2.movies.append(movie4)
    studio2.movies.append(movie5)
    studio2.movies.append(movie6)

    movie1.genres.append(genre1)
    movie1.genres.append(genre2)
    movie2.genres.append(genre3)
    movie2.genres.append(genre4)
    movie3.genres.append(genre3)
    movie3.genres.append(genre4)
    movie4.genres.append(genre3)
    movie5.genres.append(genre3)
    movie5.genres.append(genre4)
    movie6.genres.append(genre4)

    session.add(studio1)
    session.add(studio2)

    session.add(movie1)
    session.add(movie2)
    session.add(movie3)
    session.add(movie4)
    session.add(movie5)
    session.add(movie6)

    session.add(genre1)
    session.add(genre2)
    session.add(genre3)
    session.add(genre4)

    session.commit()


def clear_db():
    movies = session.query(Movie)

    for movie in movies:
        movie.genres = []

    movies.delete()
    session.query(Genre).delete()
    session.query(Studio).delete()

    session.commit()


def print_all_studios():
    studios = session.query(Studio)

    if not studios:
        print(f'Kein Studios')
        return

    print()
    print('-----Studio-----')
    for studio in studios:
        print(studio.name, studio.country, sep=' | ')


def print_all_movies_of_a_studio(studio: str):
    movies = session.query(Movie).filter(Movie.producer_studio == studio).all()

    if not movies:
        print(f'Keine Filme vom Studio {studio}')
        return

    print()
    print('-----Filme-----')
    for movie in movies:
        print(movie.imdb_id, movie.title, movie.year, movie.producer_studio, sep=' | ')


def print_all_genres():
    genres = session.query(Genre)

    if not genres:
        print('Keine Genre')
        return

    print()
    print('-----Genre-----')
    for genre in genres:
        print(genre.genre)


def print_all_movies_by_genre(genre: str):
    movies = session.query(Movie).join(Genre, Movie.genres).filter(Genre.genre == genre).all()

    if not movies:
        print(f'Keine Filme vom Genre {genre}')
        return

    print()
    print('-----Filme-----')
    for movie in movies:
        print(movie.imdb_id, movie.title, movie.year, movie.producer_studio, sep=' | ')


def menu():
    while True:
        print()

        print("Informationssystem für Studios und Filme - Hauptmenü")
        print("------------------------------------")

        print("1 Ausgabe aller Studios")
        print("2 Ausgabe aller Filme eines Studios")
        print("3 Ausgabe aller Genres")
        print("4 Ausgabe aller Filme eines Genres")
        print("0 Programm beenden")

        inp = input("Eingabe? ")

        if inp == "0":
            return
        elif inp == "1":
            print_all_studios()
        elif inp == "2":
            studio = input("Name des Studios? ")
            print_all_movies_of_a_studio(studio)
        elif inp == "3":
            print_all_genres()
        elif inp == "4":
            genre = input("Welches Genre? ")
            print_all_movies_by_genre(genre)
        else:
            print('Ungültige Eingabe!')


if __name__ == '__main__':
    db_fill()
    menu()
    clear_db()

    session.close()