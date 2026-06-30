import inicial
import normal
import cientifica
import dicionario

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
        # Variável que recebe as entradas do usuário
        self.user_input = "0"

    def display_update(self):
        telas[1].ui.displayUser.setText(self.user_input)
        telas[2].ui.displayUser.setText(self.user_input)

    def btn_push_callback(self, telas):
        sender = self.Dialog.sender()

        # Mostrar a tela de calculadora normal
        if sender.objectName() == "pushButtonNormal":
            telas[1].Dialog.show()
            telas[2].Dialog.close()

        # Mostrar a tela de calculadora cientifica
        elif sender.objectName() == "pushButtonCientifica":
            telas[2].Dialog.show()
            telas[1].Dialog.close()
        
        # Sai da tela de calculadora normal ou da cientifica
        elif sender.objectName() == "pushButtonVoltar":
            telas[1].Dialog.close()
            telas[2].Dialog.close()

        # Backspace no ultimo elemento do texto
        elif sender.objectName() == "pushButtonBACK":
            if len(self.user_input) != 0:
                self.user_input = self.user_input[:-1]

        # Limpa texto do usuário
        elif sender.objectName() == "pushButtonClear":
            self.user_input = "0"

        # Insere ponto decimal
        elif sender.objectName() == "pushButtonDOT":
            if not("." in self.user_input):
                self.user_input += "."
        
        # Atualiza texto de entrada do usuário
        elif "pushButtonDigito" in sender.objectName():
            self.user_input += sender.text()
            #telas[2].ui.lineEditUsuario.setText(sender.text())

        # Processa a seleção de operação
        elif "pushButtonOP" in sender.objectName():
            self.user_input += sender.text()

        self.display_update()


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

    # Começa com os textos de saida zerados
    telas[1].ui.displayUser.setText("0")
    telas[2].ui.displayUser.setText("0")

    # Usando a função do sender (organizar os eventos de callback)
    ui_inicial.ui.pushButtonNormal.clicked.connect(lambda: ui_inicial.btn_push_callback(telas))
    ui_inicial.ui.pushButtonCientifica.clicked.connect(lambda: ui_inicial.btn_push_callback(telas))

    ui_normal.ui.pushButtonVoltar.clicked.connect(lambda: ui_inicial.btn_push_callback(telas))
    ui_cientifica.ui.pushButtonVoltar.clicked.connect(lambda: ui_inicial.btn_push_callback(telas))

    ui_cientifica.ui.pushButtonDigito1.clicked.connect(lambda: ui_inicial.btn_push_callback(telas))
    ui_cientifica.ui.pushButtonDigito2.clicked.connect(lambda: ui_inicial.btn_push_callback(telas))
    ui_cientifica.ui.pushButtonDigito3.clicked.connect(lambda: ui_inicial.btn_push_callback(telas))

    # Declara todos os botões utilizando o o dicionario estático de ElementsUI para ui_normal
    for value, button in dicionario.ElementsUI.digit_buttons(ui_normal).items():
        button.clicked.connect(lambda: ui_inicial.btn_push_callback(telas))

    # Espera a interrupcao do usuario para finalizar
    sys.exit(app.exec_())
