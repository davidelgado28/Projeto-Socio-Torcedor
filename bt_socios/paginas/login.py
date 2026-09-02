import reflex as rx
from state.estado import EstadoAuth


def login() -> rx.Component:
    return rx.center(
        rx.card(
            rx.vstack(
                rx.heading("BT Torcedores ⚽", size="6", align="center"),
                rx.text("Acesse sua conta", size="2", color_scheme="gray"),
                rx.form(
                    rx.vstack(
                        rx.input(placeholder="E-mail", name="email", type_="email", required=True),
                        rx.input(placeholder="Senha", name="senha", type_="password", required=True),
                        rx.callout(EstadoAuth.erro, color_scheme="red"),
                        rx.button("Entrar", type_="submit", width="100%"),
                        spacing="3",
                    ),
                    on_submit=EstadoAuth.login,
                ),
                rx.link("Ainda não é sócio? Cadastre-se", href="/cadastro"),
                spacing="4",
            ),
            width="380px",
            padding="2em",
        ),
        height="100vh",
    )
