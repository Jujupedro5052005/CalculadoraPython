import inicial
import normal
import cientifica
import dicionario

import sys
import math
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
        # Modo de operação atual
        self.mode = "normal"   # ou "scientific"
        # Variáveis para a lógica de operação da calculadora
        self.angle_mode = "deg"   # or "deg"
        self.last_num = None
        self.operation = None
        self.repeat_operand = None
        self.repeat_operation = None
        self.result = 0.0
        self.expression = ""
        self.showing_result = False

    def display_update(self):
        telas[1].ui.displayUser.setText(self.user_input)
        telas[2].ui.displayUser.setText(self.user_input)

    def normal_op(self):
        if self.user_input == "":
            return

        a = self.last_num
        b = float(self.user_input)
        self.repeat_operand = b
        self.repeat_operation = self.operation

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
                self.result = 0.0
                return
            self.result = a / b

        self.result = round(self.result, NUM_DEC)
        self.user_input = str(self.result)
        self.last_num = self.result
        self.operation = None

    def _to_rad(self, x):
        return math.radians(x) if self.angle_mode == "deg" else x

    def scientific_eval(self):
        expr = self.user_input

        if expr == "":
            return

        # normalize
        expr = expr.replace("x", "*")
        expr = expr.replace("^", "**")
        expr = expr.replace("sen", "sin")

        try:
            self.result = eval(
                expr,
                {"__builtins__": None},
                {
                    "sqrt": math.sqrt,
                    "sin": lambda x: math.sin(math.radians(x) if self.angle_mode == "deg" else x),
                    "cos": lambda x: math.cos(math.radians(x) if self.angle_mode == "deg" else x),
                    "tan": lambda x: math.tan(math.radians(x) if self.angle_mode == "deg" else x),
                    "pi": math.pi,
                }
            )

            return self.result

        except:
            self.user_input = "Math Error"

    def safe_backspace(self):
        if self.user_input == "Math Error":
            self.user_input = ""
            self.expression = ""
            return

        # function-aware delete
        for token in ["sqrt(", "sin(", "cos(", "tan("]:
            if self.expression.endswith(token):
                self.expression = self.expression[:-len(token)]
                self.user_input = self.expression
                return

        self.expression = self.expression[:-1]
        self.user_input = self.expression

    def btn_push_callback(self, telas):
        sender = self.Dialog.sender()

        # Mostrar a tela de calculadora normal
        if sender.objectName() == "pushButtonNormal":
            self.mode = "normal"
            telas[1].Dialog.show()
            telas[2].Dialog.close()

        # Mostrar a tela de calculadora cientifica
        if sender.objectName() == "pushButtonCientifica":
            self.mode = "scientific"
            telas[2].Dialog.show()
            telas[1].Dialog.close()
        
        # Sai da tela de calculadora normal ou da cientifica
        if sender.objectName() == "pushButtonVoltar":
            telas[1].Dialog.close()
            telas[2].Dialog.close()

        # Backspace no ultimo elemento do texto
        if "BACK" in sender.objectName():
            if self.user_input == "Math Error":
                self.user_input = ""
            else:
                self.safe_backspace()

        # Limpa texto do usuário
        if "Clear" in sender.objectName():
            self.user_input = ""
            self.last_num = None
            self.operation = None
            self.result = 0.0

        # Insere ponto decimal
        if "DOT" in sender.objectName():
            if self.user_input == "Math Error":
                self.user_input = ""
            elif self.operation is None and self.user_input == str(self.result):
                self.user_input = ""

            if "." not in self.user_input:
                if self.user_input == "":
                    self.user_input = "0."
                else:
                    self.user_input += "."

        # Insere ponto decimal
        if "ANS" in sender.objectName():
            if self.user_input != "Math Error":
                self.user_input = str(self.result)
        
        if "pushButtonDigito" in sender.objectName():
            if self.user_input == "Math Error":
                self.user_input = ""

            # ALWAYS allow digits in both modes
            if self.operation is None and self.user_input == str(self.result):
                self.user_input = ""

            # DIGITS
            if "pushButtonDigito" in sender.objectName():
                if self.user_input == "Math Error":
                    self.expression = ""
                
                self.expression += sender.text()
                self.user_input = self.expression
                self.display_update()
                return

        # ==========================================================
        # SCIENTIFIC MODE
        # ==========================================================
        if self.mode == "scientific" and "pushButtonOPC" in sender.objectName():
            name = sender.objectName()

            if "Digito" in name:
                self.expression += sender.text()
                self.user_input = self.expression
                self.display_update()
                return
            
            # CLEAR
            elif "Clear" in name:
                self.user_input = ""

            # BACK
            elif "BACK" in name:
                if self.user_input:
                    self.user_input = self.user_input[:-1]
                

            # DOT
            elif "DOT" in name:
                if "." not in self.user_input:
                    self.user_input += "."

            # ANS
            elif "ANS" in name:
                self.user_input = str(self.result)

            # PI
            elif "PI" in name:
                self.user_input += "pi"

            # OPERATORS
            elif "ADD" in name:
                self.user_input += "+"

            elif "SUB" in name:
                self.user_input += "-"

            elif "MUL" in name:
                self.user_input += "x"

            elif "DIV" in name:
                self.user_input += "/"

            # PARENTHESIS
            elif "Paren1" in name:
                self.user_input += "("

            elif "Paren2" in name:
                self.user_input += ")"

            # SQRT
            elif "SQRT" in name:
                self.user_input += "sqrt("

            # POWER
            elif "POW" in name:
                self.user_input = f"({self.user_input})**2"

            # PERCENT
            elif "PER" in name:
                self.user_input = f"({self.user_input})/100"

            # INVERSE
            elif "INV" in name:
                self.user_input = "1/(" + self.user_input + ")"

            # SIN
            elif "SIN" in name:
                self.user_input += "sin("

            elif "COS" in name:
                self.user_input += "cos("

            elif "TAN" in name:
                self.user_input += "tan("

            elif "PLUS_MINUS" in name:
                if self.user_input == "":
                    return

                if self.expression.startswith("-"):
                    self.expression = self.expression[1:]
                else:
                    self.expression = "-" + self.expression

                self.user_input = self.expression

            # EQUALS
            elif "EQU" in name:
                self.result = self.scientific_eval()
                if self.result is None:
                    # scientific_eval already set self.user_input = "Math Error"
                    self.expression = ""
                else:
                    self.user_input = str(round(self.result, NUM_DEC))
                    self.expression = self.user_input   # allows chaining
                self.display_update()
                return
            
            # Keep expression in sync with user_input so the next digit
            # press (which rebuilds user_input from expression) doesn't
            # wipe out operators/functions typed in this branch.
            self.expression = self.user_input
            self.display_update()
            return

        # ----------------------------------------------------------
        # NORMAL calculator operations
        # ----------------------------------------------------------
        if "pushButtonOPN" in sender.objectName():
            if self.user_input == "Math Error":
                return

            print(sender.objectName())

            # ===========================
            # "="
            # ===========================
            if "EQU" in sender.objectName():
                # --------------------------------------------------
                # There is a pending operation
                # Example:
                # 5 + 3 =
                # --------------------------------------------------
                if self.operation is not None:

                    # User pressed "=" immediately after the operator
                    # Example:
                    # 5 + =
                    if self.user_input == "":

                        self.result = self.last_num
                        self.user_input = str(self.result)

                        # Do NOT clear operation.
                        # This lets repeated "=" work.

                    else:

                        self.normal_op()

                # --------------------------------------------------
                # No pending operation
                # Example:
                # "=" after a previous calculation
                # --------------------------------------------------
                else:

                    if (
                        self.repeat_operation is not None
                        and self.repeat_operand is not None
                        and self.user_input != ""
                    ):

                        self.last_num = float(self.user_input)
                        self.operation = self.repeat_operation
                        self.user_input = str(self.repeat_operand)

                        self.normal_op()

                    elif self.user_input != "":

                        self.result = float(self.user_input)

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

                if self.user_input != "Math Error":
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

        # Keep expression in sync with user_input (same reasoning as in
        # scientific mode) so digit entry after Clear/=/operators starts
        # from the correct text instead of a stale expression.
        self.expression = self.user_input
        self.display_update()


#if __name__ == "__main__":
if True:
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

    # Declara todos os botões utilizando o o dicionario estático de ElementsUI para ui_normal
    for value, button in dicionario.ElementsUI.digit_buttons(ui_normal, "ui_normal").items():
        button.clicked.connect(lambda: ui_inicial.btn_push_callback(telas))

    # Declara todos os botões utilizando o o dicionario estático de ElementsUI para ui_normal
    for value, button in dicionario.ElementsUI.digit_buttons(ui_cientifica, "ui_cientifica").items():
        button.clicked.connect(lambda: ui_inicial.btn_push_callback(telas))

    # Espera a interrupcao do usuario para finalizar
    sys.exit(app.exec_())
