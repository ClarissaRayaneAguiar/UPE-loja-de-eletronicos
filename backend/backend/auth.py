from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import bcrypt
from database import conectar

SECRET_KEY = "upe-loja-eletronicos-secret-key-2024"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

security = HTTPBearer()


def criar_token(email: str):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": email,
        "exp": expire
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def validar_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Token invalido")

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, email FROM usuarios WHERE email = ?", (email,))
        usuario = cursor.fetchone()
        conn.close()

        if usuario is None:
            raise HTTPException(status_code=401, detail="Usuario nao encontrado")

        return dict(usuario)
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalido ou expirado")


def autenticar_usuario(email: str, senha: str):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, email, senha_hash FROM usuarios WHERE email = ?", (email,))
    usuario = cursor.fetchone()
    conn.close()

    if usuario is None:
        return None

    if bcrypt.checkpw(senha.encode('utf-8'), usuario["senha_hash"].encode('utf-8')):
        return {
            "id": usuario["id"],
            "nome": usuario["nome"],
            "email": usuario["email"]
        }

    return None


def hash_senha(senha: str):
    return bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verificar_senha(senha: str, hash_armazenado: str):
    return bcrypt.checkpw(senha.encode('utf-8'), hash_armazenado.encode('utf-8'))