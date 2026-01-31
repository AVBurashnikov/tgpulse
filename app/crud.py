from sqlalchemy.orm import Session
from models import User, Channel

def get_or_create_user(db: Session, telegram_id: int, username: str | None = None) -> User:
    user = db.query(User).filter_by(telegram_id=telegram_id).first()
    if user:
        # обновим username, если появилось
        if username and user.username != username:
            user.username = username
            db.add(user)
            db.commit()
            db.refresh(user)
        return user
    user = User(telegram_id=telegram_id, username=username)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def add_channel_for_user(db: Session, user: User, tg_username: str) -> Channel:
    # Не дублируем один и тот же канал для одного пользователя
    exists = db.query(Channel).filter_by(user_id=user.id, tg_username=tg_username).first()
    if exists:
        return exists
    channel = Channel(user_id=user.id, tg_username=tg_username)
    db.add(channel)
    db.commit()
    db.refresh(channel)
    return channel

def get_channels_for_user(db: Session, user: User):
    return db.query(Channel).filter_by(user_id=user.id).all()
