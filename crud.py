from sqlalchemy.orm import Session

import models, schemas

# aqui definimos os metodos utilizado para trabalhar junto com o banco de dados

# metodo que recupera o usuário pelo id
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


# metodo utilizado para recuprar o usuario pelo username
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


# metodo que lista os usuário
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


# metodo que cria os usuário
def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(
        username=user.username,
        full_name=user.full_name,
        email=user.email,
        hashed_password=user.password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# metodo utilizado para listar os lixos cadastrados
def get_trash(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Trash).offset(skip).limit(limit).all()


# metodo utilizado para cadastrar um novo lixo
def create_trash(db: Session, trash: schemas.TrashCreate, user_id: int):
    db_lixo = models.Trash(**trash.dict(), owner_id=user_id)
    db.add(db_lixo)
    db.commit()
    db.refresh(db_lixo)
    return db_lixo