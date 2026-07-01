import math

class EngineCalculadora:
    """
    Motor lógico de cálculo da calculadora (Model).
    Centraliza todos os estados matemáticos e as operações, garantindo a 
    separação completa entre as regras de negócio e a interface gráfica.
    """
    def __init__(self, num_dec=5):
        # Número de casas decimais para o arredondamento dos resultados
        self.__num_dec = num_dec
        
        # String que armazena o que está sendo digitado ou a expressão atual
        self.__user_input = ""
        
        # Variáveis de estado para a operação sequencial (Modo Normal)
        self.__last_num = None
        self.__operation = None
        
        # Memórias de repetição para o comportamento acumulador do botão '='
        self.__repeat_operand = None
        self.__repeat_operation = None
        
        # Armazena o último resultado válido calculado (Memória ANS)
        self.__result = 0.0
        
        # Backup da última expressão válida para recuperação no Backspace pós-erro
        self.__last_valid_expression = ""
        
        # Modo de unidade angular para funções trigonométricas ("deg" ou "rad")
        self.__angle_mode = "deg"

    # --- Métodos de Encapsulamento (Getters e Setters) ---
    # Expõem os atributos privados de forma controlada para a interface gráfica

    @property
    def user_input(self):
        """Retorna o texto atual do visor."""
        return self.__user_input

    @user_input.setter
    def user_input(self, valor):
        """Permite que a interface modifique o texto do visor."""
        self.__user_input = valor

    @property
    def angle_mode(self):
        """Retorna o modo angular ativo (deg ou rad)."""
        return self.__angle_mode

    @angle_mode.setter
    def angle_mode(self, modo):
        """Altera o modo angular se o valor passado for válido."""
        if modo in ["rad", "deg"]:
            self.__angle_mode = modo

    @property
    def result(self):
        """Expõe o valor contido na memória ANS (último resultado)."""
        return self.__result

    # --- Métodos de Controle e Edição ---

    def clear(self):
        """
        Limpa o estado atual da conta para reiniciar a digitação.
        Nota: O último resultado (self.__result) é preservado para não apagar o ANS.
        """
        self.__user_input = ""
        self.__last_num = None
        self.__operation = None

    def safe_backspace(self):
        """
        Apaga o último caractere inserido. Se o visor estiver mostrando erro, 
        restaura o texto anterior. Trata funções como 'sin(' como blocos únicos.
        """
        # Se houver erro na tela, recupera o texto que o usuário tinha antes do erro
        if self.__user_input == "Math Error":
            self.__user_input = self.__last_valid_expression
            return

        # Verifica se o final da string é um bloco de função para apagá-lo por completo
        for token in ["sqrt(", "sin(", "cos(", "tan("]:
            if self.__user_input.endswith(token):
                self.__user_input = self.__user_input[:-len(token)]
                return

        # Comportamento padrão: apaga apenas o último caractere
        self.__user_input = self.__user_input[:-1]

    # --- Lógica do Modo Normal (Operação Sequencial) ---

    def normal_op(self):
        """
        Executa a operação aritmética pendente utilizando o acumulador 
        e o valor recém-digitado (comportamento padrão de calculadora comum).
        """
        if self.__user_input == "":
            return

        a = self.__last_num
        b = float(self.__user_input)
        
        # Salva os estados atuais para caso o usuário aperte '=' seguidamente
        self.__repeat_operand = b
        self.__repeat_operation = self.__operation

        # Processamento das quatro operações básicas
        if self.__operation == "+":
            self.__result = a + b
        elif self.__operation == "-":
            self.__result = a - b
        elif self.__operation == "x":
            self.__result = a * b
        elif self.__operation == "/":
            # Tratamento protetivo para divisão por zero
            if b == 0:
                self.__user_input = "Math Error"
                self.__last_num = None
                self.__operation = None
                return
            self.__result = a / b

        # Arredonda o valor para evitar problemas de precisão de ponto flutuante
        self.__result = round(self.__result, self.__num_dec)
        self.__user_input = str(self.__result)
        self.__last_num = self.__result
        self.__operation = None

    def processar_operador_normal(self, nome_botao):
        """
        Gerencia o fluxo de cliques em botões de operação (+, -, x, /, =) 
        no modo padrão, decidindo se encadeia cálculos ou se aplica repetições.
        """
        if self.__user_input == "Math Error":
            return

        # --- Caso o botão clicado seja o IGUAL (=) ---
        if "EQU" in nome_botao:
            if self.__operation is not None:
                if self.__user_input == "":
                    # Se houver operador mas sem segundo número, mantém o primeiro
                    self.__result = self.__last_num
                    self.__user_input = str(self.__result)
                else:
                    self.normal_op()
            else:
                # Comportamento acumulador: se o usuário clicar repetidamente em '=',
                # reaplica a última operação usando a memória guardada
                if self.__repeat_operation is not None and self.__repeat_operand is not None and self.__user_input != "":
                    self.__last_num = float(self.__user_input)
                    self.__operation = self.__repeat_operation
                    self.__user_input = str(self.__repeat_operand)
                    self.normal_op()
                elif self.__user_input != "":
                    self.__result = float(self.__user_input)
                    
        # --- Caso seja um operador aritmético (+, -, x, /) ---
        else:
            if self.__user_input == "":
                return
            # Se já existia uma operação pendente na fila, calcula ela primeiro (encadeamento)
            if self.__operation is not None:
                self.normal_op()

            if self.__user_input != "Math Error":
                self.__last_num = float(self.__user_input)

            # Define qual será o próximo operador a ser executado
            if "ADD" in nome_botao:
                self.__operation = "+"
            elif "SUB" in nome_botao:
                self.__operation = "-"
            elif "MUL" in nome_botao:
                self.__operation = "x"
            elif "DIV" in nome_botao:
                self.__operation = "/"
            self.__user_input = ""

    # --- Lógica do Modo Científico (Avaliação de Expressões) ---

    def scientific_eval(self):
        """
        Avalia e calcula a expressão matemática textual montada no visor.
        Utiliza um escopo controlado e seguro dentro do 'eval' para mapear as
        funções e tratar as regras de conversão trigonométrica e indeterminações.
        """
        if self.__user_input == "":
            return 0.0

        # Faz o backup da expressão atual antes de tentar calculá-la
        self.__last_valid_expression = self.__user_input
        
        # Traduz a string do visor para operadores compatíveis com a sintaxe do Python
        expr = self.__user_input.replace("x", "*").replace("π", "pi")
        
        try:
            # Executa a avaliação da string com escopo fechado e builtins desativados (segurança)
            self.__result = eval(
                expr,
                {"__builtins__": None},
                {
                    "sqrt": math.sqrt,
                    # Mapeia as funções trigonométricas respeitando a escolha de DEG ou RAD
                    "sin": lambda x: math.sin(math.radians(x) if self.__angle_mode == "deg" else x),
                    "cos": lambda x: math.cos(math.radians(x) if self.__angle_mode == "deg" else x),
                    
                    # Tratamento explícito para a tangente de 90° (e suas indeterminações periódicas)
                    "tan": lambda x: "Math Error" if (self.__angle_mode == "deg" and (x % 180 == 90 or x % 180 == -90)) 
                                     else math.tan(math.radians(x) if self.__angle_mode == "deg" else x),
                    "pi": math.pi,
                }
            )
            
            # Se a checagem da lambda da tangente disparar a string de erro, força a exceção
            if self.__result == "Math Error":
                raise ValueError

            # Formata e exibe o resultado numérico final limitando as casas decimais
            if isinstance(self.__result, (int, float)):
                self.__user_input = str(round(self.__result, self.__num_dec))
            return self.__result
            
        except:
            # Captura qualquer erro de sintaxe, parênteses abertos ou indeterminação
            self.__user_input = "Math Error"
            return "Math Error"