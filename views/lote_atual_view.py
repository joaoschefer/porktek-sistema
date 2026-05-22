from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QFrame
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
        self.lote_id = None

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

        botoes_layout = QHBoxLayout()
        botoes_layout.setSpacing(10)

        self.botao_chegada = QPushButton("Cadastrar chegada")
        self.botao_morte = QPushButton("Registrar morte")
        self.botao_racao = QPushButton("Registrar ração")
        self.botao_saida = QPushButton("Cadastrar saída")

        self.botao_chegada.setObjectName("botaoSecundario")
        self.botao_morte.setObjectName("botaoSecundario")
        self.botao_racao.setObjectName("botaoSecundario")

        botoes_layout.addWidget(self.botao_chegada)
        botoes_layout.addWidget(self.botao_morte)
        botoes_layout.addWidget(self.botao_racao)
        botoes_layout.addWidget(self.botao_saida)

        self.botao_voltar = QPushButton("Voltar ao dashboard")
        self.botao_voltar.setObjectName("botaoSecundario")

        layout.addWidget(self.titulo)
        layout.addWidget(self.card)
        layout.addLayout(botoes_layout)
        layout.addWidget(self.botao_voltar)

        self.setLayout(layout)

        self.botao_chegada.clicked.connect(self.abrir_chegada)
        self.botao_morte.clicked.connect(self.abrir_morte)
        self.botao_racao.clicked.connect(self.abrir_racao)
        self.botao_saida.clicked.connect(self.abrir_saida)
        self.botao_voltar.clicked.connect(self.voltar_dashboard)

    def carregar_lote(self):
        lote = buscar_lote_ativo()

        if lote:
            self.lote_id = lote[0]

            self.label_nome.setText(f"Nome: {lote[1]}")
            self.label_data.setText(f"Data de chegada: {lote[2]}")
            self.label_qtd_inicial.setText(f"Quantidade inicial: {lote[3]}")
            self.label_qtd_atual.setText(f"Quantidade atual: {lote[4]}")
            self.label_peso.setText(f"Peso médio: {lote[5]} kg")
            self.label_status.setText(f"Status: {lote[6]}")
        else:
            self.lote_id = None
            self.label_nome.setText("Nenhum lote ativo encontrado.")

    def abrir_chegada(self):
        from views.chegada_view import ChegadaView

        if self.lote_id:
            self.janela_chegada = ChegadaView(self.lote_id, self)
            self.janela_chegada.show()

    def abrir_morte(self):
        from views.morte_view import MorteView

        if self.lote_id:
            self.janela_morte = MorteView(self.lote_id, self)
            self.janela_morte.show()

    def abrir_racao(self):
        from views.racao_view import RacaoView

        if self.lote_id:
            self.janela_racao = RacaoView(self.lote_id, self)
            self.janela_racao.show()

    def abrir_saida(self):
        from views.saida_view import SaidaView

        if self.lote_id:
            self.janela_saida = SaidaView(self.lote_id, self)
            self.janela_saida.show()

    def voltar_dashboard(self):
        from views.dashboard_view import DashboardView

        self.dashboard = DashboardView(self.dados_usuario)
        self.dashboard.showMaximized()
        self.close()