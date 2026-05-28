from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QMessageBox
)
from PySide6.QtCore import Qt
from services.auth_service import cadastrar_usuario


class RegisterView(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sistema de Suínos - Cadastro")
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, False)
        self.setFixedSize(420, 440)

        self.titulo = QLabel("Cadastro de Usuário")

        self.input_nome = QLineEdit()
        self.input_usuario = QLineEdit()
        self.input_email = QLineEdit()
        self.input_senha = QLineEdit()
        self.input_confirmar_senha = QLineEdit()

        self.input_nome.setPlaceholderText("Nome completo")
        self.input_usuario.setPlaceholderText("Usuário")
        self.input_email.setPlaceholderText("E-mail")
        self.input_senha.setPlaceholderText("Senha")
        self.input_confirmar_senha.setPlaceholderText("Confirmar senha")

        self.input_senha.setEchoMode(QLineEdit.Password)
        self.input_confirmar_senha.setEchoMode(QLineEdit.Password)

        self.botao_cadastrar = QPushButton("Cadastrar")
        self.botao_voltar = QPushButton("Voltar para login")

        layout = QVBoxLayout()
        layout.addWidget(self.titulo)
        layout.addWidget(self.input_nome)
        layout.addWidget(self.input_usuario)
        layout.addWidget(self.input_email)
        layout.addWidget(self.input_senha)
        layout.addWidget(self.input_confirmar_senha)
        layout.addWidget(self.botao_cadastrar)
        layout.addWidget(self.botao_voltar)

        self.setLayout(layout)

        self.botao_cadastrar.clicked.connect(self.cadastrar)
        self.botao_voltar.clicked.connect(self.voltar_login)

    def cadastrar(self):
        nome = self.input_nome.text()
        usuario = self.input_usuario.text()
        email = self.input_email.text()
        senha = self.input_senha.text()
        confirmar_senha = self.input_confirmar_senha.text()

        if nome == "" or usuario == "" or email == "" or senha == "":
            QMessageBox.warning(self, "Atenção", "Preencha todos os campos.")
            return

        if senha != confirmar_senha:
            QMessageBox.warning(self, "Atenção", "As senhas não são iguais.")
            return

        sucesso, mensagem = cadastrar_usuario(nome, usuario, email, senha)

        if sucesso:
            QMessageBox.information(self, "Sucesso", mensagem)
            self.voltar_login()
        else:
            QMessageBox.warning(self, "Erro", mensagem)

    def voltar_login(self):
        from views.login_view import LoginView

        self.login = LoginView()
        self.login.show()
        self.close()
