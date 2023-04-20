import firebase_admin
from firebase_admin import auth
import bcrypt


def _hash_password(self, password):
    # Gera um hash de senha usando o Bcrypt
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password


def _verify_password(password, hashed_password):
    # Verifica se a senha corresponde ao hash de senha usando o Bcrypt
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)


def create(self, email, password) -> auth:
    try:
        # Cria um novo usuário no Firebase Auth
        user = auth.create_user(
            email=email,
            password=self._hash_password(password)
        )
        return user

    except auth.AuthError as e:
        # Retorna uma mensagem de erro, caso ocorra um erro na criação do usuário
        return f"Erro ao criar usuário no Firebase Auth - " + e


def authenticate_user(self, email, password) -> auth:
    try:
        # Autentica o usuário com o Firebase Auth
        if self._verify_password(password, self._hash_password(password)):
            user = auth.get_user_by_email(email)
            user = auth.refresh(user.refresh_token)

            return user
        raise auth.AuthError
    except ValueError as e:
        # Retorna uma mensagem de erro, caso ocorra um erro na autenticação do usuário
        return f"Erro ao criar usuário no Firebase Auth - " + e
