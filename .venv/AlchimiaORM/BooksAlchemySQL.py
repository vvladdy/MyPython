import csv
import googletrans
from sqlalchemy.engine import create_engine
from sqlalchemy import Integer, SmallInteger, Date, Column, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship


engine = create_engine('sqlite:///booksql.db', echo=True)

Base = declarative_base()


class BookPublish(Base):
    __tablename__ = 'publish'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(150), nullable=False)
    author = Column(String(50), nullable=False)
    publisher = Column(String(50), nullable=False)
    publishedDate = Column(Date)


class Book(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(150), ForeignKey(BookPublish.title), nullable=False)
    author = Column(String(50), nullable=False)
    language = Column(String(10), nullable=False)
    pagecount = Column(Integer)
    averageraiting = Column(SmallInteger)
    publish_table = Column(String, ForeignKey('book.title'))

    book_pub = relationship('BookPublish', foreign_keys='Book.title')


class Author(Base):
    __tablename__ = 'author'

    id = Column(Integer, primary_key=True, autoincrement=True)
    author = Column(String(150), ForeignKey(Book.title), nullable=False)

    books = relationship('Book', foreign_keys='Author.author')


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(String(50), ForeignKey(Author.author))

    authors = relationship('Author', foreign_keys='Category.category')


# Создание таблиц
#Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()

translator = googletrans.Translator()

with open(r'D:\MyPythonFolder\MyPython\.venv\Dif_files\csv'
          r'\google_books_dataset.csv', 'r', encoding='utf-8') as file:
    content = csv.DictReader(file)
    for row in content:
        # print(row)
        if row['language'] == 'ar':
            trans_title = translator.translate(row['title'], dest='en').text
            # print(trans_title.text)
        else:
            trans_title = row['title']
        title_t = trans_title
        auth = row['authors']
        lang = row['language']
        categories = row['categories']
        pages = row['pageCount']
        raiting = row['averageRating']
        publisher_t = row['publisher']
        publisher_d = row['publishedDate']

        categ = Category(category=categories)
        aut = Author(author=auth)
        book = Book(title=title_t, author=auth, language=lang, pagecount=pages,
                    averageraiting=raiting, publish_table=publisher_t)
        publish = BookPublish(title=title_t, author=auth,
                              publisher=publisher_t)

        # session.add_all([categ, aut, book, publish])
        # session.commit()




# Создание таблиц не классами
# node = Table(
#     "node",
#     metadata_obj,
#     Column("node_id", Integer, primary_key=True),
#     Column("primary_element", Integer, ForeignKey("element.element_id")),
# )
#
# element = Table(
#     "element",
#     metadata_obj,
#     Column("element_id", Integer, primary_key=True),
#     Column("parent_node_id", Integer),
#     ForeignKeyConstraint(
#         ["parent_node_id"], ["node.node_id"], name="fk_element_parent_node_id"
#     ),
# )