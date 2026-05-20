MAIN_STYLE = """
QWidget {
    background-color: #0f172a;
    color: #f8fafc;
    font-family: Arial;
    font-size: 14px;
}

QLabel {
    color: #f8fafc;
}

QLabel#tituloLogin {
    font-size: 30px;
    font-weight: bold;
    color: #ffffff;
    margin-bottom: 10px;
}

QLabel#subtituloLogin {
    font-size: 14px;
    color: #94a3b8;
    margin-bottom: 15px;
}

QLineEdit {
    background-color: #1e293b;
    color: #f8fafc;
    border: 1px solid #334155;
    border-radius: 10px;
    padding: 11px;
}

QLineEdit:focus {
    border: 1px solid #38bdf8;
}

QPushButton {
    background-color: #2563eb;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 11px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #1d4ed8;
}

QPushButton:pressed {
    background-color: #1e40af;
}

QPushButton#botaoSecundario {
    background-color: #334155;
    color: #f8fafc;
}

QPushButton#botaoSecundario:hover {
    background-color: #475569;
}

QLabel#tituloDashboard {
    font-size: 28px;
    font-weight: bold;
    color: #ffffff;
}

QLabel#subtituloDashboard {
    font-size: 14px;
    color: #94a3b8;
}

QLabel#secaoDashboard {
    font-size: 18px;
    font-weight: bold;
    color: #ffffff;
}

QLabel#textoInfoDashboard {
    font-size: 14px;
    color: #cbd5e1;
}

QFrame#painelDashboard {
    background-color: #111827;
    border: 1px solid #334155;
    border-radius: 16px;
    padding: 18px;
}

QFrame#cardDashboard {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 14px;
    padding: 14px;
}

QLabel#tituloCardDashboard {
    font-size: 14px;
    font-weight: bold;
    color: #94a3b8;
}

QLabel#valorCardDashboard {
    font-size: 24px;
    font-weight: bold;
    color: #ffffff;
}

QPushButton#botaoSair {
    background-color: #dc2626;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px 18px;
    font-weight: bold;
}

QPushButton#botaoSair:hover {
    background-color: #b91c1c;
}

QTableWidget#tabelaDashboard {
    background-color: #1e293b;
    color: #f8fafc;
    border: 1px solid #334155;
    border-radius: 12px;
    gridline-color: #334155;
    selection-background-color: #2563eb;
    selection-color: white;
}

QHeaderView::section {
    background-color: #2563eb;
    color: white;
    padding: 10px;
    border: none;
    font-weight: bold;
}
"""