import json
import os

ARQUIVO = "tasks.json"

def carregar_tarefas():
    if not os.path.exists(ARQUIVO):
        return []
    with open(ARQUIVO, "r") as f:
        return json.load(f)

def salvar_tarefas(tarefas):
    with open(ARQUIVO, "w") as f:
        json.dump(tarefas, f, indent=4)

def mostrar_tarefas(tarefas):
    if not tarefas:
        print("📭 Nenhuma tarefa encontrada.")
        return
    for i, tarefa in enumerate(tarefas, 1):
        status = "✔️" if tarefa["concluida"] else "❌"
        print(f"{i}. {tarefa['descricao']} [{status}]")

def adicionar_tarefa(tarefas):
    desc = input("Digite a descrição da tarefa: ").strip()
    if desc:
        tarefas.append({"descricao": desc, "concluida": False})
        salvar_tarefas(tarefas)
        print("✅ Tarefa adicionada!")
    else:
        print("⚠️ Descrição vazia.")

def concluir_tarefa(tarefas):
    mostrar_tarefas(tarefas)
    try:
        idx = int(input("Digite o número da tarefa concluída: "))
        tarefas[idx - 1]["concluida"] = True
        salvar_tarefas(tarefas)
        print("🎉 Tarefa marcada como concluída!")
    except (ValueError, IndexError):
        print("⚠️ Número inválido.")

def remover_tarefa(tarefas):
    mostrar_tarefas(tarefas)
    try:
        idx = int(input("Digite o número da tarefa a remover: "))
        removida = tarefas.pop(idx - 1)
        salvar_tarefas(tarefas)
        print(f"🗑️ Tarefa '{removida['descricao']}' removida!")
    except (ValueError, IndexError):
        print("⚠️ Número inválido.")

def menu():
    tarefas = carregar_tarefas()
    while True:
        print("\n--- MENU ---")
        print("1. Ver tarefas")
        print("2. Adicionar tarefa")
        print("3. Concluir tarefa")
        print("4. Remover tarefa")
        print("5. Sair")
        escolha = input("Escolha uma opção: ")
        
        if escolha == "1":
            mostrar_tarefas(tarefas)
        elif escolha == "2":
            adicionar_tarefa(tarefas)
        elif escolha == "3":
            concluir_tarefa(tarefas)
        elif escolha == "4":
            remover_tarefa(tarefas)
        elif escolha == "5":
            print("👋 Até mais!")
            break
        else:
            print("❌ Opção inválida.")

if __name__ == "__main__":
    menu()
