import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

_path = os.path.join(os.path.expanduser('~'), 'deezer_dl')
os.makedirs(_path, exist_ok=True)
eng_path = os.path.join(_path, 'deezerdl.db')

engine = create_engine('sqlite:///{eng_path}'.format(eng_path=eng_path))
Session = sessionmaker(bind=engine)

Base = declarative_base()

Base.metadata.create_all(engine)
