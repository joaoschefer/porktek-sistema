from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QMessageBox
)
from PySide6.QtCore import Qt
from services.auth_service import validar_login
from config.window_config import LOGIN_WIDTH, LOGIN_HEIGHT


class LoginView(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PorkTek - Login")
        self.resize(400, 400)
        self.setMinimumSize(400, 400)

        self.titulo = QLabel("PorkTek")
        self.titulo.setObjectName("tituloLogin")
        self.titulo.setAlignment(Qt.AlignCenter)

        self.subtitulo = QLabel("Gestão de lotes de suínos")
        self.subtitulo.setObjectName("subtituloLogin")
        self.subtitulo.setAlignment(Qt.AlignCenter)

        self.input_usuario = QLineEdit()
        self.input_senha = QLineEdit()

        self.input_usuario.setPlaceholderText("Usuário")
        self.input_senha.setPlaceholderText("Senha")
        self.input_senha.setEchoMode(QLineEdit.Password)

        self.botao_entrar = QPushButton("Entrar")
        self.botao_registrar = QPushButton("Criar conta")
        self.botao_registrar.setObjectName("botaoSecundario")

        layout = QVBoxLayout()
        layout.setContentsMargins(40, 35, 40, 35)
        layout.setSpacing(14)

        layout.addWidget(self.titulo)
        layout.addWidget(self.subtitulo)
        layout.addWidget(self.input_usuario)
        layout.addWidget(self.input_senha)
        layout.addWidget(self.botao_entrar)
        layout.addWidget(self.botao_registrar)

        self.setLayout(layout)

        self.botao_entrar.clicked.connect(self.fazer_login)
        self.botao_registrar.clicked.connect(self.abrir_registro)

    def fazer_login(self):
        usuario = self.input_usuario.text()
        senha = self.input_senha.text()

        if usuario == "" or senha == "":
            QMessageBox.warning(self, "Atenção", "Preencha usuário e senha.")
            return

        sucesso, dados_usuario = validar_login(usuario, senha)

        if sucesso:
            from views.dashboard_view import DashboardView

            self.dashboard = DashboardView(dados_usuario)
            self.dashboard.showMaximized()
            self.close()
        else:
            QMessageBox.warning(self, "Erro", "Usuário ou senha inválidos.")

    def abrir_registro(self):
        from views.register_view import RegisterView

        self.registro = RegisterView()
        self.registro.show()
        self.close()