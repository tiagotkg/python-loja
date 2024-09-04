import jwt
import json

from datetime import datetime, timedelta, timezone
from cryptography.fernet import Fernet
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext

from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine

#teste
# esse metodo cria nosso banco de dados caso ele não exista
models.Base.metadata.create_all(bind=engine)


# Carrega a chave de um arquivo utilizado para criptografar/descriptografar nossos dados
with open('chave.key', 'rb') as chave_file:
    KEY = chave_file.read()

# carrega o secret key utilizado para gerar nosso bearer token
with open('secret.key', 'rb') as chave_file:
    SECRET_KEY = chave_file.read()

# algoritmo utilizado no token
ALGORITHM = "HS256"

# tempo para expirar o token
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# gerando o modo de criptografia para nosso token
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# gerando nosso schema para o token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# instanciando nossa classe de criptografia de dados
fernet = Fernet(KEY)

# tags utilizadas para separar nossas rotas
tags_metadata = [
    {
        "name": "Open",
        "description": "Rotas sem criptografia",
    },
    {
        "name": "Secure",
        "description": "Rotas com criptografia",
    },
]


# instanciando nossa aplicação
app = FastAPI(openapi_tags=tags_metadata)

# metodo de acesso ao banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# metodo que verifica os dados de acesso para gerar o token
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# esse método converte a senha informada para hash. Utilizado para comparar a senha ou salvar um novo usuário
def get_password_hash(password):
    return pwd_context.hash(password)


# metodo que recupera o usuário pelo username
def get_user(db, username: str):
    db_user = crud.get_user_by_username(db, username=username)

    if db_user:
        return db_user


# a autenticação é feita primeiramente recuperando o usuário, caso ele exista é feito a verificação da senha de acordo com os métodos criados anteriormente
def authenticate_user(db, username: str, password: str):
    db_user = crud.get_user_by_username(db, username=username)

    if db_user is None:
        return False
    if not verify_password(password, db_user.hashed_password):
        return False
    return db_user


# geramos o token do usuario caso os dados de acesso estejam corretos, setamos por padrao  15 minutos para o token expirar
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# recupera as informaçoes contidas no token e valida novamente o usuário
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possivel validar o token de acesso",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception

        token_data = schemas.TokenData(username=username)

    except InvalidTokenError:
        raise credentials_exception

    user = get_user(db, username=token_data.username)

    if user is None:
        raise credentials_exception

    return user


# verifica se o usuário está ativo
async def get_current_active_user(current_user: Annotated[schemas.User, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

## por padrao as rotas do fast api são seguidas do método que será executado, o nome dos métodos são convertidos e listados na documentação

# rota para gerar o token de acesso
@app.post("/token", tags=["Open"])
async def login_for_access_token( # metodo que gera o token de acesso
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)
) -> schemas.Token:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type="bearer")


# rota para listar os usuários cadastrados
@app.get("/users/", response_model=list[schemas.User], tags=["Open"])
async def get_users(current_user: Annotated[schemas.User, Depends(get_current_active_user)], skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    trash = crud.get_users(db, skip=skip, limit=limit)

    return trash


# rota para inserir um novo usuário
@app.post("/user/", response_model=schemas.User, tags=["Open"])
async def create_user(current_user: Annotated[schemas.User, Depends(get_current_active_user)], user: schemas.UserCreate, db: Session = Depends(get_db)):
    user.password = get_password_hash(user.password)
    created_user = crud.create_user(db=db, user=user)

    return created_user


# rota para listar os lixos cadastrados
@app.get("/trash/", response_model=list[schemas.Trash], tags=["Open"])
async def get_trash(current_user: Annotated[schemas.User, Depends(get_current_active_user)], skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    trash = crud.get_trash(db, skip=skip, limit=limit)

    return trash

# rota para inserir um novo lixo no banco de dados
@app.post("/trash/", response_model=schemas.Trash, tags=["Open"])
async def create_trash(current_user: Annotated[schemas.User, Depends(get_current_active_user)], trash: schemas.TrashCreate, db: Session = Depends(get_db)):
    trash = crud.create_trash(db, trash=trash, user_id=current_user.id)

    return trash


# rota para decriptografar o dado
@app.post("/decoder/", tags=["Open"])
async def decoder(current_user: Annotated[schemas.User, Depends(get_current_active_user)], dados:schemas.DataEncodeDecode, db: Session = Depends(get_db)):
    try:
        fernet = Fernet(dados.key)

        string_decoded = fernet.decrypt(dados.data).decode("utf-8")
        string_json = json.loads(string_decoded)

    except:
        raise HTTPException(status_code=404, detail="Não foi possível decriptografar os dados, verifique a string e chave informada")

    return string_json


# rota para encriptografar o dado
@app.post("/encoder", tags=["Open"])
async def encoder(current_user: Annotated[schemas.User, Depends(get_current_active_user)], dados:schemas.DataEncodeDecode, db: Session = Depends(get_db)):
    try:
        fernet = Fernet(dados.key)
        string_encoded = fernet.encrypt(dados.data.encode())

        return string_encoded
    except:
        raise HTTPException(status_code=404, detail="Não foi possível encriptar os dados, verifique a string e chave informada")


# rota criptografada para listar o usuarios
@app.get("/secure/users/", tags=["Secure"])
async def get_encrypted_users(current_user: Annotated[schemas.User, Depends(get_current_active_user)], skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    users_json = jsonable_encoder(users)
    users_stringfy = json.dumps(users_json)
    users_encoded = fernet.encrypt(users_stringfy.encode())

    return users_encoded


# rota criptografada para cadastrar um usuário
@app.post("/secure/user/", response_model=schemas.User, tags=["Secure"])
async def create_encrypted_user(current_user: Annotated[schemas.User, Depends(get_current_active_user)], user: schemas.DataEncoded, db: Session = Depends(get_db)):
    string_decoded = fernet.decrypt(user.data).decode("utf-8")
    users_json = json.loads(string_decoded)
    password = get_password_hash(users_json['password'])
    user_create = schemas.UserCreate(username=users_json['username'], full_name=users_json['full_name'], email=users_json['email'], password=password)


    created_user = crud.create_user(db=db, user=user_create)

    return created_user


# # rota criptografada para listar os lixos cadastrados
@app.get("/secure/trash/", tags=["Secure"])
async def get_encrypted_trash(current_user: Annotated[schemas.User, Depends(get_current_active_user)], skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    trash = crud.get_trash(db, skip=skip, limit=limit)
    trash_json = jsonable_encoder(trash)
    trash_stringfy = json.dumps(trash_json)
    trash_encoded = fernet.encrypt(trash_stringfy.encode())

    return trash_encoded


# rota criptografada para cadatrar o lixo
@app.post("/secure/trash/", response_model=schemas.Trash, tags=["Secure"])
async def create_encrypted_trash(current_user: Annotated[schemas.User, Depends(get_current_active_user)], trash: schemas.DataEncoded, db: Session = Depends(get_db)):
    string_decoded = fernet.decrypt(trash.data).decode("utf-8")
    trash_json = json.loads(string_decoded)
    trash_create = schemas.TrashCreate(name=trash_json["name"],description=trash_json["description"],  kilos=trash_json["kilos"])
    trash = crud.create_trash(db, trash=trash_create, user_id=current_user.id)

    return trash


