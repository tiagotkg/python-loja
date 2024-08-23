# Bibliotecas necessárias:

```
 pip install pyjwt
 pip install fastapi
 pip install uvicorn
 pip install "passlib[bcrypt]"
 pip install datetime
 pip install cryptography
 pip install sqlalchemy
 pip install python-multipart
```

## No terminal execute o comando:
```
 uvicorn main:app --reload
```

 -  Como estamos tratando de uma API Rest, é possível testá-la através de softwares como Insomnia ou pela própria documentação acessando o link:
 [http://localhost:8000/docs#/](http://localhost:8000/docs#/)


 - Para conseguir utilizar as rotas é necessário gerar o token ou realizar a autenticação clicando no botão "Authorize". Utilize os seguintes dados para gerar o token:
```
 username: admin 
 password: admin
```


 - No projeto deixamos dois tipos de rotas, as abertas (open) e as encriptadas (secure). A rotas abertas possuem em sua descrição o formato do json para o cadastro e no caso das rotas encriptadas, o json deve ser encriptado utilizando a criptografia de Fernet e enviado no parâmetro "data". O segredo para a criptografia está no arquivo chamado "chave.key".


 - Deixamos também em aberto duas rotas para criptografar e descriptografar os dados das rotas encriptadas. Informe a chave (localizada no arquivo chave.key) e o conteúdo para obter a informação desejada.


 - Abaixo dois exemplos da rota "/encoder", uma para encriptar os dados do cadastro de usuário e outro para encripdar os dados do cadastro do lixo:
    
    
    POST - localhost:8000/encoder
    {
      "key": "f6dyPkSDzGDUzWtYb6JN6kmlRH56CqDm9hxkuRkistQ=",
      "data": "{\"username\": \"teste\", \"full_name\": \"teste teste\", \"email\": \"teste@teste.com\", \"password\": \"teste\"}"
    }

    Response:
    "gAAAAABmXpXYFqIIN6wyaqpUsH62UhtQOyXoGJA9YlL5Is9NWe1ASD_Ng1xZ9OUjiRotP_5fifhDTDKJ5vrYgYQp7oTe--r9bK94qzP5vhjUFc2NMNp3mbxMYS0Rhj22eawjS2BvaJfqaMdktAYI2SAm9v8rLalJyNEffhTkzZYS9kAWIFGzNW5ufmF_i7A--TwklOwKbST8atxHyAD7gA-wYdMLs4I6uw=="

    - Com este response será possivel cadastrar um usuário utilizando a rota encriptada "POST - /secure/user"
---

    POST - localhost:8000/encoder
    {
      "key": "f6dyPkSDzGDUzWtYb6JN6kmlRH56CqDm9hxkuRkistQ=",
      "data": "{\"name\": \"canudo\", \"description\": \"canudo de plástico\", \"kilos\": 23.53}"
    }

    Response:
    "gAAAAABmXpW6c1HPsGCSlkWv7J2OzRrDCwfjnrsNV5pjLlpiSUOV5L1kjm7F4tSGQG9i95tljtVAPDzcBTihWi07qLYITqzIsLgb8ElJ0kZVk6RHgQz9C5Y2MTrUk4OUr0FuU3DF6CGQ5dsY9mlwCN3fmhKodWjbWeKc5gWyIJaNFIOJM_yejO4="

    - Com este response será possivel inserir um novo registro rota encriptada "POST - /secure/trash"


 - Exemplo para descriptografar o retorno da rota "GET - /trash"
    
    
    GET - localhoset:8000/secure/trash
    Response:
    "gAAAAABmXqcXkGnTNegrPp1F7lvsqXengXGj0tWcD3mnbKmN1mbtpKUVVAjFAi1VdzT_H_G9FzBDUCAsWWH9HxO8R--kHVbZ0CK5OzvHs_MEzfuahwt3y_yfXzau7vCmA5XIHHTpKiyRypS4MhjKUk14EgtyUOxR7U2GfWqXYUEufsTJgNy2tZ3yojb-E2IFTb97PRaMyfvtZL4pjLEYggNQZmVBaeei8aZhwXdyRwqMpXV9T-tMEKs44KAO8CT8-LKIBC10ao7s2D9T_CDyebrklv8Hi7O9D3uI5C6k4YqOzg_EYZ63fyfOoFfZy-hhU6NzfJt0A_Jb_6fpG6S9hn3AnHnGm93p2w=="

    POST - localhost:8000/decoder
    {
      "key": "f6dyPkSDzGDUzWtYb6JN6kmlRH56CqDm9hxkuRkistQ=",
      "data": "gAAAAABmXqcXkGnTNegrPp1F7lvsqXengXGj0tWcD3mnbKmN1mbtpKUVVAjFAi1VdzT_H_G9FzBDUCAsWWH9HxO8R--kHVbZ0CK5OzvHs_MEzfuahwt3y_yfXzau7vCmA5XIHHTpKiyRypS4MhjKUk14EgtyUOxR7U2GfWqXYUEufsTJgNy2tZ3yojb-E2IFTb97PRaMyfvtZL4pjLEYggNQZmVBaeei8aZhwXdyRwqMpXV9T-tMEKs44KAO8CT8-LKIBC10ao7s2D9T_CDyebrklv8Hi7O9D3uI5C6k4YqOzg_EYZ63fyfOoFfZy-hhU6NzfJt0A_Jb_6fpG6S9hn3AnHnGm93p2w=="
    }
    
    Response:
    [
      {
        "id": 2,
        "kilos": 23.53,
        "name": "plastico",
        "description": "canudo de plástico",
        "owner_id": 1
      },
      {
        "id": 3,
        "kilos": 134.32,
        "name": "metal",
        "description": "lata de refrigerante",
        "owner_id": 1
      }
    ]
