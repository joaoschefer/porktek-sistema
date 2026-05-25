from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QMessageBox
)
from PySide6.QtCore import Qt
from datetime import date
from services.lote_service import cadastrar_racao


class RacaoView(QWidget):
    def __init__(self, lote_id, tela_lote):
        super().__init__()

        self.lote_id = lote_id
        self.tela_lote = tela_lote

        self.setWindowTitle("Registrar ração")
        self.setFixedSize(500, 500)

        self.titulo = QLabel("Registrar ração")
        self.titulo.setObjectName("tituloLogin")
        self.titulo.setAlignment(Qt.AlignCenter)

        self.input_data = QLineEdit()
        self.input_tipo = QLineEdit()
        self.input_quantidade = QLineEdit()
        self.input_observacao = QLineEdit()

        self.input_data.setText(date.today().strftime("%d/%m/%Y"))
        self.input_tipo.setPlaceholderText("Tipo de ração")
        self.input_quantidade.setPlaceholderText("Quantidade em kg")
        self.input_observacao.setPlaceholderText("Observação")

        self.botao_salvar = QPushButton("Salvar ração")
        self.botao_cancelar = QPushButton("Cancelar")
        self.botao_cancelar.setObjectName("botaoSecundario")

        layout = QVBoxLayout()
        layout.setContentsMargins(35, 25, 35, 25)
        layout.setSpacing(12)

        layout.addWidget(self.titulo)
        layout.addWidget(self.input_data)
        layout.addWidget(self.input_tipo)
        layout.addWidget(self.input_quantidade)
        layout.addWidget(self.input_observacao)
        layout.addWidget(self.botao_salvar)
        layout.addWidget(self.botao_cancelar)

        self.setLayout(layout)

        self.botao_salvar.clicked.connect(self.salvar)
        self.botao_cancelar.clicked.connect(self.close)

    def salvar(self):
        try:
            data = self.input_data.text().strip()
            tipo = self.input_tipo.text().strip()
            quantidade_kg = float(self.input_quantidade.text().replace(",", "."))
            observacao = self.input_observacao.text().strip()

            sucesso, mensagem = cadastrar_racao(
                self.lote_id, data, tipo, quantidade_kg, observacao
            )

            if sucesso:
                QMessageBox.information(self, "Sucesso", mensagem)
                self.tela_lote.carregar_lote()
                self.close()
            else:
                QMessageBox.warning(self, "Erro", mensagem)

        except ValueError:
            QMessageBox.warning(self, "Atenção", "Informe a quantidade corretamente.")