import math

class EngineCalculadora:
    def __init__(self, num_dec=5):
        # Atributos encapsulados (privados)
        self.__num_dec = num_dec
        self.__user_input = ""
        self.__last_num = None
        self.__operation = None
        self.__repeat_operand = None
        self.__repeat_operation = None
        self.__result = 0.0
        self.__last_valid_expression = ""
        self.__angle_mode = "deg"  # "rad" ou "deg"

    # Getters e Setters para expor APENAS o necessário de forma segura
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

    def safe_backspace(self):
        if self.__user_input == "Math Error":
            self.__user_input = self.__last_valid_expression
            return

        for token in ["sqrt(", "sin(", "cos(", "tan("]:
            if self.__user_input.endswith(token):
                self.__user_input = self.__user_input[:-len(token)]
                return

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
                self.__result = 0.0
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
                    "tan": lambda x: math.tan(math.radians(x) if self.__angle_mode == "deg" else x),
                    "pi": math.pi,
                }
            )
            if isinstance(self.__result, (int, float)):
                self.__user_input = str(round(self.__result, self.__num_dec))
            return self.__result
        except:
            self.__user_input = "Math Error"
            return "Math Error"