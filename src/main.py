#       -> Repositório público do GitHub <-
# https://github.com/Jujupedro5052005/CalculadoraPython

# Aluno: João Pedro de Jesus Cândido Silva
# R.A.: 23.01416-4


import inicial
import normal
import cientifica
import dicionario
from calculadora import EngineCalculadora  # Importa a lógica separada

import sys
from PyQt5 import QtCore, QtGui, QtWidgets

class HandlerQT(QtCore.QObject):
    """
    Classe responsável por gerenciar a interface gráfica (View).
    Ela escuta os eventos dos botões do PyQt5 e repassa as ações para a 
    EngineCalculadora processar a lógica matemática.
    """
    def __init__(self, name, engine: EngineCalculadora):
        super().__init__()
        self.__name = name
        self.Dialog = QtWidgets.QDialog()
        self.ui = self.__name.Ui_Dialog()
        self.ui.setupUi(self.Dialog)
        
        # Injeção de dependência: a interface compartilha o mesmo motor de cálculo
        self.engine = engine
        self.mode = "normal"   

    def display_update(self, telas):
        """Atualiza o visor de texto em ambas as telas de calculadora simultaneamente."""
        texto = self.engine.user_input
        telas[1].ui.displayUser.setText(texto)
        telas[2].ui.displayUser.setText(texto)

    def btn_push_callback(self, telas):
        """
        Método central que gerencia os cliques de todos os botões do app.
        Identifica quem chamou o evento pelo objectName e decide se muda de tela
        ou se envia o comando para a classe de lógica.
        """
        sender = self.Dialog.sender()
        if not sender:
            return

        name = sender.objectName()

        # --- Fluxo de Alternância entre Janelas ---
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

        # --- Ações Globais (Funcionam em ambos os modos) ---
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

            # Evento para mostrar o histórico de cálculos
            if "HIST" in name:
                historico_lista = self.engine.history
                
                # Se não houver nenhuma conta feita ainda
                if not historico_lista:
                    texto_historico = "Nenhum cálculo registrado ainda."
                else:
                    # Junta todas as linhas do histórico que guardamos pulando uma linha
                    texto_historico = "\n".join(historico_lista)
                
                # Abre um pop-up nativo do PyQt5 mostrando o histórico de um jeito bem elegante
                msg = QtWidgets.QMessageBox(self.Dialog)
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setWindowTitle("Histórico de Cálculos - Científica")
                msg.setText(texto_historico)
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msg.exec_()
                return

            # Alternador de unidade angular (DEG / RAD)
            if "TOGGLE_ANGLE" in name:
                if self.engine.angle_mode == "rad":
                    self.engine.angle_mode = "deg"
                    sender.setText("DEG")
                else:
                    self.engine.angle_mode = "rad"
                    sender.setText("RAD")
                return
            
            # Encaminhamento das strings de comando para a Engine montar a expressão
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

            # --- Ajuste para cálculo direto com funções científicas ---
            elif "SQRT" in name:
                if self.engine.user_input:
                    try:
                        # Tenta validar se o que está no visor é um número puro
                        float(self.engine.user_input)
                        self.engine.user_input = f"sqrt({self.engine.user_input})"
                    except ValueError:
                        # Se tiver letras ou operadores (como '5x'), apenas concatena a função aberta
                        self.engine.user_input += "sqrt("
                else:
                    self.engine.user_input += "sqrt("

            elif "SIN" in name:
                if self.engine.user_input:
                    try:
                        float(self.engine.user_input)
                        self.engine.user_input = f"sin({self.engine.user_input})"
                    except ValueError:
                        self.engine.user_input += "sin("
                else:
                    self.engine.user_input += "sin("

            elif "COS" in name:
                if self.engine.user_input:
                    try:
                        float(self.engine.user_input)
                        self.engine.user_input = f"cos({self.engine.user_input})"
                    except ValueError:
                        self.engine.user_input += "cos("
                else:
                    self.engine.user_input += "cos("

            elif "TAN" in name:
                if self.engine.user_input:
                    try:
                        float(self.engine.user_input)
                        self.engine.user_input = f"tan({self.engine.user_input})"
                    except ValueError:
                        self.engine.user_input += "tan("
                else:
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
            # Se o visor mostra erro ou o resultado anterior, limpa antes de digitar o novo número
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
            # Repassa a operação (+, -, *, /, =) para o tratamento sequencial da lógica comum
            self.engine.processar_operador_normal(name)

        self.display_update(telas)


# --- Bloco de Inicialização do Programa ---
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    # Instancia a classe de lógica matemática (Instanciação do Objeto compartilhado)
    calc_engine = EngineCalculadora(num_dec=5)

    # Cria as instâncias de interface injetando o mesmo motor lógico nelas
    ui_inicial = HandlerQT(inicial, calc_engine)
    ui_normal = HandlerQT(normal, calc_engine)
    ui_cientifica = HandlerQT(cientifica, calc_engine)
    telas = [ui_inicial, ui_normal, ui_cientifica]

    # Exibe a tela de menu para seleção de modo
    telas[0].Dialog.show()

    # Inicializa os displays como limpos
    telas[1].ui.displayUser.setText("")
    telas[2].ui.displayUser.setText("")

    # Conexões de eventos usando clicked.connect e mapeando para o callback central
    ui_inicial.ui.pushButtonNormal.clicked.connect(lambda: ui_inicial.btn_push_callback(telas))
    ui_inicial.ui.pushButtonCientifica.clicked.connect(lambda: ui_inicial.btn_push_callback(telas))

    ui_normal.ui.pushButtonVoltar.clicked.connect(lambda: ui_inicial.btn_push_callback(telas))
    ui_cientifica.ui.pushButtonVoltar.clicked.connect(lambda: ui_inicial.btn_push_callback(telas))

    # Loop para mapear dinamicamente os botões da UI Normal usando o dicionário estático
    for value, button in dicionario.ElementsUI.digit_buttons(ui_normal, "ui_normal").items():
        if button:
            button.clicked.connect(lambda: ui_inicial.btn_push_callback(telas))

    # Loop para mapear dinamicamente os botões da UI Científica usando o dicionário estático
    for value, button in dicionario.ElementsUI.digit_buttons(ui_cientifica, "ui_cientifica").items():
        if button:
            button.clicked.connect(lambda: ui_inicial.btn_push_callback(telas))

    sys.exit(app.exec_())