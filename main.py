import flet as ft
from jogadores import jogadores
from titulos import TITULOS
from clube import dados_clube
from tabela import tabela

# Constantes de Design - Identidade Galatasaray
COR_PRIMARIA = "#D32F2F"    # Vermelho Oficial
COR_SECUNDARIA = "#FFC107"  # Amarelo/Ouro Oficial        
COR_FUNDO = "#D32F2F"       # Fundo Vermelho
COR_CARD = "#B71C1C"        # Vermelho Escuro para contraste
COR_BRANCO = "#FFFFFF"       
COR_BRANCO_70 = "#B3FFFFFF" 

# Configuração da Liga 
LEAGUE_ID_TURKEY = 203
SEASON_ATUAL = 2022
TEAM_ID = 645

def status_chip(status):
    cores = {"Disponível": "#388E3C", "Dúvida": "#FB8C00", "Indisponível": "#D32F2F"}
    return ft.Chip(
        label=ft.Text(status),
        bgcolor=cores.get(status, "#757575"),
        label_style=ft.TextStyle(color=COR_BRANCO)
    )

def main(page: ft.Page):
    page.title = "Galatasaray Fan App"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = COR_FUNDO
    page.padding = 0
    
    clube = dados_clube()
    elenco = jogadores()
    dados_tabela = tabela(league_id=LEAGUE_ID_TURKEY, season=SEASON_ATUAL)

    # --- LÓGICA DE NAVEGAÇÃO INTERNA DE TÍTULOS ---
    lista_titulos_container = ft.Column(expand=True)
    detalhes_container = ft.Column(visible=False, expand=True, scroll=ft.ScrollMode.ADAPTIVE)

    def abrir_titulo(titulo_selecionado):
        lista_titulos_container.visible = False
        detalhes_container.visible = True
        
        # Conteúdo do Detalhe (Aparece na mesma janela)
        detalhes_container.controls = [
            ft.Container(
                padding=20,
                content=ft.Column([
                    ft.IconButton(
                        icon="arrow_back", # Usando string direta para evitar erro de atributo
                        on_click=voltar_para_lista, 
                        icon_color=COR_SECUNDARIA
                    ),
                    ft.Text(titulo_selecionado["nome"], size=28, weight="bold", color=COR_SECUNDARIA),
                    ft.Image(src=titulo_selecionado.get("capa_url"), border_radius=10),
                    ft.Divider(height=20, color=COR_BRANCO_70),
                    ft.Markdown(
    titulo_selecionado.get("historia_detalhada", ""),
    selectable=True,
    extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
    # Em vez de style ou text_style, usamos as propriedades de estilo de cores do Markdown:
    md_style_sheet=ft.MarkdownStyleSheet(
        p_text_style=ft.TextStyle(color="white"),
        h1_text_style=ft.TextStyle(color=COR_SECUNDARIA, weight="bold"),
        h2_text_style=ft.TextStyle(color=COR_SECUNDARIA, weight="bold"),
    ),
),
                ])
            )
        ]
        

    def voltar_para_lista(e):
        lista_titulos_container.visible = True
        detalhes_container.visible = False
        page.update()

    # --- VIEWS DAS ABAS ---
    
    # Aba Jogadores
    jogadores_view = ft.ListView(
        expand=True, spacing=10, padding=10,
        controls=[
            ft.Container(
                padding=10, border_radius=12, bgcolor=COR_CARD,
                content=ft.Row([
                    ft.Container(
                        width=60, height=60, border_radius=30, border=ft.border.all(2, COR_SECUNDARIA),
                        content=ft.Image(src=j["foto"], fit=ft.ImageFit.COVER),
                        clip_behavior=ft.ClipBehavior.HARD_EDGE
                    ),
                    ft.Column([
                        ft.Text(j["nome"], size=18, weight="bold", color=COR_BRANCO),
                        ft.Text(j["posicao"], size=12, color=COR_BRANCO_70),
                    ], expand=True),
                    status_chip(j["status"])
                ])
            ) for j in elenco
        ]
    )

    # Aba Títulos (Integrada)
    titulos_list_view = ft.ListView(
        expand=True, padding=10,
        controls=[
            ft.Container(
                bgcolor=COR_CARD, border_radius=10, margin=5,
                content=ft.ListTile(
                    leading=ft.Icon("emoji_events", color=COR_SECUNDARIA), # 'emoji_events' é o ícone de troféu padrão
                    title=ft.Text(t["nome"], weight="bold", color=COR_BRANCO),
                    subtitle=ft.Text(t["descricao"], color=COR_BRANCO_70, max_lines=1),
                    on_click=lambda e, data=t: abrir_titulo(data),
                )
            ) for t in TITULOS
        ]
    )
    lista_titulos_container.controls = [titulos_list_view]

    # Aba Uniformes (3D/Fotos)
    uniformes_view = ft.GridView(
        expand=True, max_extent=250, child_aspect_ratio=0.7, spacing=10, padding=10,
        controls=[
            ft.Container(
                bgcolor=COR_CARD, border_radius=10, padding=10,
                content=ft.Column([
                    ft.Image(src=url, height=180, fit=ft.ImageFit.CONTAIN),
                    ft.Text(nome, weight="bold", color=COR_BRANCO, text_align="center")
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            ) for url, nome in [
                ("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQjXEQLjAW5IUtyeKz4FRfXyImX2huNNEmTJw&s", "Titular 2022"),
                ("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS6r6lWHu9LNDeNhgdCREMNokmOChIbirI6Ew&s", "Alternativo")
            ]
        ]
    )

    # Aba Tabela
    tabela_view = ft.ListView(
        expand=True, padding=10,
        controls=[
            ft.Text(f"Süper Lig {SEASON_ATUAL}", size=20, weight="bold", text_align="center"),
            *[ft.Container(
                padding=10, margin=2, border_radius=8,
                bgcolor=COR_SECUNDARIA if t["team"].get("id") == TEAM_ID else COR_CARD,
                content=ft.Row([
                    ft.Text(str(t["rank"]), width=30, color="black" if t["team"].get("id") == TEAM_ID else "white"),
                    ft.Text(t["team"]["name"], expand=True, color="black" if t["team"].get("id") == TEAM_ID else "white"),
                    ft.Text(str(t["points"]), weight="bold")
                ])
            ) for t in dados_tabela]
        ]
    )

    # --- ESTRUTURA FINAL ---
    header = ft.Container(
        content=ft.Row([
            ft.Image(src=clube["logo"], width=50),
            ft.Column([
                ft.Text(clube["nome"], size=22, weight="bold"),
                ft.Text(f"Fundação: {clube['fundacao']}", size=12)
            ])
        ]), padding=15, bgcolor=COR_CARD
    )

    tabs = ft.Tabs(
        expand=True, selected_index=0,
        indicator_color=COR_SECUNDARIA, label_color=COR_SECUNDARIA,
        unselected_label_color=COR_BRANCO_70,
        tabs=[
            ft.Tab(text="Jogadores", content=jogadores_view),
            ft.Tab(text="Títulos", content=ft.Column([lista_titulos_container, detalhes_container])),
            ft.Tab(text="Tabela", content=tabela_view),
            ft.Tab(text="Uniformes", content=uniformes_view),
        ]
    )

    page.add(header, tabs)

if __name__ == "__main__":
    ft.app(target=main)