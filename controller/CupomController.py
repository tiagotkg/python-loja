from xmlrpc.client import DateTime

from math import trunc
from sqlalchemy import delete, Column, func
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException
from sqlalchemy.sql.operators import and_

from model.Cupom import Cupom
import schema


# metodo utilizado para listar os lixos cadastrados
def get_cupom(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Cupom).filter(Cupom.deleted_at == None).offset(skip).limit(limit).all()


def get_cupom_estoque(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Cupom).options(joinedload(Cupom.estoque)).offset(skip).limit(limit).all()


def get_cupom_estoque_alerta(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Cupom).options(joinedload(Cupom.estoque)).filter(Cupom.quantidade <= Cupom.quantidade_minima).all()


# metodo utilizado para cadastrar um novo lixo
def create_cupom(db: Session, cupom: schema.CupomSchema.CupomCreate):
    db_cupom = Cupom(**cupom.model_dump())
    db.add(db_cupom)
    db.commit()
    db.refresh(db_cupom)
    return db_cupom


def update_cupom(db: Session, cupom_id: int, cupom: schema.CupomSchema.CupomUpdate):
    db_cupom = db.query(Cupom).filter(Cupom.id == cupom_id).first()
    if db_cupom is None:
        raise HTTPException(status_code=404, detail="Cupom não encontrado")

    for key, value in cupom.model_dump().items():
        if(value):
            setattr(db_cupom, key, value)

    db.commit()
    db.refresh(db_cupom)
    return db_cupom

def delete_cupom(db: Session, cupom_id: int):
    db_cupom = db.query(Cupom).filter(and_(Cupom.id == cupom_id, Cupom.deleted_at == None)).first()

    if db_cupom is None:
        raise HTTPException(status_code=404, detail="Cupom não encontrado")

    db_cupom.deleted_at = func.now()
    db.commit()
    db.refresh(db_cupom)
    return db_cupom

