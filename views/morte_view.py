from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QMessageBox, QComboBox
)
from PySide6.QtCore import Qt
from datetime import date
from services.lote_service import (
    cadastrar_morte,
    atualizar_morte,
    buscar_mossas_lote
)


CAUSAS_MORTE = [
    "Pneumonia",
    "Torcao",
    "Descartado",
    "Canibalismo",
    "Problema locomotor",
    "Prolapso",
    "Morte subita",
    "Outro"
]


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
        self.input_mossa = QComboBox()
        self.input_causa = QComboBox()
        self.input_observacao = QLineEdit()

        self.input_data.setText(date.today().strftime("%d/%m/%Y"))
        self.carregar_mossas()
        self.input_causa.setEditable(True)
        self.input_causa.addItems(CAUSAS_MORTE)
        self.input_causa.setCurrentIndex(-1)
        self.input_observacao.setPlaceholderText("Observacao")

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
            self.selecionar_mossa(mossa)
            self.input_causa.setCurrentText(str(causa or ""))
            self.input_observacao.setText(str(observacao or ""))

    def carregar_mossas(self):
        self.input_mossa.addItem("Selecione a mossa", None)

        for mossa in buscar_mossas_lote(self.lote_id):
            self.input_mossa.addItem(str(mossa), mossa)

    def selecionar_mossa(self, mossa):
        indice = self.input_mossa.findData(mossa)

        if indice < 0:
            self.input_mossa.addItem(str(mossa), mossa)
            indice = self.input_mossa.findData(mossa)

        self.input_mossa.setCurrentIndex(indice)

    def salvar(self):
        data = self.input_data.text().strip()
        mossa = self.input_mossa.currentData()
        causa = self.input_causa.currentText().strip()
        observacao = self.input_observacao.text().strip()

        if mossa is None:
            QMessageBox.warning(self, "Atencao", "Selecione a mossa.")
            return

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
