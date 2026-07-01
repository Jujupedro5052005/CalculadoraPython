import math

class EngineCalculadora:
    """
    Motor lógico de cálculo da calculadora (Model).
    Centraliza todos os estados matemáticos, operações e agora o histórico de cálculos.
    """
    def __init__(self, num_dec=5):
        self.__num_dec = num_dec
        self.__user_input = ""
        self.__last_num = None
        self.__operation = None
        self.__repeat_operand = None
        self.__repeat_operation = None
        self.__result = 0.0
        self.__last_valid_expression = ""
        self.__angle_mode = "deg"
        
        self.__history = []

    # --- Getters e Setters ---
    @property
    def user_input(self):
        return self.__user_input

    @user_input.setter
    def user_input(self, valor):
        self.__user_input = valor

    @property
    def angle_mode(self):
        return self.__angle_mode

    @angle_mode.setter
    def angle_mode(self, modo):
        if modo in ["rad", "deg"]:
            self.__angle_mode = modo

    @property
    def result(self):
        return self.__result

    def clear(self):
        self.__user_input = ""
        self.__last_num = None
        self.__operation = None

    def clear_history(self):
        """Esvazia o histórico de cálculos."""
        self.__history = []

    def safe_backspace(self):
        """
        Apaga o último caractere inserido. Se o visor estiver mostrando erro, 
        restaura o texto anterior. Trata funções e o 'pi' como blocos únicos.
        """
        # Se houver erro na tela, recupera o texto que o usuário tinha antes do erro
        if self.__user_input == "Math Error":
            self.__user_input = self.__last_valid_expression
            return

        # Adicionamos "pi" na lista para ser detectado e apagado por completo de uma vez só
        for token in ["sqrt(", "sin(", "cos(", "tan(", "pi"]:
            if self.__user_input.endswith(token):
                self.__user_input = self.__user_input[:-len(token)]
                return

        # Comportamento padrão: apaga apenas o último caractere
        self.__user_input = self.__user_input[:-1]

    def normal_op(self):
        if self.__user_input == "":
            return

        a = self.__last_num
        b = float(self.__user_input)
        self.__repeat_operand = b
        self.__repeat_operation = self.__operation

        if self.__operation == "+":
            self.__result = a + b
        elif self.__operation == "-":
            self.__result = a - b
        elif self.__operation == "x":
            self.__result = a * b
        elif self.__operation == "/":
            if b == 0:
                self.__user_input = "Math Error"
                self.__last_num = None
                self.__operation = None
                return
            self.__result = a / b

        self.__result = round(self.__result, self.__num_dec)
        self.__user_input = str(self.__result)
        self.__last_num = self.__result
        self.__operation = None

    def processar_operador_normal(self, nome_botao):
        if self.__user_input == "Math Error":
            return

        if "EQU" in nome_botao:
            if self.__operation is not None:
                if self.__user_input == "":
                    self.__result = self.__last_num
                    self.__user_input = str(self.__result)
                else:
                    self.normal_op()
            else:
                if self.__repeat_operation is not None and self.__repeat_operand is not None and self.__user_input != "":
                    self.__last_num = float(self.__user_input)
                    self.__operation = self.__repeat_operation
                    self.__user_input = str(self.__repeat_operand)
                    self.normal_op()
                elif self.__user_input != "":
                    self.__result = float(self.__user_input)
        else:
            if self.__user_input == "":
                return
            if self.__operation is not None:
                self.normal_op()

            if self.__user_input != "Math Error":
                self.__last_num = float(self.__user_input)

            if "ADD" in nome_botao:
                self.__operation = "+"
            elif "SUB" in nome_botao:
                self.__operation = "-"
            elif "MUL" in nome_botao:
                self.__operation = "x"
            elif "DIV" in nome_botao:
                self.__operation = "/"
            self.__user_input = ""

    # --- Lógica do Modo Científico com Histórico ---
    def scientific_eval(self):
        if self.__user_input == "":
            return 0.0

        self.__last_valid_expression = self.__user_input
        expr = self.__user_input.replace("x", "*").replace("π", "pi")
        
        try:
            self.__result = eval(
                expr,
                {"__builtins__": None},
                {
                    "sqrt": math.sqrt,
                    "sin": lambda x: math.sin(math.radians(x) if self.__angle_mode == "deg" else x),
                    "cos": lambda x: math.cos(math.radians(x) if self.__angle_mode == "deg" else x),
                    "tan": lambda x: "Math Error" if (self.__angle_mode == "deg" and (x % 180 == 90 or x % 180 == -90)) 
                                     else math.tan(math.radians(x) if self.__angle_mode == "deg" else x),
                    "pi": math.pi,
                }
            )
            
            if self.__result == "Math Error":
                raise ValueError

            if isinstance(self.__result, (int, float)):
                resultado_formatado = str(round(self.__result, self.__num_dec))
                
                # NOVO: Se o cálculo deu certo, monta a string e adiciona na nossa lista de histórico
                linha_historico = f"{self.__last_valid_expression} = {resultado_formatado}"
                self.__history.append(linha_historico)
                
                self.__user_input = resultado_formatado
                
            return self.__result
            
        except:
            self.__user_input = "Math Error"
            return "Math Error"