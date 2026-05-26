from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QPushButton, QFrame, QMessageBox, QTabWidget,
    QTableWidget, QTableWidgetItem, QHeaderView
)
from PySide6.QtCore import Qt
from services.lote_service import buscar_lote_ativo, finalizar_lote
from database import conectar
from config.window_config import (
    DEFAULT_WIDTH,
    DEFAULT_HEIGHT,
    DEFAULT_MIN_WIDTH,
    DEFAULT_MIN_HEIGHT
)
from datetime import date


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
        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(30, 25, 30, 25)
        layout_principal.setSpacing(22)

        # Cabeçalho
        header_layout = QHBoxLayout()

        textos_header = QVBoxLayout()
        textos_header.setSpacing(4)

        self.titulo = QLabel("Lote ativo")
        self.titulo.setObjectName("tituloDashboard")

        self.subtitulo = QLabel("Gerencie chegadas, mortes, ração, saídas e finalização do lote atual.")
        self.subtitulo.setObjectName("subtituloDashboard")

        textos_header.addWidget(self.titulo)
        textos_header.addWidget(self.subtitulo)

        self.botao_voltar = QPushButton("Voltar")
        self.botao_voltar.setObjectName("botaoSecundario")
        self.botao_voltar.setFixedWidth(120)
        self.botao_voltar.setMinimumHeight(42)

        header_layout.addLayout(textos_header)
        header_layout.addStretch()
        header_layout.addWidget(self.botao_voltar)

        layout_principal.addLayout(header_layout)

        # Cards principais
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(12)

        self.card_nome = self.criar_card("Nome do lote", "-")
        self.card_qtd_inicial = self.criar_card("Qtd. inicial", "-")
        self.card_qtd_atual = self.criar_card("Qtd. atual", "-")
        self.card_peso = self.criar_card("Peso médio", "-")

        cards_layout.addWidget(self.card_nome["frame"], 1)
        cards_layout.addWidget(self.card_qtd_inicial["frame"], 1)
        cards_layout.addWidget(self.card_qtd_atual["frame"], 1)
        cards_layout.addWidget(self.card_peso["frame"], 1)

        layout_principal.addLayout(cards_layout)

        # Área central
        area_central = QHBoxLayout()
        area_central.setSpacing(18)

        # Painel informações
        painel_info = QFrame()
        painel_info.setObjectName("painelDashboard")

        info_layout = QVBoxLayout()
        info_layout.setSpacing(14)

        titulo_info = QLabel("Informações do lote")
        titulo_info.setObjectName("secaoDashboard")

        self.label_codigo = QLabel("Código: -")
        self.label_data = QLabel("Data de chegada: -")
        self.label_status = QLabel("Status: -")
        self.label_peso = QLabel("Peso médio atual: -")

        self.label_codigo.setObjectName("textoInfoDashboard")
        self.label_data.setObjectName("textoInfoDashboard")
        self.label_status.setObjectName("textoInfoDashboard")
        self.label_peso.setObjectName("textoInfoDashboard")

        info_layout.addWidget(titulo_info)
        info_layout.addWidget(self.label_codigo)
        info_layout.addWidget(self.label_data)
        info_layout.addWidget(self.label_status)
        info_layout.addWidget(self.label_peso)
        info_layout.addStretch()

        painel_info.setLayout(info_layout)

        # Painel ações
        painel_acoes = QFrame()
        painel_acoes.setObjectName("painelDashboard")

        acoes_layout = QVBoxLayout()
        acoes_layout.setSpacing(14)

        titulo_acoes = QLabel("Ações rápidas")
        titulo_acoes.setObjectName("secaoDashboard")

        texto_acoes = QLabel("Cadastre movimentações ou finalize o lote atual.")
        texto_acoes.setObjectName("textoInfoDashboard")

        self.botao_chegada = QPushButton("Cadastrar chegada")
        self.botao_morte = QPushButton("Registrar morte")
        self.botao_racao = QPushButton("Registrar ração")
        self.botao_saida = QPushButton("Cadastrar saída")
        self.botao_finalizar = QPushButton("Finalizar lote")

        self.botao_chegada.setObjectName("botaoSecundario")
        self.botao_morte.setObjectName("botaoSecundario")
        self.botao_racao.setObjectName("botaoSecundario")
        self.botao_saida.setObjectName("botaoSecundario")
        self.botao_finalizar.setObjectName("botaoSair")

        self.botao_chegada.setMinimumHeight(44)
        self.botao_morte.setMinimumHeight(44)
        self.botao_racao.setMinimumHeight(44)
        self.botao_saida.setMinimumHeight(44)
        self.botao_finalizar.setMinimumHeight(44)

        acoes_layout.addWidget(titulo_acoes)
        acoes_layout.addWidget(texto_acoes)
        acoes_layout.addSpacing(8)
        acoes_layout.addWidget(self.botao_chegada)
        acoes_layout.addWidget(self.botao_morte)
        acoes_layout.addWidget(self.botao_racao)
        acoes_layout.addWidget(self.botao_saida)
        acoes_layout.addWidget(self.botao_finalizar)
        acoes_layout.addStretch()

        painel_acoes.setLayout(acoes_layout)

        area_central.addWidget(painel_info, 2)
        area_central.addWidget(painel_acoes, 1)

        layout_principal.addLayout(area_central)

        # Histórico do lote
        painel_historico = QFrame()
        painel_historico.setObjectName("painelDashboard")

        historico_layout = QVBoxLayout()
        historico_layout.setSpacing(12)

        titulo_historico = QLabel("Histórico do lote")
        titulo_historico.setObjectName("secaoDashboard")

        self.abas_historico = QTabWidget()

        self.tabela_chegadas = self.criar_tabela([
            "Data", "Quantidade", "Peso médio", "Observação"
        ])

        self.tabela_mortes = self.criar_tabela([
            "Data", "Mossa", "Causa", "Observação"
        ])

        self.tabela_racoes = self.criar_tabela([
            "Data", "Tipo", "Quantidade kg", "Observação"
        ])

        self.tabela_saidas = self.criar_tabela([
            "Data", "Quantidade", "Peso médio", "Observação"
        ])

        self.abas_historico.addTab(self.tabela_chegadas, "Chegadas")
        self.abas_historico.addTab(self.tabela_mortes, "Mortes")
        self.abas_historico.addTab(self.tabela_racoes, "Rações")
        self.abas_historico.addTab(self.tabela_saidas, "Saídas")

        historico_layout.addWidget(titulo_historico)
        historico_layout.addWidget(self.abas_historico)

        painel_historico.setLayout(historico_layout)

        layout_principal.addWidget(painel_historico, 1)

        self.setLayout(layout_principal)

        self.botao_chegada.clicked.connect(self.abrir_chegada)
        self.botao_morte.clicked.connect(self.abrir_morte)
        self.botao_racao.clicked.connect(self.abrir_racao)
        self.botao_saida.clicked.connect(self.abrir_saida)
        self.botao_finalizar.clicked.connect(self.finalizar_lote_atual)
        self.botao_voltar.clicked.connect(self.voltar_dashboard)

    def criar_card(self, titulo, valor):
        frame = QFrame()
        frame.setObjectName("cardDashboard")
        frame.setMinimumHeight(110)

        layout = QVBoxLayout()
        layout.setSpacing(6)

        label_titulo = QLabel(titulo)
        label_titulo.setObjectName("tituloCardDashboard")

        label_valor = QLabel(valor)
        label_valor.setObjectName("valorCardDashboard")

        layout.addWidget(label_titulo)
        layout.addWidget(label_valor)
        layout.addStretch()

        frame.setLayout(layout)

        return {
            "frame": frame,
            "valor": label_valor
        }

    def criar_tabela(self, colunas):
        tabela = QTableWidget()
        tabela.setObjectName("tabelaDashboard")
        tabela.setColumnCount(len(colunas))
        tabela.setHorizontalHeaderLabels(colunas)

        tabela.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        tabela.verticalHeader().setVisible(False)
        tabela.setEditTriggers(QTableWidget.NoEditTriggers)
        tabela.setSelectionBehavior(QTableWidget.SelectRows)

        return tabela

    def carregar_lote(self):
        lote = buscar_lote_ativo()

        if lote:
            self.lote_id = lote[0]

            nome = lote[1]
            data_chegada = lote[2]
            qtd_inicial = lote[3]
            qtd_atual = lote[4]
            peso_medio = lote[5] if lote[5] is not None else 0
            status = lote[6]

            self.card_nome["valor"].setText(str(nome))
            self.card_qtd_inicial["valor"].setText(str(qtd_inicial))
            self.card_qtd_atual["valor"].setText(str(qtd_atual))
            self.card_peso["valor"].setText(f"{peso_medio} kg")

            self.label_codigo.setText(f"Código: {nome}")
            data_chegada_texto = data_chegada if data_chegada else "Aguardando primeira chegada"
            self.label_data.setText(f"Data de chegada: {data_chegada_texto}")
            self.label_status.setText(f"Status: {status}")
            self.label_peso.setText(f"Peso médio atual: {peso_medio} kg")

            self.carregar_historico()

        else:
            self.lote_id = None

            self.card_nome["valor"].setText("-")
            self.card_qtd_inicial["valor"].setText("-")
            self.card_qtd_atual["valor"].setText("-")
            self.card_peso["valor"].setText("-")

            self.label_codigo.setText("Código: -")
            self.label_data.setText("Data de chegada: -")
            self.label_status.setText("Status: -")
            self.label_peso.setText("Peso médio atual: -")

            self.limpar_historico()

    def carregar_historico(self):
        if not self.lote_id:
            return

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT data, quantidade, peso_medio, observacao
            FROM chegadas
            WHERE lote_id = ?
            ORDER BY id DESC
        """, (self.lote_id,))
        chegadas = cursor.fetchall()

        cursor.execute("""
            SELECT data, mossa, causa, observacao
            FROM mortes
            WHERE lote_id = ?
            ORDER BY id DESC
        """, (self.lote_id,))
        mortes = cursor.fetchall()

        cursor.execute("""
            SELECT data, tipo, quantidade_kg, observacao
            FROM racoes
            WHERE lote_id = ?
            ORDER BY id DESC
        """, (self.lote_id,))
        racoes = cursor.fetchall()

        cursor.execute("""
            SELECT data, quantidade, peso_medio, observacao
            FROM saidas
            WHERE lote_id = ?
            ORDER BY id DESC
        """, (self.lote_id,))
        saidas = cursor.fetchall()

        conexao.close()

        self.preencher_tabela(self.tabela_chegadas, chegadas)
        self.preencher_tabela(self.tabela_mortes, mortes)
        self.preencher_tabela(self.tabela_racoes, racoes)
        self.preencher_tabela(self.tabela_saidas, saidas)

    def preencher_tabela(self, tabela, dados):
        tabela.setRowCount(len(dados))

        for linha, registro in enumerate(dados):
            for coluna, valor in enumerate(registro):
                item = QTableWidgetItem(str(valor if valor is not None else ""))
                item.setTextAlignment(Qt.AlignCenter)
                tabela.setItem(linha, coluna, item)

    def limpar_historico(self):
        self.tabela_chegadas.setRowCount(0)
        self.tabela_mortes.setRowCount(0)
        self.tabela_racoes.setRowCount(0)
        self.tabela_saidas.setRowCount(0)

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

    def finalizar_lote_atual(self):
        if not self.lote_id:
            QMessageBox.warning(self, "Atenção", "Nenhum lote ativo encontrado.")
            return

        confirmacao = QMessageBox.question(
            self,
            "Finalizar lote",
            "Tem certeza que deseja finalizar este lote?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirmacao == QMessageBox.No:
            return

        data_finalizacao = date.today().strftime("%d/%m/%Y")

        sucesso, mensagem = finalizar_lote(self.lote_id, data_finalizacao)

        if sucesso:
            QMessageBox.information(self, "Sucesso", mensagem)
            self.voltar_dashboard()
        else:
            QMessageBox.warning(self, "Erro", mensagem)

    def voltar_dashboard(self):
        from views.dashboard_view import DashboardView

        self.dashboard = DashboardView(self.dados_usuario)
        self.dashboard.showMaximized()
        self.close()
