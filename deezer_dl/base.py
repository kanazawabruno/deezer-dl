from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


eng_path =  os.path.join(os.path.expanduser('~'), 'deezer_dl', 'deezerdl.db')


engine = create_engine('sqlite:///{eng_path}'.format(eng_path=eng_path))
Session = sessionmaker(bind=engine)

Base = declarative_base()

Base.metadata.create_all(engine)
