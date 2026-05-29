from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QIntValidator
from datetime import date
from services.lote_service import cadastrar_chegada, atualizar_chegada


class ChegadaView(QWidget):
    def __init__(self, lote_id, tela_lote, registro=None):
        super().__init__()

        self.lote_id = lote_id
        self.tela_lote = tela_lote
        self.registro = registro

        self.setWindowTitle("Editar chegada" if self.registro else "Cadastrar chegada")
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, False)
        self.setFixedSize(500, 560)

        self.titulo = QLabel("Editar chegada" if self.registro else "Cadastrar chegada")
        self.titulo.setObjectName("tituloLogin")
        self.titulo.setAlignment(Qt.AlignCenter)

        self.input_data = QLineEdit()
        self.input_mossa = QLineEdit()
        self.input_quantidade = QLineEdit()
        self.input_peso_total = QLineEdit()
        self.input_peso_medio = QLineEdit()
        self.input_observacao = QLineEdit()

        self.input_data.setText(date.today().strftime("%d/%m/%Y"))
        self.input_mossa.setValidator(QIntValidator(0, 999999, self))
        self.input_quantidade.setValidator(QIntValidator(0, 999999, self))
        self.input_mossa.setPlaceholderText("Numero da mossa")
        self.input_quantidade.setPlaceholderText("Quantidade de suinos")
        self.input_peso_total.setPlaceholderText("Peso total da carga")
        self.input_peso_medio.setPlaceholderText("Peso medio inicial calculado")
        self.input_peso_medio.setReadOnly(True)
        self.input_observacao.setPlaceholderText("Observacao")

        self.botao_salvar = QPushButton("Salvar chegada")
        self.botao_cancelar = QPushButton("Cancelar")
        self.botao_cancelar.setObjectName("botaoSecundario")

        layout = QVBoxLayout()
        layout.setContentsMargins(35, 25, 35, 25)
        layout.setSpacing(12)

        layout.addWidget(self.titulo)
        layout.addWidget(self.input_data)
        layout.addWidget(self.input_mossa)
        layout.addWidget(self.input_quantidade)
        layout.addWidget(self.input_peso_total)
        layout.addWidget(self.input_peso_medio)
        layout.addWidget(self.input_observacao)
        layout.addWidget(self.botao_salvar)
        layout.addWidget(self.botao_cancelar)

        self.setLayout(layout)

        self.botao_salvar.clicked.connect(self.salvar)
        self.botao_cancelar.clicked.connect(self.close)
        self.input_quantidade.textChanged.connect(self.atualizar_peso_medio)
        self.input_peso_total.textChanged.connect(self.atualizar_peso_medio)

        if self.registro:
            _, data, mossa, quantidade, peso_total, peso_medio, observacao = self.registro
            self.input_data.setText(str(data))
            self.input_mossa.setText(str(mossa or ""))
            self.input_quantidade.setText(str(quantidade))
            self.input_peso_total.setText(str(peso_total if peso_total is not None else ""))
            self.input_peso_medio.setText(str(peso_medio))
            self.input_observacao.setText(str(observacao or ""))

    def atualizar_peso_medio(self):
        try:
            quantidade = int(self.input_quantidade.text())
            peso_total = float(self.input_peso_total.text().replace(",", "."))

            if quantidade > 0 and peso_total > 0:
                self.input_peso_medio.setText(f"{peso_total / quantidade:.2f}")
            else:
                self.input_peso_medio.clear()
        except ValueError:
            self.input_peso_medio.clear()

    def salvar(self):
        try:
            data = self.input_data.text().strip()
            mossa = int(self.input_mossa.text())
            quantidade = int(self.input_quantidade.text())
            peso_total = float(self.input_peso_total.text().replace(",", "."))
            observacao = self.input_observacao.text().strip()

            if self.registro:
                sucesso, mensagem = atualizar_chegada(
                    self.registro[0], self.lote_id, data, mossa, quantidade, peso_total, observacao
                )
            else:
                sucesso, mensagem = cadastrar_chegada(
                    self.lote_id, data, mossa, quantidade, peso_total, observacao
                )

            if sucesso:
                QMessageBox.information(self, "Sucesso", mensagem)
                self.tela_lote.carregar_lote()
                self.close()
            else:
                QMessageBox.warning(self, "Erro", mensagem)

        except ValueError:
            QMessageBox.warning(self, "Atencao", "Preencha mossa, quantidade e peso total corretamente.")
