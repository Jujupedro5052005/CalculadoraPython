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
- Potência (`x²`)
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

# 📁 Estrutura do Projeto

```
CalculadoraPOO/
│
├── main.py                     # Arquivo principal
├── Calculadora.py              # Lógica da calculadora
├── interface_normal.py         # Interface da calculadora normal
├── interface_cientifica.py     # Interface da calculadora científica
└── menu_selector.py            # Menu de seleção do modo
```

---

# 🚀 Instalação do Ambiente (Windows)

O projeto foi desenvolvido utilizando **Python 3.10**, **Miniforge** e **PyQt5**.

## 1. Instalar o Miniforge

Abra o **Prompt de Comando (CMD)** do Windows (não precisa ser administrador).

### Opção 1 (PowerShell)

```powershell
Invoke-WebRequest -Uri https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Windows-x86_64.exe -OutFile Miniforge3.exe
```

### Opção 2 (curl)

```bash
curl -L -o Miniforge3.exe https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Windows-x86_64.exe
```

Após o download, execute:

```bash
Miniforge3.exe
```

e siga normalmente o instalador.

---

## 2. Abrir o Miniforge Prompt

Após instalar o Miniforge:

- Pressione a tecla **Windows**
- Digite:

```
Miniforge Prompt
```

- Abra o terminal.

---

## 3. Criar um ambiente Conda

Crie um ambiente dedicado para o projeto:

```bash
conda create -n qt_env python=3.10
```

Este ambiente isola a instalação do Python e evita conflitos com outras versões instaladas no computador.

---

## 4. Ativar o ambiente

```bash
conda activate qt_env
```

---

## 5. Instalar o PyQt5

Instale o Qt através do canal oficial do **conda-forge**:

```bash
conda install -c conda-forge pyqt qt-main
```

---

## 6. Abrir o Qt Designer

Após instalar o PyQt5, existem duas formas de abrir o Qt Designer.

### Opção 1

```bash
designer
```

### Opção 2

```bash
%CONDA_PREFIX%\Library\bin\designer.exe
```

---

## 7. Clonar o repositório

```bash
git clone https://github.com/SEU-USUARIO/CalculadoraPOO.git
```

Entre na pasta do projeto:

```bash
cd CalculadoraPOO
```

---

## 8. Executar a aplicação

```bash
python main.py
```

---

# 🎯 Resumo da Instalação

```bash
conda create -n qt_env python=3.10

conda activate qt_env

conda install -c conda-forge pyqt qt-main

%CONDA_PREFIX%\Library\bin\designer.exe
```

---

# 🖥️ Convertendo arquivos `.ui` para Python

Após criar uma interface utilizando o **Qt Designer**, é necessário convertê-la para um arquivo Python utilizando o comando `pyuic5`.

Entre na pasta onde está localizado o arquivo `.ui` e execute:

```bash
pyuic5 <nome_da_tela>.ui -o <nome_da_tela>.py -x
```

### Exemplo

```bash
pyuic5 inicial.ui -o inicial.py -x
```

Também é possível converter várias interfaces de uma única vez:

```bash
pyuic5 inicial.ui -o inicial.py -x ^
pyuic5 cientifica.ui -o cientifica.py -x ^
pyuic5 normal.ui -o normal.py -x
```

> No Windows, também pode ser utilizado:

```bash
pyuic5 inicial.ui -o inicial.py -x & pyuic5 cientifica.ui -o cientifica.py -x & pyuic5 normal.ui -o normal.py -x
```

Depois da conversão, basta executar normalmente o arquivo Python gerado.

---

# 📦 Utilizando o projeto no VS Code

Caso deseje apenas executar o projeto no VS Code (sem utilizar o ambiente Conda), instale o PyQt5 com o pip:

```bash
pip install PyQt5
```

Exemplo:

```bash
PS C:\Users\joao.silva\Documents> pip install PyQt5
```

---

# 🏗️ Arquitetura

O projeto segue os princípios da Programação Orientada a Objetos (POO), promovendo:

- Separação entre interface e lógica da aplicação;
- Organização modular;
- Reutilização de código;
- Facilidade para manutenção e expansão.

---

# 💡 Possíveis Melhorias

- Histórico de operações;
- Temas claro e escuro;
- Suporte a expressões matemáticas completas;
- Avaliação segura de expressões sem utilização de `eval`;
- Atalhos de teclado;
- Memória da calculadora (MC, MR, M+, M-).

---

# 📜 Licença

Projeto desenvolvido para fins educacionais, podendo ser utilizado livremente como base para estudos e aprimoramentos.