import inicial
import normal
import cientifica
import dicionario
from calculadora import EngineCalculadora  # Importa a lógica separada

import sys
from PyQt5 import QtCore, QtGui, QtWidgets

class HandlerQT(QtCore.QObject):
    def __init__(self, name, engine: EngineCalculadora):
        super().__init__()
        self.__name = name
        self.Dialog = QtWidgets.QDialog()
        self.ui = self.__name.Ui_Dialog()
        self.ui.setupUi(self.Dialog)
        
        # Injeção de dependência: A interface recebe o motor de cálculo
        self.engine = engine
        self.mode = "normal"   

    def display_update(self, telas):
        # Busca o valor guardado de forma encapsulada no motor de cálculo
        texto = self.engine.user_input
        telas[1].ui.displayUser.setText(texto)
        telas[2].ui.displayUser.setText(texto)

    def btn_push_callback(self, telas):
        sender = self.Dialog.sender()
        if not sender:
            return

        name = sender.objectName()

        # Fluxo de Janelas
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

        # Ações Globais delegadas para a classe Engine
        if "Clear" in name:
            self.engine.clear()
            self.display_update(telas)
            return

        if "BACK" in name:
            self.engine.safe_backspace()
            self.display_update(telas)
            return

        # ==========================================================
        # INTERFACE MODO CIENTÍFICO
        # ==========================================================
        if self.mode == "scientific":
            if self.engine.user_input == "Math Error":
                self.engine.user_input = ""

            if "TOGGLE_ANGLE" in name:
                if self.engine.angle_mode == "rad":
                    self.engine.angle_mode = "deg"
                    sender.setText("DEG")
                else:
                    self.engine.angle_mode = "rad"
                    sender.setText("RAD")
                return
            
            # Encaminhamento das strings de botões para a Engine
            if "pushButtonDigito" in name:
                self.engine.user_input += sender.text()
            elif "DOT" in name:
                self.engine.user_input += "."
            elif "ANS" in name:
                self.engine.user_input += str(self.engine.result)
            elif "PI" in name:
                self.engine.user_input += "pi"
            elif "ADD" in name:
                self.engine.user_input += "+"
            elif "SUB" in name:
                self.engine.user_input += "-"
            elif "MUL" in name:
                self.engine.user_input += "x"
            elif "DIV" in name:
                self.engine.user_input += "/"
            elif "Paren1" in name:
                self.engine.user_input += "("
            elif "Paren2" in name:
                self.engine.user_input += ")"
            elif "SQRT" in name:
                self.engine.user_input += "sqrt("
            elif "SIN" in name:
                self.engine.user_input += "sin("
            elif "COS" in name:
                self.engine.user_input += "cos("
            elif "TAN" in name:
                self.engine.user_input += "tan("
            elif "POW" in name:
                if self.engine.user_input:
                    self.engine.user_input = f"({self.engine.user_input})**2"
            elif "PER" in name:
                if self.engine.user_input:
                    self.engine.user_input = f"({self.engine.user_input})/100"
            elif "INV" in name:
                if self.engine.user_input:
                    self.engine.user_input = f"1/({self.engine.user_input})"
            elif "PLUS_MINUS" in name:
                if self.engine.user_input:
                    if self.engine.user_input.startswith("-"):
                        self.engine.user_input = self.engine.user_input[1:]
                    else:
                        self.engine.user_input = "-" + self.engine.user_input
            elif "EQU" in name:
                self.engine.scientific_eval()
            
            self.display_update(telas)
            return

        # ==========================================================
        # INTERFACE MODO NORMAL
        # ==========================================================
        if "pushButtonDigito" in name:
            if self.engine.user_input == "Math Error" or self.engine.user_input == str(self.engine.result):
                self.engine.user_input = ""
            self.engine.user_input += sender.text()

        elif "DOT" in name:
            if self.engine.user_input == "Math Error" or self.engine.user_input == str(self.engine.result):
                self.engine.user_input = "0."
            elif "." not in self.engine.user_input:
                self.engine.user_input += "." if self.engine.user_input != "" else "0."

        elif "ANS" in name:
            if self.engine.user_input != "Math Error":
                self.engine.user_input = str(self.engine.result)

        elif "pushButtonOPN" in name:
            self.engine.processar_operador_normal(name)

        self.display_update(telas)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    # Instancia a classe de lógica de cálculo (Instanciação de Objeto)
    calc_engine = EngineCalculadora(num_dec=5)

    # Passa a mesma instância lógica (calc_engine) para todas as interfaces compartilharem os dados
    ui_inicial = HandlerQT(inicial, calc_engine)
    ui_normal = HandlerQT(normal, calc_engine)
    ui_cientifica = HandlerQT(cientifica, calc_engine)
    telas = [ui_inicial, ui_normal, ui_cientifica]

    telas[0].Dialog.show()

    telas[1].ui.displayUser.setText("")
    telas[2].ui.displayUser.setText("")

    ui_inicial.ui.pushButtonNormal.clicked.connect(lambda: ui_inicial.btn_push_callback(telas))
    ui_inicial.ui.pushButtonCientifica.clicked.connect(lambda: ui_inicial.btn_push_callback(telas))

    ui_normal.ui.pushButtonVoltar.clicked.connect(lambda: ui_inicial.btn_push_callback(telas))
    ui_cientifica.ui.pushButtonVoltar.clicked.connect(lambda: ui_inicial.btn_push_callback(telas))

    for value, button in dicionario.ElementsUI.digit_buttons(ui_normal, "ui_normal").items():
        if button:
            button.clicked.connect(lambda: ui_inicial.btn_push_callback(telas))

    for value, button in dicionario.ElementsUI.digit_buttons(ui_cientifica, "ui_cientifica").items():
        if button:
            button.clicked.connect(lambda: ui_inicial.btn_push_callback(telas))

    sys.exit(app.exec_())