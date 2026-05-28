from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QPushButton, QFrame, QMessageBox, QTabWidget,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QGridLayout, QScrollArea, QSizePolicy
)
from PySide6.QtCore import Qt
from services.lote_service import (
    buscar_lote_ativo,
    buscar_lote_por_id,
    buscar_historico_lote,
    buscar_resumo_lote,
    excluir_movimentacao,
    finalizar_lote
)
from config.window_config import (
    DEFAULT_WIDTH,
    DEFAULT_HEIGHT,
    DEFAULT_MIN_WIDTH,
    DEFAULT_MIN_HEIGHT
)
from datetime import date


class LoteAtualView(QWidget):
    def __init__(self, dados_usuario, lote_id=None, somente_leitura=False):
        super().__init__()

        self.dados_usuario = dados_usuario
        self.lote_id = lote_id
        self.lote_consulta_id = lote_id
        self.somente_leitura = somente_leitura
        self.historico = {
            "chegadas": [],
            "mortes": [],
            "racoes": [],
            "saidas": []
        }

        titulo_janela = "Sistema de Suínos - Detalhe do Lote" if self.somente_leitura else "Sistema de Suínos - Lote Ativo"
        self.setWindowTitle(titulo_janela)
        self.resize(DEFAULT_WIDTH, DEFAULT_HEIGHT)
        self.setMinimumSize(DEFAULT_MIN_WIDTH, DEFAULT_MIN_HEIGHT)

        self.montar_interface()
        self.carregar_lote()

    def montar_interface(self):
        layout_raiz = QVBoxLayout()
        layout_raiz.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        conteudo = QWidget()
        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(30, 25, 30, 25)
        layout_principal.setSpacing(22)

        header_layout = QHBoxLayout()

        textos_header = QVBoxLayout()
        textos_header.setSpacing(4)

        titulo = "Detalhe do lote finalizado" if self.somente_leitura else "Lote ativo"
        self.titulo = QLabel(titulo)
        self.titulo.setObjectName("tituloDashboard")

        subtitulo = "Consulte o resumo e o histórico completo deste lote."
        if not self.somente_leitura:
            subtitulo = "Gerencie chegadas, mortes, ração, saídas e finalização do lote atual."
        self.subtitulo = QLabel(subtitulo)
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

        cards_layout = QGridLayout()
        cards_layout.setSpacing(12)

        self.card_nome = self.criar_card("Nome do lote", "-")
        self.card_qtd_inicial = self.criar_card("Qtd. inicial", "-")
        self.card_qtd_atual = self.criar_card("Qtd. atual", "-")
        self.card_peso = self.criar_card("Peso médio", "-")

        cards_layout.addWidget(self.card_nome["frame"], 0, 0)
        cards_layout.addWidget(self.card_qtd_inicial["frame"], 0, 1)
        cards_layout.addWidget(self.card_qtd_atual["frame"], 1, 0)
        cards_layout.addWidget(self.card_peso["frame"], 1, 1)
        cards_layout.setColumnStretch(0, 1)
        cards_layout.setColumnStretch(1, 1)

        layout_principal.addLayout(cards_layout)

        area_central = QHBoxLayout()
        area_central.setSpacing(18)

        painel_info = QFrame()
        painel_info.setObjectName("painelDashboard")

        info_layout = QVBoxLayout()
        info_layout.setSpacing(14)

        titulo_info = QLabel("Informações do lote")
        titulo_info.setObjectName("secaoDashboard")

        self.label_codigo = QLabel("Código: -")
        self.label_data = QLabel("Data de chegada: -")
        self.label_status = QLabel("Status: -")
        self.label_finalizacao = QLabel("Data de finalização: -")
        self.label_peso = QLabel("Peso médio atual: -")
        self.label_mortalidade = QLabel("Mortalidade: -")
        self.label_racao = QLabel("Ração consumida: -")
        self.label_racao_animal = QLabel("Ração por animal: -")
        self.label_saidas = QLabel("Saídas: -")

        for label in (
            self.label_codigo,
            self.label_data,
            self.label_status,
            self.label_finalizacao,
            self.label_peso,
            self.label_mortalidade,
            self.label_racao,
            self.label_racao_animal,
            self.label_saidas
        ):
            label.setObjectName("textoInfoDashboard")

        info_layout.addWidget(titulo_info)
        info_layout.addWidget(self.label_codigo)
        info_layout.addWidget(self.label_data)
        info_layout.addWidget(self.label_status)
        info_layout.addWidget(self.label_finalizacao)
        info_layout.addWidget(self.label_peso)
        info_layout.addWidget(self.label_mortalidade)
        info_layout.addWidget(self.label_racao)
        info_layout.addWidget(self.label_racao_animal)
        info_layout.addWidget(self.label_saidas)
        info_layout.addStretch()

        painel_info.setLayout(info_layout)

        self.painel_acoes = QFrame()
        self.painel_acoes.setObjectName("painelDashboard")

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

        for botao in (
            self.botao_chegada,
            self.botao_morte,
            self.botao_racao,
            self.botao_saida,
            self.botao_finalizar
        ):
            botao.setMinimumHeight(44)

        acoes_layout.addWidget(titulo_acoes)
        acoes_layout.addWidget(texto_acoes)
        acoes_layout.addSpacing(8)
        acoes_layout.addWidget(self.botao_chegada)
        acoes_layout.addWidget(self.botao_morte)
        acoes_layout.addWidget(self.botao_racao)
        acoes_layout.addWidget(self.botao_saida)
        acoes_layout.addWidget(self.botao_finalizar)
        acoes_layout.addStretch()

        self.painel_acoes.setLayout(acoes_layout)

        area_central.addWidget(painel_info, 2)
        area_central.addWidget(self.painel_acoes, 1)

        layout_principal.addLayout(area_central)

        painel_historico = QFrame()
        painel_historico.setObjectName("painelDashboard")
        painel_historico.setMinimumHeight(500)
        painel_historico.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        historico_layout = QVBoxLayout()
        historico_layout.setSpacing(12)

        titulo_historico = QLabel("Histórico do lote")
        titulo_historico.setObjectName("secaoDashboard")

        self.abas_historico = QTabWidget()
        self.abas_historico.setMinimumHeight(280)
        self.abas_historico.setMaximumHeight(340)
        self.abas_historico.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

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

        botoes_historico = QHBoxLayout()
        botoes_historico.setContentsMargins(0, 12, 0, 0)
        botoes_historico.addStretch()

        self.botao_editar = QPushButton("Editar selecionado")
        self.botao_excluir = QPushButton("Excluir selecionado")
        self.botao_editar.setObjectName("botaoSecundario")
        self.botao_excluir.setObjectName("botaoSair")
        self.botao_editar.setMinimumHeight(38)
        self.botao_excluir.setMinimumHeight(38)

        botoes_historico.addWidget(self.botao_editar)
        botoes_historico.addWidget(self.botao_excluir)

        historico_layout.addWidget(titulo_historico)
        historico_layout.addWidget(self.abas_historico)
        historico_layout.addLayout(botoes_historico)

        painel_historico.setLayout(historico_layout)
        layout_principal.addWidget(painel_historico, 2)

        conteudo.setLayout(layout_principal)
        scroll.setWidget(conteudo)
        layout_raiz.addWidget(scroll)

        self.setLayout(layout_raiz)

        self.botao_chegada.clicked.connect(self.abrir_chegada)
        self.botao_morte.clicked.connect(self.abrir_morte)
        self.botao_racao.clicked.connect(self.abrir_racao)
        self.botao_saida.clicked.connect(self.abrir_saida)
        self.botao_finalizar.clicked.connect(self.finalizar_lote_atual)
        self.botao_voltar.clicked.connect(self.voltar_dashboard)
        self.botao_editar.clicked.connect(self.editar_movimentacao)
        self.botao_excluir.clicked.connect(self.excluir_movimentacao_selecionada)

        if self.somente_leitura:
            self.painel_acoes.hide()
            self.botao_editar.hide()
            self.botao_excluir.hide()

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
        tabela.setMinimumHeight(230)
        tabela.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        tabela.setColumnCount(len(colunas) + 1)
        tabela.setHorizontalHeaderLabels(["ID"] + colunas)
        tabela.hideColumn(0)
        tabela.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        tabela.verticalHeader().setVisible(False)
        tabela.setEditTriggers(QTableWidget.NoEditTriggers)
        tabela.setSelectionBehavior(QTableWidget.SelectRows)
        tabela.setAlternatingRowColors(True)

        return tabela

    def carregar_lote(self):
        lote = buscar_lote_por_id(self.lote_consulta_id) if self.lote_consulta_id else buscar_lote_ativo()

        if lote:
            self.lote_id = lote[0]

            nome = lote[1]
            data_chegada = lote[2]
            qtd_inicial = lote[3]
            qtd_atual = lote[4]
            peso_medio = lote[5] if lote[5] is not None else 0
            status = lote[6]
            data_finalizacao = lote[7] if len(lote) > 7 else None

            self.card_nome["valor"].setText(str(nome))
            self.card_qtd_inicial["valor"].setText(str(qtd_inicial))
            self.card_qtd_atual["valor"].setText(str(qtd_atual))
            self.card_peso["valor"].setText(f"{peso_medio} kg")

            data_chegada_texto = data_chegada if data_chegada else "Aguardando primeira chegada"
            self.label_codigo.setText(f"Código: {nome}")
            self.label_data.setText(f"Data de chegada: {data_chegada_texto}")
            self.label_status.setText(f"Status: {status}")
            data_finalizacao_texto = data_finalizacao if data_finalizacao else "-"
            self.label_finalizacao.setText(f"Data de finalização: {data_finalizacao_texto}")
            self.label_peso.setText(f"Peso médio atual: {peso_medio} kg")

            self.carregar_historico()
            self.carregar_resumo()

        else:
            self.lote_id = None

            self.card_nome["valor"].setText("-")
            self.card_qtd_inicial["valor"].setText("-")
            self.card_qtd_atual["valor"].setText("-")
            self.card_peso["valor"].setText("-")

            self.label_codigo.setText("Código: -")
            self.label_data.setText("Data de chegada: -")
            self.label_status.setText("Status: -")
            self.label_finalizacao.setText("Data de finalização: -")
            self.label_peso.setText("Peso médio atual: -")
            self.label_mortalidade.setText("Mortalidade: -")
            self.label_racao.setText("Ração consumida: -")
            self.label_racao_animal.setText("Ração por animal: -")
            self.label_saidas.setText("Saídas: -")

            self.limpar_historico()

    def carregar_historico(self):
        if not self.lote_id:
            return

        self.historico = buscar_historico_lote(self.lote_id)

        self.preencher_tabela(self.tabela_chegadas, self.historico["chegadas"])
        self.preencher_tabela(self.tabela_mortes, self.historico["mortes"])
        self.preencher_tabela(self.tabela_racoes, self.historico["racoes"])
        self.preencher_tabela(self.tabela_saidas, self.historico["saidas"])

    def carregar_resumo(self):
        resumo = buscar_resumo_lote(self.lote_id)

        if not resumo:
            return

        self.label_mortalidade.setText(
            f"Mortalidade: {resumo['mortes']} ({resumo['mortalidade_percentual']}%)"
        )
        self.label_racao.setText(f"Ração consumida: {resumo['total_racao']} kg")
        self.label_racao_animal.setText(f"Ração por animal: {resumo['racao_por_animal']} kg")
        self.label_saidas.setText(
            f"Saídas: {resumo['total_saidas']} | Peso médio saída: {resumo['peso_medio_saida']} kg"
        )

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

    def tipo_historico_atual(self):
        indice = self.abas_historico.currentIndex()
        tipos = ["chegadas", "mortes", "racoes", "saidas"]
        return tipos[indice]

    def tabela_historico_atual(self):
        indice = self.abas_historico.currentIndex()
        tabelas = [
            self.tabela_chegadas,
            self.tabela_mortes,
            self.tabela_racoes,
            self.tabela_saidas
        ]
        return tabelas[indice]

    def registro_selecionado(self):
        tipo = self.tipo_historico_atual()
        tabela = self.tabela_historico_atual()
        linha = tabela.currentRow()

        if linha < 0:
            QMessageBox.warning(self, "Atenção", "Selecione um registro do histórico.")
            return None, None

        registro_id = int(tabela.item(linha, 0).text())

        for registro in self.historico[tipo]:
            if registro[0] == registro_id:
                return tipo, registro

        QMessageBox.warning(self, "Atenção", "Registro selecionado não encontrado.")
        return None, None

    def editar_movimentacao(self):
        tipo, registro = self.registro_selecionado()

        if not registro:
            return

        if tipo == "chegadas":
            from views.chegada_view import ChegadaView
            self.janela_edicao = ChegadaView(self.lote_id, self, registro)
        elif tipo == "mortes":
            from views.morte_view import MorteView
            self.janela_edicao = MorteView(self.lote_id, self, registro)
        elif tipo == "racoes":
            from views.racao_view import RacaoView
            self.janela_edicao = RacaoView(self.lote_id, self, registro)
        else:
            from views.saida_view import SaidaView
            self.janela_edicao = SaidaView(self.lote_id, self, registro)

        self.janela_edicao.show()

    def excluir_movimentacao_selecionada(self):
        tipo, registro = self.registro_selecionado()

        if not registro:
            return

        confirmacao = QMessageBox.question(
            self,
            "Excluir registro",
            "Tem certeza que deseja excluir o registro selecionado?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirmacao == QMessageBox.No:
            return

        sucesso, mensagem = excluir_movimentacao(tipo, registro[0], self.lote_id)

        if sucesso:
            QMessageBox.information(self, "Sucesso", mensagem)
            self.carregar_lote()
        else:
            QMessageBox.warning(self, "Erro", mensagem)

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
