# To-Do List em Python (CLI)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)

Uma aplicação de linha de comando (CLI) para gerenciamento de tarefas, desenvolvida em Python. Permite ao usuário adicionar, listar, concluir e remover tarefas de forma simples e eficiente, com todos os dados persistidos localmente em um arquivo JSON.

Este projeto serviu como um exercício prático para aprofundar conceitos fundamentais de Python, incluindo manipulação de arquivos, estruturas de dados e a criação de uma interface de usuário interativa no terminal.

## ✨ Funcionalidades Principais

-    **Adicionar:** Crie novas tarefas com uma descrição.
-    **Listar:** Visualize todas as tarefas, com status de concluída ou pendente.
-    **Concluir:** Marque tarefas como concluídas.
-    **Remover:** Exclua tarefas da lista.
-    **Filtrar:** Exiba apenas as tarefas pendentes ou as já concluídas.
-    **Persistência de Dados:** As tarefas são salvas em `tasks.json`, garantindo que não se percam ao fechar o programa.

## Como Rodar o Projeto

Siga os passos abaixo para executar o projeto localmente.

### Pré-requisitos

-   [Python 3.8](https://www.python.org/downloads/) ou superior instalado.
-   [Git](https://git-scm.com/downloads/) instalado para clonar o repositório.

### Instalação e Execução

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/alana-britoc/to-do-list-python.git](https://github.com/alana-britoc/to-do-list-python.git)
    ```

2.  **Navegue até o diretório do projeto:**
    ```bash
    cd to-do-list-python
    ```

3.  **Execute a aplicação:**
    ```bash
    python main.py
    ```

4.  Pronto! Agora basta seguir as opções apresentadas no menu do terminal.

## Próximos Passos (Roadmap)

Este projeto está em constante evolução. Os próximos passos planejados são:

-   [x] Criar filtros para visualizar tarefas pendentes/concluídas.
-   [ ] Implementar a funcionalidade de **editar** uma tarefa existente.
-   [ ] Adicionar **níveis de prioridade** (ex: alta, média, baixa) para as tarefas.
-   [ ] Desenvolver uma interface gráfica com **Tkinter** ou **PyQt**.
-   [ ] Criar uma versão web da aplicação com **Flask** ou **FastAPI**.

---

Desenvolvido por **Alana Brito**.