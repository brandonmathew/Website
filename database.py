from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime


Base = declarative_base()

class ArtistStats(Base):
    __tablename__ = 'artist_stats'

    id = Column(Integer, primary_key=True)
    artist_id = Column(String)
    followers = Column(Integer)
    popularity = Column(Integer)
    listeners = Column(Integer)
    timestamp = Column(DateTime, nullable=True)

engine = create_engine('sqlite:///artist_stats.db')
Session = sessionmaker(bind=engine)
session = Session()

def create_tables():
    Base.metadata.create_all(engine)

def add_stat(artist_id, followers, popularity, listeners, timestamp=None):
    if timestamp is None:
        timestamp = datetime.utcnow()
    stat = ArtistStats(artist_id=artist_id, followers=followers, popularity=popularity, listeners=listeners, timestamp=timestamp)
    session.add(stat)
    session.commit()


def get_stats(artist_id):
    engine = create_engine('sqlite:///artist_stats.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    stats = session.query(ArtistStats).filter(ArtistStats.artist_id == artist_id).order_by(ArtistStats.timestamp.asc()).all()
    session.close()

    return [{
        'timestamp': stat.timestamp,
        'followers': stat.followers,
        'popularity': stat.popularity,
        'listeners': stat.listeners
    } for stat in stats]

if __name__ == '__main__':
    create_tables()
