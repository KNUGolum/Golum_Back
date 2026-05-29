from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.models.title import Title, UserTitle
from app.models.user import User

def getShopTitles(db: Session):
    return db.query(Title).order_by(Title.id).all()

def purchaseTitle(db: Session, userId: int, titleId: int):
    try:
        user = db.query(User).filter(User.id == userId).first()

        if not user:
            return None, "USER_NOT_FOUND"

        title = db.query(Title).filter(Title.id == titleId).first()

        if not title:
            return None, "TITLE_NOT_FOUND"

        alreadyOwnedTitle = db.query(UserTitle).filter(
            UserTitle.user_id == userId,
            UserTitle.title_id == titleId
        ).first()

        if alreadyOwnedTitle:
            return None, "ALREADY_OWNED"

        if user.credit < title.price:
            return None, "INSUFFICIENT_CREDIT"

        user.credit -= title.price

        newUserTitle = UserTitle(
            user_id=userId,
            title_id=titleId
        )

        db.add(newUserTitle)
        db.commit()
        db.refresh(newUserTitle)
        db.refresh(user)

        return user, "SUCCESS"

    except SQLAlchemyError as databaseError:
        db.rollback()
        raise databaseError

def equipTitle(db: Session, userId: int, titleId: int):
    try:
        user = db.query(User).filter(User.id == userId).first()

        if not user:
            return None, "USER_NOT_FOUND"

        userTitle = db.query(UserTitle).filter(
            UserTitle.user_id == userId,
            UserTitle.title_id == titleId
        ).first()

        if not userTitle:
            return None, "TITLE_NOT_OWNED"

        if user.equipped_title_id == titleId:
            return None, "ALREADY_EQUIPPED"

        user.equipped_title_id = titleId

        db.commit()
        db.refresh(user)

        return user, "SUCCESS"

    except SQLAlchemyError as databaseError:
        db.rollback()
        raise databaseError


def unequipTitle(db: Session, userId: int):
    try:
        user = db.query(User).filter(User.id == userId).first()

        if not user:
            return None, "USER_NOT_FOUND"

        user.equipped_title_id = None

        db.commit()
        db.refresh(user)

        return user, "SUCCESS"

    except SQLAlchemyError as databaseError:
        db.rollback()
        raise databaseError