import inicial
import normal
import cientifica
import dicionario

import sys
from PyQt5 import QtCore, QtGui, QtWidgets


# Número de casas decimais a serem mostradas no display
NUM_DEC = 5


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
        self.user_input = ""
        # Variáveis para a lógica de operação da calculadora NORMAL
        self.user_input = ""
        self.last_num = None
        self.operation = None
        self.result = 0.0

    def display_update(self):
        telas[1].ui.displayUser.setText(self.user_input)
        telas[2].ui.displayUser.setText(self.user_input)

    def normal_op(self):
        a = self.last_num
        b = float(self.user_input)

        if self.operation == "+":
            self.result = a + b

        elif self.operation == "-":
            self.result = a - b

        elif self.operation == "x":
            self.result = a * b

        elif self.operation == "/":

            if b == 0:
                self.user_input = "Math Error"
                self.last_num = None
                self.operation = None
                return
            self.result = a / b

        self.result = round(self.result, NUM_DEC)
        self.user_input = str(self.result)
        self.last_num = self.result
        self.operation = None

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

        # Backspace no ultimo elemento do texto
        if "BACK" in sender.objectName():
            if self.user_input != "":
                self.user_input = self.user_input[:-1]

        # Limpa texto do usuário
        if "Clear" in sender.objectName():
            self.user_input = ""
            self.last_num = None
            self.operation = None
            self.result = 0.0

        # Insere ponto decimal
        if "DOT" in sender.objectName():
            if self.operation is None and self.user_input == str(self.result):
                self.user_input = ""
            if "." not in self.user_input:
                if self.user_input == "":
                    self.user_input = "0."
                else:
                    self.user_input += "."

        # Insere ponto decimal
        if "ANS" in sender.objectName():
            self.user_input = str(self.result)
        
        if "pushButtonDigito" in sender.objectName():
            if self.operation is None and self.user_input == str(self.result):
                self.user_input = ""
            self.user_input += sender.text()

        # ----------------------------------------------------------
        # NORMAL calculator operations
        # ----------------------------------------------------------
        if "pushButtonOPN" in sender.objectName():

            print(sender.objectName())

            # ===========================
            # "="
            # ===========================
            if "EQU" in sender.objectName():

                if self.operation is None:

                    if self.user_input != "":
                        self.result = float(self.user_input)

                else:

                    if self.user_input == "":

                        # user typed:
                        #
                        # 52 +
                        # =
                        #
                        self.user_input = str(self.last_num)

                        self.result = self.last_num

                        self.operation = None

                    else:

                        self.normal_op()

            # ===========================
            # + - x /
            # ===========================
            else:

                if self.user_input == "":
                    return

                # Continue calculating:
                #
                # 5+2=+3=
                #
                if self.operation is not None:

                    self.normal_op()

                self.last_num = float(self.user_input)

                if "ADD" in sender.objectName():
                    self.operation = "+"

                elif "SUB" in sender.objectName():
                    self.operation = "-"

                elif "MUL" in sender.objectName():
                    self.operation = "x"

                elif "DIV" in sender.objectName():
                    self.operation = "/"

                self.user_input = ""

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
    telas[1].ui.displayUser.setText("")
    telas[2].ui.displayUser.setText("")

    # Usando a função do sender (organizar os eventos de callback)
    ui_inicial.ui.pushButtonNormal.clicked.connect(lambda: ui_inicial.btn_push_callback(telas))
    ui_inicial.ui.pushButtonCientifica.clicked.connect(lambda: ui_inicial.btn_push_callback(telas))

    ui_normal.ui.pushButtonVoltar.clicked.connect(lambda: ui_inicial.btn_push_callback(telas))
    ui_cientifica.ui.pushButtonVoltar.clicked.connect(lambda: ui_inicial.btn_push_callback(telas))

    ui_cientifica.ui.pushButtonDigitoC1.clicked.connect(lambda: ui_inicial.btn_push_callback(telas))
    ui_cientifica.ui.pushButtonDigitoC2.clicked.connect(lambda: ui_inicial.btn_push_callback(telas))
    ui_cientifica.ui.pushButtonDigitoC3.clicked.connect(lambda: ui_inicial.btn_push_callback(telas))

    # Declara todos os botões utilizando o o dicionario estático de ElementsUI para ui_normal
    for value, button in dicionario.ElementsUI.digit_buttons(ui_normal).items():
        button.clicked.connect(lambda: ui_inicial.btn_push_callback(telas))

    # Espera a interrupcao do usuario para finalizar
    sys.exit(app.exec_())
