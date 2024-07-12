# código varre os arquivos e adiciona no gitignore aqueles acima de 50 MB
import os

# Defina o limite de tamanho em bytes (50MB)
size_limit = 50 * 1024 * 1024

# Caminho do repositório Git
repo_path = "."

# Caminho do arquivo .gitignore
gitignore_path = os.path.join(repo_path, ".gitignore")

# Função para verificar o tamanho do arquivo
def check_file_size(filepath):
    return os.path.getsize(filepath) > size_limit

# Lista de arquivos a serem adicionados ao .gitignore
files_to_ignore = []

# Percorrer o repositório
for root, dirs, files in os.walk(repo_path):
    for file in files:
        file_path = os.path.join(root, file)
        if check_file_size(file_path):
            # Adicionar ao .gitignore se o tamanho exceder o limite
            relative_path = os.path.relpath(file_path, repo_path)
            files_to_ignore.append(relative_path)

# Adicionar os arquivos ao .gitignore
with open(gitignore_path, "a") as gitignore_file:
    for file in files_to_ignore:
        gitignore_file.write(f"\n{file}")

print("Arquivos grandes adicionados ao .gitignore.")
