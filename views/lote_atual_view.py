from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton, QFrame
)
from services.lote_service import buscar_lote_ativo
from config.window_config import (
    DEFAULT_WIDTH,
    DEFAULT_HEIGHT,
    DEFAULT_MIN_WIDTH,
    DEFAULT_MIN_HEIGHT
)


class LoteAtualView(QWidget):
    def __init__(self, dados_usuario):
        super().__init__()

        self.dados_usuario = dados_usuario

        self.setWindowTitle("Sistema de Suínos - Lote Ativo")
        self.resize(DEFAULT_WIDTH, DEFAULT_HEIGHT)
        self.setMinimumSize(DEFAULT_MIN_WIDTH, DEFAULT_MIN_HEIGHT)

        self.montar_interface()
        self.carregar_lote()

    def montar_interface(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(18)

        self.titulo = QLabel("Lote ativo")
        self.titulo.setObjectName("tituloDashboard")

        self.card = QFrame()
        self.card.setObjectName("painelDashboard")

        card_layout = QVBoxLayout()
        card_layout.setSpacing(10)

        self.label_nome = QLabel("Nome: -")
        self.label_data = QLabel("Data de chegada: -")
        self.label_qtd_inicial = QLabel("Quantidade inicial: -")
        self.label_qtd_atual = QLabel("Quantidade atual: -")
        self.label_peso = QLabel("Peso médio: -")
        self.label_status = QLabel("Status: -")

        self.label_nome.setObjectName("textoInfoDashboard")
        self.label_data.setObjectName("textoInfoDashboard")
        self.label_qtd_inicial.setObjectName("textoInfoDashboard")
        self.label_qtd_atual.setObjectName("textoInfoDashboard")
        self.label_peso.setObjectName("textoInfoDashboard")
        self.label_status.setObjectName("textoInfoDashboard")

        card_layout.addWidget(self.label_nome)
        card_layout.addWidget(self.label_data)
        card_layout.addWidget(self.label_qtd_inicial)
        card_layout.addWidget(self.label_qtd_atual)
        card_layout.addWidget(self.label_peso)
        card_layout.addWidget(self.label_status)

        self.card.setLayout(card_layout)

        self.botao_voltar = QPushButton("Voltar ao dashboard")
        self.botao_voltar.setObjectName("botaoSecundario")
        self.botao_voltar.clicked.connect(self.voltar_dashboard)

        layout.addWidget(self.titulo)
        layout.addWidget(self.card)
        layout.addWidget(self.botao_voltar)

        self.setLayout(layout)

    def carregar_lote(self):
        lote = buscar_lote_ativo()

        if lote:
            self.label_nome.setText(f"Nome: {lote[1]}")
            self.label_data.setText(f"Data de chegada: {lote[2]}")
            self.label_qtd_inicial.setText(f"Quantidade inicial: {lote[3]}")
            self.label_qtd_atual.setText(f"Quantidade atual: {lote[4]}")
            self.label_peso.setText(f"Peso médio: {lote[5]} kg")
            self.label_status.setText(f"Status: {lote[6]}")
        else:
            self.label_nome.setText("Nenhum lote ativo encontrado.")

    def voltar_dashboard(self):
        from views.dashboard_view import DashboardView

        self.dashboard = DashboardView(self.dados_usuario)
        self.dashboard.show()
        self.close()