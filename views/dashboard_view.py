from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QFrame, QHeaderView
)
from PySide6.QtCore import Qt
from database import conectar
from config.window_config import (
    DEFAULT_WIDTH,
    DEFAULT_HEIGHT,
    DEFAULT_MIN_WIDTH,
    DEFAULT_MIN_HEIGHT
)


class DashboardView(QWidget):
    def __init__(self, dados_usuario):
        super().__init__()

        self.dados_usuario = dados_usuario

        self.setWindowTitle("Sistema de Suínos - Dashboard")
        self.resize(DEFAULT_WIDTH, DEFAULT_HEIGHT)
        self.setMinimumSize(DEFAULT_MIN_WIDTH, DEFAULT_MIN_HEIGHT)

        self.montar_interface()

        self.botao_sair.clicked.connect(self.sair)
        self.botao_criar_lote.clicked.connect(self.abrir_criar_lote)
        self.botao_acessar_lote.clicked.connect(self.abrir_lote_ativo)

        self.carregar_lote_ativo()
        self.carregar_lotes_finalizados()

    def montar_interface(self):
        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(30, 25, 30, 25)
        layout_principal.setSpacing(20)

        # Cabeçalho
        header_layout = QHBoxLayout()

        textos_header = QVBoxLayout()

        self.titulo = QLabel(f"Bem-vindo, {self.dados_usuario[1]}")
        self.titulo.setObjectName("tituloDashboard")

        self.subtitulo = QLabel("Acompanhe o lote ativo e o histórico de lotes finalizados.")
        self.subtitulo.setObjectName("subtituloDashboard")

        textos_header.addWidget(self.titulo)
        textos_header.addWidget(self.subtitulo)

        self.botao_sair = QPushButton("Sair")
        self.botao_sair.setObjectName("botaoSair")

        header_layout.addLayout(textos_header)
        header_layout.addStretch()
        header_layout.addWidget(self.botao_sair)

        layout_principal.addLayout(header_layout)

        # Painel lote ativo
        self.painel_lote = QFrame()
        self.painel_lote.setObjectName("painelDashboard")

        painel_layout = QVBoxLayout()
        painel_layout.setSpacing(15)

        titulo_lote = QLabel("Lote ativo")
        titulo_lote.setObjectName("secaoDashboard")

        self.lote_ativo_label = QLabel("Nenhum lote ativo encontrado.")
        self.lote_ativo_label.setObjectName("textoInfoDashboard")

        painel_layout.addWidget(titulo_lote)
        painel_layout.addWidget(self.lote_ativo_label)

        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(12)

        self.card_codigo = self.criar_card("Código", "-")
        self.card_qtd_inicial = self.criar_card("Qtd. inicial", "-")
        self.card_qtd_atual = self.criar_card("Qtd. atual", "-")
        self.card_peso = self.criar_card("Peso médio", "-")

        cards_layout.addWidget(self.card_codigo["frame"])
        cards_layout.addWidget(self.card_qtd_inicial["frame"])
        cards_layout.addWidget(self.card_qtd_atual["frame"])
        cards_layout.addWidget(self.card_peso["frame"])

        painel_layout.addLayout(cards_layout)

        self.painel_lote.setLayout(painel_layout)
        layout_principal.addWidget(self.painel_lote)

        botoes_layout = QHBoxLayout()
        botoes_layout.setSpacing(10)

        self.botao_acessar_lote = QPushButton("Acessar lote ativo")
        self.botao_criar_lote = QPushButton("Criar lote")

        self.botao_acessar_lote.setObjectName("botaoSecundario")

        botoes_layout.addWidget(self.botao_acessar_lote)
        botoes_layout.addWidget(self.botao_criar_lote)

        layout_principal.addLayout(botoes_layout)


        # Tabela de lotes finalizados
        titulo_finalizados = QLabel("Lotes finalizados")
        titulo_finalizados.setObjectName("secaoDashboard")
        layout_principal.addWidget(titulo_finalizados)

        self.tabela_lotes = QTableWidget()
        self.tabela_lotes.setObjectName("tabelaDashboard")
        self.tabela_lotes.setColumnCount(6)
        self.tabela_lotes.setHorizontalHeaderLabels([
            "Código",
            "Data chegada",
            "Data finalização",
            "Qtd inicial",
            "Qtd atual",
            "Status"
        ])

        self.tabela_lotes.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabela_lotes.verticalHeader().setVisible(False)
        self.tabela_lotes.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabela_lotes.setSelectionBehavior(QTableWidget.SelectRows)

        layout_principal.addWidget(self.tabela_lotes)

        self.setLayout(layout_principal)

    def criar_card(self, titulo, valor):
        frame = QFrame()
        frame.setObjectName("cardDashboard")

        layout = QVBoxLayout()
        layout.setSpacing(6)

        label_titulo = QLabel(titulo)
        label_titulo.setObjectName("tituloCardDashboard")

        label_valor = QLabel(valor)
        label_valor.setObjectName("valorCardDashboard")

        layout.addWidget(label_titulo)
        layout.addWidget(label_valor)

        frame.setLayout(layout)

        return {
            "frame": frame,
            "valor": label_valor
        }

    def carregar_lote_ativo(self):
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT codigo, data_chegada, quantidade_inicial, quantidade_atual, peso_medio_atual
            FROM lotes
            WHERE status = 'ativo'
            LIMIT 1
        """)

        lote = cursor.fetchone()
        conexao.close()

        if lote:
            codigo = lote[0]
            data_chegada = lote[1]
            qtd_inicial = lote[2]
            qtd_atual = lote[3]
            peso_medio = lote[4] if lote[4] is not None else 0

            texto = "Aguardando primeira chegada"
            if data_chegada:
                texto = f"Lote iniciado em {data_chegada}"

            self.lote_ativo_label.setText(texto)
            self.card_codigo["valor"].setText(str(codigo))
            self.card_qtd_inicial["valor"].setText(str(qtd_inicial))
            self.card_qtd_atual["valor"].setText(str(qtd_atual))
            self.card_peso["valor"].setText(f"{peso_medio} kg")
        else:
            self.lote_ativo_label.setText("Nenhum lote ativo encontrado.")
            self.card_codigo["valor"].setText("-")
            self.card_qtd_inicial["valor"].setText("-")
            self.card_qtd_atual["valor"].setText("-")
            self.card_peso["valor"].setText("-")

    def abrir_criar_lote(self):
        from views.create_lote_view import CreateLoteView

        self.create_lote_view = CreateLoteView(self)
        self.create_lote_view.show()

    def abrir_lote_ativo(self):
        from services.lote_service import buscar_lote_ativo
        from views.lote_atual_view import LoteAtualView
        from PySide6.QtWidgets import QMessageBox

        lote_ativo = buscar_lote_ativo()

        if not lote_ativo:
            QMessageBox.warning(self, "Atenção", "Nenhum lote ativo encontrado.")
            return

        self.lote_atual_view = LoteAtualView(self.dados_usuario)
        self.lote_atual_view.showMaximized()
        self.close()

    def carregar_lotes_finalizados(self):
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT codigo, data_chegada, data_finalizacao, quantidade_inicial, quantidade_atual, status
            FROM lotes
            WHERE status = 'finalizado'
        """)

        lotes = cursor.fetchall()
        conexao.close()

        self.tabela_lotes.setRowCount(len(lotes))

        for linha, lote in enumerate(lotes):
            for coluna, valor in enumerate(lote):
                item = QTableWidgetItem(str(valor if valor is not None else ""))
                item.setTextAlignment(Qt.AlignCenter)
                self.tabela_lotes.setItem(linha, coluna, item)

    def sair(self):
        from views.login_view import LoginView

        self.login = LoginView()
        self.login.show()
        self.close()
