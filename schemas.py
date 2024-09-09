from pydantic import BaseModel

# vamos criar a base dos nossos schemas para definir os atributos dos metodos do CRUD que também serão herdados

# classe para geração do token
class Token(BaseModel):
    access_token: str
    token_type: str

# classe utilizada na verificação do token
class TokenData(BaseModel):
    username: str | None = None


# criando classe para receber atributos para codificar e decodificar os dados
class DataEncodeDecode(BaseModel):
    key: str
    data: str

# classe utilizada no request dos dados criptografados
class DataEncoded(BaseModel):
    data: str

# criando UserBase para ter atributos comuns ao criar ou recuperar os dados
class UserBase(BaseModel):
    username: str
    full_name: str
    email: str

# criando o UserCreate que hedará o o UserBase mais os dados para a criação. Assim o usuário também tera uma senha ao criá-lo.
# Mas por segurança, a senha não estará em outros schemas ou seja, ela não será retornada ao recuperar o usuário
class UserCreate(UserBase):
    password: str

# classe utilizada para listar o usuário
class User(UserBase):
    id: int
    disabled: bool

    class Config:
        from_attributes = True