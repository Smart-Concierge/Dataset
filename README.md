# Projeto Portaria Inteligente

Este repositório contém os códigos e datasets para o desenvolvimento do sistema de NLU (Natural Language Understanding) para uma portaria inteligente.

## 🚀 Configuração do Ambiente de Desenvolvimento

Para garantir que todos os desenvolvedores trabalhem com as mesmas dependências e versões de pacotes, utilizamos um ambiente virtual gerenciado pelo Conda.

### Pré-requisitos

O único pré-requisito é ter o **Miniconda** instalado em seu sistema.

<details>
<summary>🐧 <strong>Clique aqui para ver as instruções de instalação do Miniconda no Linux via terminal.</strong></summary>

#### Instalando o Miniconda no Linux

1.  **Baixe o script de instalação:**
    Abra o terminal e use o comando `curl` para baixar a versão mais recente.
    ```bash
    curl -O [https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh](https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh)
    ```

2.  **Execute o script de instalação:**
    Este comando instala o Miniconda de forma silenciosa (`-b`) no diretório padrão do seu usuário (`-p $HOME/miniconda`).
    ```bash
    bash Miniconda3-latest-Linux-x86_64.sh -b -p $HOME/miniconda
    ```

3.  **Inicialize o Conda no seu Shell:**
    Este passo configura seu terminal para reconhecer o comando `conda`.
    ```bash
    ~/miniconda/bin/conda init bash
    ```
    *(Se você usa um shell diferente, como o Zsh, substitua `bash` por `zsh`)*.

4.  **Reinicie o Terminal:**
    **Feche a janela atual e abra uma nova.** As mudanças só terão efeito em uma nova sessão do terminal. Você deverá ver `(base)` no início do seu prompt.

5.  **Verifique a Instalação:**
    ```bash
    conda --version
    ```
    Se o comando retornar a versão do Conda, a instalação foi bem-sucedida.

</details>

### Passos para a Instalação do Ambiente do Projeto

1.  **Clone o Repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
    cd seu-repositorio
    ```

2.  **Crie o Ambiente Conda:**
    Use o arquivo `environment.yml` para criar o ambiente com todas as dependências necessárias. O nome do ambiente será `portaria-ia`.
    ```bash
    conda env create -f environment.yml
    ```
    *Este comando pode levar alguns minutos, pois irá baixar e instalar todos os pacotes.*

3.  **Ative o Ambiente:**
    Antes de trabalhar no projeto, você **sempre** deve ativar o ambiente recém-criado.
    ```bash
    conda activate portaria-ia
    ```
    *Você saberá que funcionou pois o nome do seu terminal mudará para `(portaria-ia) ...`*

4.  **Verifique a Instalação:**
    Com o ambiente ativo, você pode verificar se os pacotes foram instalados corretamente.
    ```bash
    conda list pandas
    ```
    *Isso deve mostrar o `pandas` na lista de pacotes instalados.*

Pronto! Seu ambiente está configurado e pronto para ser usado.

## 📓 Como Usar

- **Para desativar o ambiente** quando terminar de trabalhar, use o comando:
  ```bash
  conda deactivate
  ```

- **Para atualizar as bibliotecas** caso o arquivo `environment.yml` seja modificado, use o comando com o ambiente ativo:
  ```bash
  conda env update --file environment.yml --prune
  ```
  *O comando `--prune` remove pacotes que não estão mais listados no arquivo, mantendo o ambiente limpo.*