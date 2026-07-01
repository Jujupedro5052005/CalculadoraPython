class ElementsUI:

    @staticmethod
    def digit_buttons(ui_type, screen):
        if screen == "ui_normal":
            return {
                0: ui_type.ui.pushButtonDigitoN0,
                1: ui_type.ui.pushButtonDigitoN1,
                2: ui_type.ui.pushButtonDigitoN2,
                3: ui_type.ui.pushButtonDigitoN3,
                4: ui_type.ui.pushButtonDigitoN4,
                5: ui_type.ui.pushButtonDigitoN5,
                6: ui_type.ui.pushButtonDigitoN6,
                7: ui_type.ui.pushButtonDigitoN7,
                8: ui_type.ui.pushButtonDigitoN8,
                9: ui_type.ui.pushButtonDigitoN9,
                10: ui_type.ui.pushButtonVoltar,
                11: ui_type.ui.pushButtonN_BACK,
                12: ui_type.ui.pushButtonN_ANS,
                13: ui_type.ui.pushButtonN_Clear,
                14: ui_type.ui.pushButtonN_DOT,
                15: ui_type.ui.pushButtonOPN_DIV,
                16: ui_type.ui.pushButtonOPN_MUL,
                17: ui_type.ui.pushButtonOPN_SUB,
                18: ui_type.ui.pushButtonOPN_ADD,
                19: ui_type.ui.pushButtonOPN_EQU,
            }
        
        if screen == "ui_cientifica":
            return {
                0: ui_type.ui.pushButtonDigitoC0,
                1: ui_type.ui.pushButtonDigitoC1,
                2: ui_type.ui.pushButtonDigitoC2,
                3: ui_type.ui.pushButtonDigitoC3,
                4: ui_type.ui.pushButtonDigitoC4,
                5: ui_type.ui.pushButtonDigitoC5,
                6: ui_type.ui.pushButtonDigitoC6,
                7: ui_type.ui.pushButtonDigitoC7,
                8: ui_type.ui.pushButtonDigitoC8,
                9: ui_type.ui.pushButtonDigitoC9,
                10: ui_type.ui.pushButtonVoltar,
                11: ui_type.ui.pushButtonC_BACK,
                12: ui_type.ui.pushButtonC_ANS,
                13: ui_type.ui.pushButtonC_Clear,
                14: ui_type.ui.pushButtonC_DOT,
                15: ui_type.ui.pushButtonOPC_DIV,
                16: ui_type.ui.pushButtonOPC_MUL,
                17: ui_type.ui.pushButtonOPC_SUB,
                18: ui_type.ui.pushButtonOPC_ADD,
                19: ui_type.ui.pushButtonOPC_EQU,
                20: ui_type.ui.pushButtonOPC_Paren1,    # abre parenteses
                21: ui_type.ui.pushButtonOPC_Paren2,    # fecha parenteses
                22: ui_type.ui.pushButtonOPC_SQRT,      # raiz quadrada
                23: ui_type.ui.pushButtonOPC_POW,       # elevado ao quadrado
                24: ui_type.ui.pushButtonOPC_PER,       # porcentagem
                25: ui_type.ui.pushButtonOPC_INV,       # inverso
                26: ui_type.ui.pushButtonOPC_SIN,       # seno
                27: ui_type.ui.pushButtonOPC_COS,       # cosseno
                28: ui_type.ui.pushButtonOPC_TAN,       # tangente
                29: ui_type.ui.pushButtonOPC_PI,        # úmero PI
                30: ui_type.ui.pushButtonOPC_PLUS_MINUS,
                31: ui_type.ui.pushButtonOPC_TOGGLE_ANGLE
            }
    