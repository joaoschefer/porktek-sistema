from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIntValidator
from datetime import date
from services.lote_service import cadastrar_morte, atualizar_morte


class MorteView(QWidget):
    def __init__(self, lote_id, tela_lote, registro=None):
        super().__init__()

        self.lote_id = lote_id
        self.tela_lote = tela_lote
        self.registro = registro

        self.setWindowTitle("Editar morte" if self.registro else "Registrar morte")
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, False)
        self.setFixedSize(500, 500)

        self.titulo = QLabel("Editar morte" if self.registro else "Registrar morte")
        self.titulo.setObjectName("tituloLogin")
        self.titulo.setAlignment(Qt.AlignCenter)

        self.input_data = QLineEdit()
        self.input_mossa = QLineEdit()
        self.input_causa = QLineEdit()
        self.input_observacao = QLineEdit()

        self.input_data.setText(date.today().strftime("%d/%m/%Y"))
        self.input_mossa.setValidator(QIntValidator(0, 999999, self))
        self.input_mossa.setPlaceholderText("Número da mossa")
        self.input_causa.setPlaceholderText("Causa")
        self.input_observacao.setPlaceholderText("Observação")

        self.botao_salvar = QPushButton("Salvar morte")
        self.botao_cancelar = QPushButton("Cancelar")
        self.botao_cancelar.setObjectName("botaoSecundario")

        layout = QVBoxLayout()
        layout.setContentsMargins(35, 25, 35, 25)
        layout.setSpacing(12)

        layout.addWidget(self.titulo)
        layout.addWidget(self.input_data)
        layout.addWidget(self.input_mossa)
        layout.addWidget(self.input_causa)
        layout.addWidget(self.input_observacao)
        layout.addWidget(self.botao_salvar)
        layout.addWidget(self.botao_cancelar)

        self.setLayout(layout)

        self.botao_salvar.clicked.connect(self.salvar)
        self.botao_cancelar.clicked.connect(self.close)

        if self.registro:
            _, data, mossa, causa, observacao = self.registro
            self.input_data.setText(str(data))
            self.input_mossa.setText(str(mossa))
            self.input_causa.setText(str(causa or ""))
            self.input_observacao.setText(str(observacao or ""))

    def salvar(self):
        data = self.input_data.text().strip()
        mossa = self.input_mossa.text().strip()
        causa = self.input_causa.text().strip()
        observacao = self.input_observacao.text().strip()

        if mossa == "":
            QMessageBox.warning(self, "Atenção", "Informe o número da mossa.")
            return

        mossa = int(mossa)

        if self.registro:
            sucesso, mensagem = atualizar_morte(
                self.registro[0], self.lote_id, data, mossa, causa, observacao
            )
        else:
            sucesso, mensagem = cadastrar_morte(
                self.lote_id, data, mossa, causa, observacao
            )

        if sucesso:
            QMessageBox.information(self, "Sucesso", mensagem)
            self.tela_lote.carregar_lote()
            self.close()
        else:
            QMessageBox.warning(self, "Erro", mensagem)
