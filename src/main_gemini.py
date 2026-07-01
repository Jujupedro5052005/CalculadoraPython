import inicial
import normal
import cientifica
import dicionario

import sys
import math
from PyQt5 import QtCore, QtGui, QtWidgets

NUM_DEC = 5

class HandlerQT(QtCore.QObject):
    def __init__(self, name):
        super().__init__()
        self.__name = name
        self.Dialog = QtWidgets.QDialog()
        self.ui = self.__name.Ui_Dialog()
        self.ui.setupUi(self.Dialog)
        
        self.user_input = ""
        self.mode = "normal"   
        self.last_num = None
        self.operation = None
        self.repeat_operand = None
        self.repeat_operation = None
        self.result = 0.0
        self.expression = ""
        self.angle_mode = "deg"
        self.last_valid_expression = ""

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

    def scientific_eval(self):
        expr = self.user_input
        if expr == "":
            return 0.0

        # Salva um backup caso a expressão dê erro no eval
        self.last_valid_expression = expr 

        expr = expr.replace("x", "*")
        expr = expr.replace("π", "pi")
        
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
            return "Math Error"

    def safe_backspace(self):
        # Se estiver em tela de erro, recupera a última expressão tentada
        if self.user_input == "Math Error":
            self.user_input = self.last_valid_expression
            return

        # Apaga funções inteiras
        for token in ["sqrt(", "sin(", "cos(", "tan("]:
            if self.user_input.endswith(token):
                self.user_input = self.user_input[:-len(token)]
                return

        self.user_input = self.user_input[:-1]

    def btn_push_callback(self, telas):
        sender = self.Dialog.sender()
        if not sender:
            return

        name = sender.objectName()

        # Alternância de telas
        if name == "pushButtonNormal":
            self.mode = "normal"
            telas[1].Dialog.show()
            telas[2].Dialog.close()
            return

        if name == "pushButtonCientifica":
            self.mode = "scientific"
            telas[2].Dialog.show()
            telas[1].Dialog.close()
            return
        
        if name == "pushButtonVoltar":
            telas[1].Dialog.close()
            telas[2].Dialog.close()
            return

        # Controle global de Clear e Backspace
        if "Clear" in name:
            self.user_input = ""
            self.expression = ""
            self.last_num = None
            self.operation = None
            self.result = 0.0
            self.display_update()
            return

        if "BACK" in name:
            self.safe_backspace()
            self.display_update()
            return

        # ==========================================================
        # LOGICA DO MODO CIENTÍFICO
        # ==========================================================
        if self.mode == "scientific":
            if self.user_input == "Math Error":
                self.user_input = ""

            # NOVO: Alternador de Modo de Ângulo (DEG / RAD)
            if "TOGGLE_ANGLE" in name:
                if self.angle_mode == "rad":
                    self.angle_mode = "deg"
                    sender.setText("DEG") # Muda o texto do botão para indicar Graus
                else:
                    self.angle_mode = "rad"
                    sender.setText("RAD") # Muda o texto do botão para indicar Radianos
                return # Não precisa atualizar o display principal de números

            if "pushButtonDigito" in name:
                self.user_input += sender.text()
            elif "DOT" in name:
                # Permite ponto se o último bloco numérico não tiver um
                self.user_input += "."
            elif "ANS" in name:
                self.user_input += str(self.result)
            elif "PI" in name:
                self.user_input += "pi"
            elif "ADD" in name:
                self.user_input += "+"
            elif "SUB" in name:
                self.user_input += "-"
            elif "MUL" in name:
                self.user_input += "x"
            elif "DIV" in name:
                self.user_input += "/"
            elif "Paren1" in name:
                self.user_input += "("
            elif "Paren2" in name:
                self.user_input += ")"
            elif "SQRT" in name:
                self.user_input += "sqrt("
            elif "SIN" in name:
                self.user_input += "sin("
            elif "COS" in name:
                self.user_input += "cos("
            elif "TAN" in name:
                self.user_input += "tan("
            elif "POW" in name:
                if self.user_input:
                    self.user_input = f"({self.user_input})**2"
            elif "PER" in name:
                if self.user_input:
                    self.user_input = f"({self.user_input})/100"
            elif "INV" in name:
                if self.user_input:
                    self.user_input = f"1/({self.user_input})"
            elif "PLUS_MINUS" in name:
                if self.user_input:
                    if self.user_input.startswith("-"):
                        self.user_input = self.user_input[1:]
                    else:
                        self.user_input = "-" + self.user_input
            elif "EQU" in name:
                res = self.scientific_eval()
                if res == "Math Error":
                    self.user_input = "Math Error"
                else:
                    self.result = res
                    self.user_input = str(round(self.result, NUM_DEC))
            
            self.display_update()
            return

        # ==========================================================
        # LOGICA DO MODO NORMAL
        # ==========================================================
        if "pushButtonDigito" in name:
            if self.user_input == "Math Error" or self.user_input == str(self.result):
                self.user_input = ""
            self.user_input += sender.text()

        elif "DOT" in name:
            if self.user_input == "Math Error" or self.user_input == str(self.result):
                self.user_input = "0."
            elif "." not in self.user_input:
                self.user_input += "." if self.user_input != "" else "0."

        elif "ANS" in name:
            if self.user_input != "Math Error":
                self.user_input = str(self.result)

        elif "pushButtonOPN" in name:
            if self.user_input == "Math Error":
                return

            if "EQU" in name:
                if self.operation is not None:
                    if self.user_input == "":
                        self.result = self.last_num
                        self.user_input = str(self.result)
                    else:
                        self.normal_op()
                else:
                    if self.repeat_operation is not None and self.repeat_operand is not None and self.user_input != "":
                        self.last_num = float(self.user_input)
                        self.operation = self.repeat_operation
                        self.user_input = str(self.repeat_operand)
                        self.normal_op()
                    elif self.user_input != "":
                        self.result = float(self.user_input)
            else:
                if self.user_input == "":
                    return
                if self.operation is not None:
                    self.normal_op()

                if self.user_input != "Math Error":
                    self.last_num = float(self.user_input)

                if "ADD" in name:
                    self.operation = "+"
                elif "SUB" in name:
                    self.operation = "-"
                elif "MUL" in name:
                    self.operation = "x"
                elif "DIV" in name:
                    self.operation = "/"
                self.user_input = ""

        self.display_update()


