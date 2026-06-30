# 🧮 Calculadora em Python com PyQt5

Uma aplicação gráfica de calculadora desenvolvida em **Python** utilizando **PyQt5**, seguindo os princípios de **Programação Orientada a Objetos (POO)**. O projeto oferece dois modos de operação: **Calculadora Normal** e **Calculadora Científica**, com interface intuitiva e arquitetura modular.

---

## 📋 Funcionalidades

### Calculadora Normal

- Operações básicas:
  - Adição (`+`)
  - Subtração (`-`)
  - Multiplicação (`*`)
  - Divisão (`/`)
- Botões numéricos (0–9)
- Ponto decimal
- Limpar expressão (`C`)
- Cálculo do resultado (`=`)
- Exibição da expressão e do resultado

### Calculadora Científica

Além de todas as funcionalidades da calculadora normal, inclui:

- Raiz quadrada (`√`)
- Potência ao quadrado (`x²`)
- Porcentagem (`%`)
- Inverso (`1/x`)
- Troca de sinal (`±`)
- Funções trigonométricas:
  - `sin`
  - `cos`
  - `tan`
- Constante matemática `π`

> **Observação:** As funções trigonométricas utilizam **radianos**.

---

## 🖥️ Interface

A interface foi desenvolvida utilizando **PyQt5**, permitindo alternar entre os modos de calculadora através de um menu de seleção.

As conexões entre botões e funcionalidades são realizadas utilizando o mecanismo de sinais e slots do Qt (`clicked.connect`), mantendo a separação entre interface gráfica e lógica da aplicação.

---

## 📁 Estrutura do Projeto

```
CalculadoraPOO/
│
├── main.py                     # Arquivo principal
├── Calculadora.py              # Implementação da lógica da calculadora
├── interface_normal.py         # Interface da calculadora normal
├── interface_cientifica.py     # Interface da calculadora científica
└── menu_selector.py            # Menu para seleção do modo
```

---

## 🏗️ Arquitetura

O projeto segue os princípios de Programação Orientada a Objetos, promovendo:

- Separação entre interface e lógica de negócio;
- Modularização do código;
- Reutilização de componentes;
- Organização em múltiplas classes e arquivos;
- Facilidade para manutenção e expansão do sistema.

---

## 🚀 Tecnologias Utilizadas

- Python 3
- PyQt5

---

## ▶️ Como Executar

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/CalculadoraPOO.git
```

2. Entre na pasta do projeto:

```bash
cd CalculadoraPOO
```

3. Instale as dependências:

```bash
pip install PyQt5
```

4. Execute a aplicação:

```bash
python main.py
```

---

## 💡 Possíveis Melhorias

- Histórico de operações;
- Suporte a expressões matemáticas completas;
- Avaliação segura de expressões (sem uso de `eval`);
- Temas claro e escuro;
- Atalhos de teclado;
- Memória (MC, MR, M+, M-).

---

## ▶️ Instalação (Windows)

Este projeto foi desenvolvido utilizando **Python 3.10**, **Miniforge** e **PyQt5**. Siga os passos abaixo para configurar corretamente o ambiente.

### 1. Instalar o Miniforge

Abra o **Prompt de Comando (CMD)** do Windows e execute um dos comandos abaixo para baixar o instalador.

**PowerShell:**

```powershell
Invoke-WebRequest -Uri https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Windows-x86_64.exe -OutFile Miniforge3.exe
```

**ou**

```bash
curl -L -o Miniforge3.exe https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Windows-x86_64.exe
```

Após o download, execute:

```bash
Miniforge3.exe
```

e siga o assistente de instalação.

---

### 2. Abrir o Miniforge Prompt

Após a instalação:

- Pressione **Windows**
- Digite **Miniforge Prompt**
- Abra o terminal

---

### 3. Criar o ambiente Conda

Crie um ambiente dedicado para o projeto:

```bash
conda create -n qt_env python=3.10
```

---

### 4. Ativar o ambiente

```bash
conda activate qt_env
```

---

### 5. Instalar o PyQt5

Instale o PyQt5 utilizando os pacotes do **conda-forge**:

```bash
conda install -c conda-forge pyqt qt-main
```

---

### 6. Clonar o repositório

```bash
git clone https://github.com/seu-usuario/CalculadoraPOO.git
```

Entre na pasta do projeto:

```bash
cd CalculadoraPOO
```

---

### 7. Executar a aplicação

```bash
python main.py
```

---

## ✅ Requisitos

- Windows 10 ou superior
- Miniforge
- Python 3.10
- PyQt5

---

## 📜 Licença

Este projeto foi desenvolvido para fins educacionais e pode ser utilizado como base para estudos e aprimoramentos.