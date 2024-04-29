# CompliAI
Para utilizar este projeto recomendo utilizar o Linux e caso esteja no Windows utilizar o WSL  
  
## Como iniciar o projeto
1. Criar ambiente virtual
```
# Linux / WSL
python3 -m venv .venv
# Windows
python -m venv .venv
```
2. Ativar o ambiente
```
# Linux / WSL
. ./.venv/bin/activate
# Windows
.\.venv\Scripts\activate
```

> Para validar se o ambiente esta ativo pode utilizar o seguinte comando
> `which python3` ou `gcm python` no windows

3. Instalar as bibliotecas
```
pip install -r ./requirements.txt
```

## Utilizar o Genie
Após o ambiente configurado é possível usar o "genie" que é um Chat com o GPT para ser utilizado no Terminal.  
Para abrir, digite
```
# Linux
python3 genie/genie.py

# Windows
python genie/genie.py
```
![Genie Compliance](./examples/image1.png)

### Rodar a imagem Docker
```
docker run -p 8080:80 -e OPENAI_API_KEY="....." devcst/compliai

# Teste de chamada da API
curl -X POST http://127.0.0.1:8080/chain --data '{"HumamMessage": "Quem é o presidente do Brasil?"}' -H "content-type: application/json"
```

### Subir aplicação inteira
Para subir a aplicação copie o arquivo `example.env` para o arquivo `.env` e substitua os valores das chaves de API antes de subir a aplicação
```
docker compose up --build
```

### Subir o Genie no Docker
```
docker exec -it compliai-api-1 python3 main.py
```

### WebChat disponivel em :
OBS : ENV do chat inserir do DockerFile
```
http://localhost:3000
```