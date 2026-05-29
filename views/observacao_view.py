from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PySide6.QtCore import Qt
from services.lote_service import cadastrar_observacao, atualizar_observacao


class ObservacaoView(QWidget):
    def __init__(self, lote_id, tela_lote, registro=None):
        super().__init__()

        self.lote_id = lote_id
        self.tela_lote = tela_lote
        self.registro = registro

        self.setWindowTitle("Editar observação" if self.registro else "Registrar observação")
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, False)
        self.setFixedSize(500, 420)

        self.titulo = QLabel("Editar observação" if self.registro else "Registrar observação")
        self.titulo.setObjectName("tituloLogin")
        self.titulo.setAlignment(Qt.AlignCenter)

        self.input_observacao = QLineEdit()
        self.input_data_inicio = QLineEdit()
        self.input_data_termino = QLineEdit()

        self.input_observacao.setPlaceholderText("Observação")
        self.input_data_inicio.setPlaceholderText("Data de início")
        self.input_data_termino.setPlaceholderText("Data de término")

        self.botao_salvar = QPushButton("Salvar observação")
        self.botao_cancelar = QPushButton("Cancelar")
        self.botao_cancelar.setObjectName("botaoSecundario")

        layout = QVBoxLayout()
        layout.setContentsMargins(35, 25, 35, 25)
        layout.setSpacing(12)

        layout.addWidget(self.titulo)
        layout.addWidget(self.input_observacao)
        layout.addWidget(self.input_data_inicio)
        layout.addWidget(self.input_data_termino)
        layout.addWidget(self.botao_salvar)
        layout.addWidget(self.botao_cancelar)

        self.setLayout(layout)

        self.botao_salvar.clicked.connect(self.salvar)
        self.botao_cancelar.clicked.connect(self.close)

        if self.registro:
            _, observacao, data_inicio, data_termino = self.registro
            self.input_observacao.setText(str(observacao or ""))
            self.input_data_inicio.setText(str(data_inicio or ""))
            self.input_data_termino.setText(str(data_termino or ""))

    def salvar(self):
        observacao = self.input_observacao.text().strip()
        data_inicio = self.input_data_inicio.text().strip()
        data_termino = self.input_data_termino.text().strip()

        if self.registro:
            sucesso, mensagem = atualizar_observacao(
                self.registro[0], self.lote_id, observacao, data_inicio, data_termino
            )
        else:
            sucesso, mensagem = cadastrar_observacao(
                self.lote_id, observacao, data_inicio, data_termino
            )

        if sucesso:
            QMessageBox.information(self, "Sucesso", mensagem)
            self.tela_lote.carregar_lote()
            self.close()
        else:
            QMessageBox.warning(self, "Erro", mensagem)
