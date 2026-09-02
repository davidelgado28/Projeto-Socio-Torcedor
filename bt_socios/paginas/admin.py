import reflex as rx
from state.estado import EstadoAuth, EstadoSocios
from models.socios import Socio


def linha_socio(socio: Socio) -> rx.Component:
    return rx.table.row(
        rx.table.cell(socio.nome),
        rx.table.cell(socio.email),
        rx.table.cell(socio.telefone),
        rx.table.cell(
            rx.badge(
                rx.cond(socio.ativo, "Ativo", "Inativo"),
                color_scheme=rx.cond(socio.ativo, "green", "red"),
            )
        ),
        rx.table.cell(
            rx.hstack(
                rx.button("Editar", on_click=lambda: EstadoSocios.editar(socio.id), size="1"),
                rx.button(
                    "Excluir",
                    on_click=lambda: EstadoSocios.excluir(socio.id),
                    size="1",
                    color_scheme="red",
                ),
                spacing="2",
            )
        ),
    )

def formulario_socio() -> rx.Component:
    return rx.card(
        rx.form(
            rx.vstack(
                rx.heading(
                    rx.cond(EstadoSocios.editando_id, "Editar Sócio", "Novo Sócio"),
                    size="4",
                ),
                rx.input(placeholder="Nome", name="nome", required=True),
                rx.input(placeholder="E-mail", name="email", type_="email", required=True),
                rx.input(placeholder="Telefone", name="telefone"),
                rx.button("Salvar", type_="submit", width="100%"),
                spacing="3",
            ),
            on_submit=EstadoSocios.salvar,
        ),
        width="100%",
    )


def admin() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.heading("Painel do Sócio-Torcedor BT ⚫⚪", size="6"),
            rx.spacer(),
            rx.button("Sair", on_click=EstadoAuth.logout, color_scheme="red"),
            width="100%",
        ),
        formulario_socio(),
        rx.input(
            placeholder="Buscar por nome...",
            on_change=EstadoSocios.set_busca,
            on_blur=EstadoSocios.carregar,
        ),
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("Nome"),
                    rx.table.column_header_cell("E-mail"),
                    rx.table.column_header_cell("Telefone"),
                    rx.table.column_header_cell("Status"),
                    rx.table.column_header_cell("Ações"),
                )
            ),
            rx.table.body(
                rx.foreach(EstadoSocios.socios, linha_socio)
            ),
        ),
        on_mount=EstadoSocios.carregar,
        padding="2em",
        spacing="4",
        max_width="1000px",
        margin="auto",
    )


def protegido():
    """Redireciona para login se não estiver logado."""
    return rx.cond(
        EstadoAuth.esta_logado,
        admin(),
        rx.redirect("/login"),
    )
