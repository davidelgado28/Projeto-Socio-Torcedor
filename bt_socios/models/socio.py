import bcrypt
from datetime import datetime

import reflex as rx
from sqlmodel import Field

class Socio(rx.Model, table=True):
    """Modelo do sócio-torcedor do BT."""

    nome: str
    email: str = Field(unique=True, index=True)
    senha_hash: str
    cpf: str = ""
    telefone: str = ""
    plano_id: int | None = Field(default=None, foreign_key="plano.id")
    ativo: bool = True
    is_admin: bool = False
    criado_em: datetime = Field(default_factory=datetime.utcnow)

    def verificar_senha(self, senha: str) -> bool:
        """Confere se a senha bate com o hash salvo no banco."""
        return bcrypt.checkpw(senha.encode(), self.senha_hash.encode())

    @staticmethod
    def hash_senha(senha: str) -> str:
       Gera o hash bcrypt da senha (nunca salvamos senha pura!)."""
        return bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()

    def __repr__(self) -> str:
        return f"<Socio {self.nome} ({self.email})>"


class Plano(rx.Model, table=True):
    """Planos de sócio-torcedor (ex: Bronze, Prata, Ouro)."""

    nome: str
    preco_mensal: float
    beneficios: str = ""  # texto livre, separado por vírgula ou quebra de linha

    def __repr__(self) -> str:
        return f"<Plano {self.nome} - R$ {self.preco_mensal}/mês>"
