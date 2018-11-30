from sqlalchemy import Column, Integer, String, Table, MetaData

from deezer_dl.base import Base, Session, engine

metadata = MetaData()

# Create an empty table
deezerdl = Table('deezerdl', metadata,
                 Column('id', Integer, primary_key=True),
                 Column('artist', String),
                 Column('song', String),
                 Column('sha1', String))

metadata.create_all(engine)


class DeezerDLmodel(Base):
    __tablename__ = 'deezerdl'

    id = Column(Integer, primary_key=True)
    artist = Column(String)
    song = Column(String)
    sha1 = Column(String)

    def __init__(self, artist, song, sha1):
        self.artist = artist
        self.song = song
        self.sha1 = sha1
        self.__session = Session()

    @classmethod
    def find_by_song(cls, song):
        return Session().query(cls).filter(cls.song == song).first()

    def json(self):
        return {self.artist: {'title': self.song, 'sha1': self.sha1}}

    def save_to_db(self):
        self.__session.add(self)
        self.__session.commit()

    def delete_from_db(self):
        self.__session.delete(self)
        self.__session.commit()

    def __repr__(self):
        repr = "Artist(name={0}, song={1}, sha1={2}')".format(self.artist, self.song, self.sha1)
        return repr