#if __name__ == "__main__":
if True :
    app = QtWidgets.QApplication(sys.argv)

    ui_inicial = HandlerQT(inicial)
    ui_normal = HandlerQT(normal)
    ui_cientifica = HandlerQT(cientifica)
    telas = [ui_inicial, ui_normal, ui_cientifica]

    telas[0].Dialog.show()

    telas[1].ui.displayUser.setText("")
    telas[2].ui.displayUser.setText("")

    ui_inicial.ui.pushButtonNormal.clicked.connect(lambda: ui_inicial.btn_push_callback(telas))
    ui_inicial.ui.pushButtonCientifica.clicked.connect(lambda: ui_inicial.btn_push_callback(telas))

    ui_normal.ui.pushButtonVoltar.clicked.connect(lambda: ui_inicial.btn_push_callback(telas))
    ui_cientifica.ui.pushButtonVoltar.clicked.connect(lambda: ui_inicial.btn_push_callback(telas))

    # Conectar botões adicionais mapeados do modo normal
    for value, button in dicionario.ElementsUI.digit_buttons(ui_normal, "ui_normal").items():
        if button:
            button.clicked.connect(lambda: ui_inicial.btn_push_callback(telas))

    # Conectar botões adicionais mapeados do modo científico
    for value, button in dicionario.ElementsUI.digit_buttons(ui_cientifica, "ui_cientifica").items():
        if button:
            button.clicked.connect(lambda: ui_inicial.btn_push_callback(telas))

    sys.exit(app.exec_())