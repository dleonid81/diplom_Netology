# импорты
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import Session
from vkinder.config import db_url_object


# схема БД
metadata = MetaData()
Base = declarative_base()


class Viewed(Base):
    __tablename__ = 'viewed'
    profile_id = sq.Column(sq.Integer, primary_key=True)
    worksheet_id = sq.Column(sq.Integer, primary_key=True)


class Last_offset(Base):
    __tablename__ = 'last_offset'
    profile_id = sq.Column(sq.Integer, primary_key=True)
    offset = sq.Column(sq.Integer, primary_key=True)


def add_user(engine, profile_id, worksheet_id):
    with Session(engine) as session:
        to_bd = Viewed(profile_id=profile_id, worksheet_id=worksheet_id)
        session.add(to_bd)
        session.commit()


def last_offset(engine, profile_id, offset):
    with Session(engine) as session:
        to_bd = Last_offset(profile_id=profile_id, offset=offset)
        session.add(to_bd)
        session.commit()


def user_exists_in_db(engine, profile_id, worksheet_id):
    with Session(engine) as session:
        user = session.query(Viewed).filter(
            Viewed.profile_id == profile_id,
            Viewed.worksheet_id == worksheet_id).first()
        return True if user else False


def set_offset(engine, profile_id, new_offset):
    print(f'У вас {profile_id}, новый оффсет {new_offset}')
    session = Session(engine) 
    existing_offset = session.query(Last_offset).filter_by(profile_id=profile_id).first()
    if existing_offset:
        existing_offset.offset = new_offset
    else:
        new_entry = Last_offset(profile_id=profile_id, offset=new_offset)
        session.add(new_entry)

    session.commit() 
    session.close()  


if __name__ == '__main__':
    engine = create_engine(db_url_object)
    Base.metadata.create_all(engine)