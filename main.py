import sys
from PySide6.QtWidgets import QApplication
from views.login_view import LoginView
from database import criar_banco
from styles.main_style import MAIN_STYLE

if __name__ == "__main__":
    app = QApplication(sys.argv)

    app.setStyleSheet(MAIN_STYLE)

    criar_banco()

    janela = LoginView()
    janela.show()

    sys.exit(app.exec())