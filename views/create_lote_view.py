from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QMessageBox
)
from PySide6.QtCore import Qt
from services.lote_service import criar_lote


class CreateLoteView(QWidget):
    def __init__(self, dashboard):
        super().__init__()

        self.dashboard = dashboard

        self.setWindowTitle("Criar novo lote")
        self.setFixedSize(500, 500)

        self.titulo = QLabel("Criar novo lote")
        self.titulo.setObjectName("tituloLogin")
        self.titulo.setAlignment(Qt.AlignCenter)

        self.input_nome = QLineEdit()
        self.input_nome.setPlaceholderText("Nome do lote. Ex: Lote 001")

        self.botao_criar = QPushButton("Criar lote")
        self.botao_cancelar = QPushButton("Cancelar")
        self.botao_cancelar.setObjectName("botaoSecundario")

        layout = QVBoxLayout()
        layout.setContentsMargins(35, 25, 35, 25)
        layout.setSpacing(14)

        layout.addWidget(self.titulo)
        layout.addWidget(self.input_nome)
        layout.addWidget(self.botao_criar)
        layout.addWidget(self.botao_cancelar)

        self.setLayout(layout)

        self.botao_criar.clicked.connect(self.salvar_lote)
        self.botao_cancelar.clicked.connect(self.close)

    def salvar_lote(self):
        nome_lote = self.input_nome.text().strip()

        if nome_lote == "":
            QMessageBox.warning(self, "Atenção", "Informe o nome do lote.")
            return

        sucesso, mensagem = criar_lote(nome_lote)

        if sucesso:
            QMessageBox.information(self, "Sucesso", mensagem)

            self.dashboard.carregar_lote_ativo()
            self.dashboard.carregar_lotes_finalizados()

            self.close()
        else:
            QMessageBox.warning(self, "Erro", mensagem)