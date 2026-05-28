from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PySide6.QtCore import Qt
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
        self.setFixedSize(500, 500)

        self.titulo = QLabel("Editar chegada" if self.registro else "Cadastrar chegada")
        self.titulo.setObjectName("tituloLogin")
        self.titulo.setAlignment(Qt.AlignCenter)

        self.input_data = QLineEdit()
        self.input_quantidade = QLineEdit()
        self.input_peso = QLineEdit()
        self.input_observacao = QLineEdit()

        self.input_data.setText(date.today().strftime("%d/%m/%Y"))
        self.input_quantidade.setPlaceholderText("Quantidade de suínos")
        self.input_peso.setPlaceholderText("Peso médio inicial")
        self.input_observacao.setPlaceholderText("Observação")

        self.botao_salvar = QPushButton("Salvar chegada")
        self.botao_cancelar = QPushButton("Cancelar")
        self.botao_cancelar.setObjectName("botaoSecundario")

        layout = QVBoxLayout()
        layout.setContentsMargins(35, 25, 35, 25)
        layout.setSpacing(12)

        layout.addWidget(self.titulo)
        layout.addWidget(self.input_data)
        layout.addWidget(self.input_quantidade)
        layout.addWidget(self.input_peso)
        layout.addWidget(self.input_observacao)
        layout.addWidget(self.botao_salvar)
        layout.addWidget(self.botao_cancelar)

        self.setLayout(layout)

        self.botao_salvar.clicked.connect(self.salvar)
        self.botao_cancelar.clicked.connect(self.close)

        if self.registro:
            _, data, quantidade, peso, observacao = self.registro
            self.input_data.setText(str(data))
            self.input_quantidade.setText(str(quantidade))
            self.input_peso.setText(str(peso))
            self.input_observacao.setText(str(observacao or ""))

    def salvar(self):
        try:
            data = self.input_data.text().strip()
            quantidade = int(self.input_quantidade.text())
            peso = float(self.input_peso.text().replace(",", "."))
            observacao = self.input_observacao.text().strip()

            if self.registro:
                sucesso, mensagem = atualizar_chegada(
                    self.registro[0], self.lote_id, data, quantidade, peso, observacao
                )
            else:
                sucesso, mensagem = cadastrar_chegada(
                    self.lote_id, data, quantidade, peso, observacao
                )

            if sucesso:
                QMessageBox.information(self, "Sucesso", mensagem)
                self.tela_lote.carregar_lote()
                self.close()
            else:
                QMessageBox.warning(self, "Erro", mensagem)

        except ValueError:
            QMessageBox.warning(self, "Atenção", "Preencha quantidade e peso corretamente.")
