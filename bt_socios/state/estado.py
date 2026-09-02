import reflex as rx
from models.socios import Socio, Plano


class EstadoAuth(rx.State):
    usuario_logado: Socio | None = None
    erro: str = ""

    @rx.var
    # Verifica se está logado
    def esta_logado(self) -> bool:
        return self.usuario_logado is not None

    # Loga se já não estiver logado
    def login(self, form: dict):
        self.erro = ""
        with rx.session() as session:
            socio = session.exec(
                Socio.select().where(Socio.email == form["email"])
            ).first()
            if socio and socio.verificar_senha(form["senha"]):
                self.usuario_logado = socio
                return rx.redirect("/admin")
            self.erro = "E-mail ou senha inválidos."

    # Deslogar
    def logout(self):    
        self.reset()
        return rx.redirect("/")
      
    # Criação de contas
    def registrar(self, form: dict):
        self.erro = ""
        if form["senha"] != form.get("confirmar_senha", ""):
            self.erro = "As senhas não coincidem."
            return
        with rx.session() as session:
            existe = session.exec(
                Socio.select().where(Socio.email == form["email"])
            ).first()
            if existe:
                self.erro = "E-mail já cadastrado."
                return
            socio = Socio(
                nome=form["nome"],
                email=form["email"],
                senha_hash=Socio.hash_senha(form["senha"]),
                telefone=form.get("telefone", ""),
            )
            session.add(socio)
            session.commit()
            self.usuario_logado = socio
            return rx.redirect("/admin")


class EstadoSocios(rx.State):
    socios: list[Socio] = []
    busca: str = ""
    editando_id: int | None = None

    # bitch
    def carregar(self):
        with rx.session() as session:
            query = Socio.select()
            if self.busca:
                query = query.where(Socio.nome.contains(self.busca))
            self.socios = session.exec(query).all()

    def salvar(self, form: dict):
        with rx.session() as session:
            if self.editando_id:
                socio = session.get(Socio, self.editando_id)
                socio.nome = form["nome"]
                socio.email = form["email"]
                socio.telefone = form["telefone"]
            else:
                socio = Socio(
                    nome=form["nome"],
                    email=form["email"],
                    telefone=form.get("telefone", ""),
                    senha_hash=Socio.hash_senha(form.get("senha", "123456")),
                )
                session.add(socio)
            session.commit()
        self.editando_id = None
        self.carregar()

    def editar(self, socio_id: int):
        self.editando_id = socio_id

    def excluir(self, socio_id: int):
        with rx.session() as session:
            socio = session.get(Socio, socio_id)
            if socio:
                session.delete(socio)
                session.commit()
        self.carregar()

    def alternar_ativo(self, socio_id: int):
        with rx.session() as session:
            socio = session.get(Socio, socio_id)
            socio.ativo = not socio.ativo
            session.commit()
        self.carregar()
