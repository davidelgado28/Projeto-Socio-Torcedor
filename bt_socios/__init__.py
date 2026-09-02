import reflex as rx
from models.socios import Socio, Plano
from paginas.login import login
from paginas.admin import protegido
from state.estado import EstadoAuth, EstadoSocios

def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("Seja um Sócio-Torcedor do BT! ⚫⚪", size="8"),
            rx.text("Viva o clube de perto. Escolha seu plano e faça parte."),
            rx.hstack(
                rx.button("Entrar", on_click=rx.redirect("/login")),
                rx.button("Cadastrar", on_click=rx.redirect("/cadastro")),
            ),
            spacing="4",
        ),
        height="100vh",
    )

app = rx.App()
app.add_page(index, route="/")
app.add_page(login, route="/login")
app.add_page(protegido, route="/admin")
