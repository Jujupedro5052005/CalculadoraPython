import inicial
import normal
import cientifica

import sys
from PyQt5 import QtCore, QtGui, QtWidgets


class HandlerQT(QtCore.QObject):
    def __init__(self, name):
        super().__init__()
        self.__name = name
        # Atribui a janela do tipo Dialog
        self.Dialog = QtWidgets.QDialog()
        # Atribui os elementos ede exibicao na UI
        self.ui = self.__name.Ui_Dialog()
        # Atribui os elementos da UI na janela criada
        self.ui.setupUi(self.Dialog)

    def btn_push_callback(self, telas):
        sender = self.Dialog.sender()

        # Mostrar a tela de calculadora normal
        if sender.objectName() == "pushButtonNormal":
            telas[1].Dialog.show()
            telas[2].Dialog.close()

        # Mostrar a tela de calculadora cientifica
        if sender.objectName() == "pushButtonCientifica":
            telas[2].Dialog.show()
            telas[1].Dialog.close()
        
        # Sai da tela de calculadora normal ou da cientifica
        if sender.objectName() == "pushButtonVoltar":
            telas[1].Dialog.close()
            telas[2].Dialog.close()
        
        # Mostra digito no line edit
        if "pushButtonDigito" in sender.objectName():
            telas[1].ui.lineEditUsuario.setText(sender.text())


if __name__ == "__main__":
    # Inicializa a aplicacao
    app = QtWidgets.QApplication(sys.argv)

    # Cria os objetos das telas
    ui_inicial = HandlerQT(inicial)
    ui_normal = HandlerQT(normal)
    ui_cientifica = HandlerQT(cientifica)
    telas = [ui_inicial, ui_normal, ui_cientifica]

    # Mostra tela inicial
    telas[0].Dialog.show()

    # Começa os textos de saida zerados
    telas[1].ui.lineEditUsuario.setText("0")
    telas[2].ui.lineEditUsuario.setText("0")

    telas[1].ui.textBrowser.setHtml("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Page</title>
    <style>
        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #4facfe, #00f2fe);
            color: #333;
        }

        header {
            background: rgba(255, 255, 255, 0.9);
            padding: 20px;
            text-align: center;
            font-size: 1.8em;
            font-weight: bold;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        .container {
            max-width: 900px;
            margin: 40px auto;
            padding: 20px;
        }

        .card {
            background: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }

        button {
            background: #4facfe;
            border: none;
            padding: 12px 20px;
            color: white;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1em;
            transition: 0.3s;
        }

        button:hover {
            background: #0077ff;
        }

        footer {
            text-align: center;
            padding: 15px;
            color: white;
            font-size: 0.9em;
        }
    </style>
</head>
<body>

<header>
    My Test Page
</header>

<div class="container">
    <div class="card">
        <h2>Welcome 👋</h2>
        <p>This is a simple, clean HTML test page with modern styling.</p>
        <button onclick="showMessage()">Click Me</button>
    </div>

    <div class="card">
        <h3>Features</h3>
        <ul>
            <li>Responsive layout</li>
            <li>Gradient background</li>
            <li>Card design</li>
            <li>Interactive button</li>
        </ul>
    </div>
</div>

<footer>
    © 2026 Test Page
</footer>

<script>
    function showMessage() {
        alert("Button clicked! 🎉");
    }
</script>

</body>
</html>""")
    
    ui_inicial.ui.pushButtonNormal.setStyleSheet("""
QPushButton {
    background-color: #007BFF;
    color: white;
    border: none;
    border-radius: 2px;
    padding: 6px 12px;
}

QPushButton:hover {
    background-color: #0056b3;
}

QPushButton:pressed {
    background-color: #004494;
}
""")
    


    # Usando a função do sender (organizar os eventos de callback)
    ui_inicial.ui.pushButtonNormal.clicked.connect(lambda: ui_inicial.btn_push_callback(telas))
    ui_inicial.ui.pushButtonCientifica.clicked.connect(lambda: ui_inicial.btn_push_callback(telas))

    ui_normal.ui.pushButtonVoltar.clicked.connect(lambda: ui_inicial.btn_push_callback(telas))
    ui_cientifica.ui.pushButtonVoltar.clicked.connect(lambda: ui_inicial.btn_push_callback(telas))

    ui_cientifica.ui.pushButtonDigito1.clicked.connect(lambda: ui_inicial.btn_push_callback(telas))
    ui_cientifica.ui.pushButtonDigito2.clicked.connect(lambda: ui_inicial.btn_push_callback(telas))
    ui_cientifica.ui.pushButtonDigito3.clicked.connect(lambda: ui_inicial.btn_push_callback(telas))
    

    # Espera a interrupcao do usuario para finalizar
    sys.exit(app.exec_())
