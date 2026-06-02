from sqlalchemy.orm import Session

from app.models.title import Title

def getShopTitles(db: Session):
    return db.query(Title).order_by(Title.id).all()