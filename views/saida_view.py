from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QMessageBox
)
from PySide6.QtCore import Qt
from datetime import date
from services.lote_service import cadastrar_saida


class SaidaView(QWidget):
    def __init__(self, lote_id, tela_lote):
        super().__init__()

        self.lote_id = lote_id
        self.tela_lote = tela_lote

        self.setWindowTitle("Cadastrar saída")
        self.resize(500, 500)
        self.setMinimumSize(500, 500)

        self.titulo = QLabel("Cadastrar saída")
        self.titulo.setObjectName("tituloLogin")
        self.titulo.setAlignment(Qt.AlignCenter)

        self.input_data = QLineEdit()
        self.input_quantidade = QLineEdit()
        self.input_peso = QLineEdit()
        self.input_observacao = QLineEdit()

        self.input_data.setText(date.today().strftime("%d/%m/%Y"))
        self.input_quantidade.setPlaceholderText("Quantidade de saída")
        self.input_peso.setPlaceholderText("Peso médio final")
        self.input_observacao.setPlaceholderText("Observação")

        self.botao_salvar = QPushButton("Finalizar lote")
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

    def salvar(self):
        try:
            data = self.input_data.text().strip()
            quantidade = int(self.input_quantidade.text())
            peso = float(self.input_peso.text().replace(",", "."))
            observacao = self.input_observacao.text().strip()

            sucesso, mensagem = cadastrar_saida(
                self.lote_id, data, quantidade, peso, observacao
            )

            if sucesso:
                QMessageBox.information(self, "Sucesso", mensagem)
                self.tela_lote.voltar_dashboard()
                self.close()
            else:
                QMessageBox.warning(self, "Erro", mensagem)

        except ValueError:
            QMessageBox.warning(self, "Atenção", "Preencha quantidade e peso corretamente.")