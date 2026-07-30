UV := uv
PYTHON := .venv/bin/python

.PHONY: setup install run clean lock update add remove sync

# Cria a venv e instala exatamente o que está no uv.lock
setup:
	$(UV) venv
	$(UV) sync

# Alias para setup
install: setup

# Executa o projeto
run:
	$(UV) run python hand_controller.py

# Atualiza o lockfile
lock:
	$(UV) lock

# Atualiza todas as dependências
update:
	$(UV) lock --upgrade
	$(UV) sync

# Sincroniza a venv com o lock
sync:
	$(UV) sync

# Adiciona uma dependência
# Uso: make add PKG=pygame
add:
	@if [ -z "$(PKG)" ]; then \
		echo "Uso: make add PKG=nome_do_pacote"; \
		exit 1; \
	fi
	$(UV) add $(PKG)

# Remove uma dependência
# Uso: make remove PKG=pygame
remove:
	@if [ -z "$(PKG)" ]; then \
		echo "Uso: make remove PKG=nome_do_pacote"; \
		exit 1; \
	fi
	$(UV) remove $(PKG)

# Limpa o projeto
clean:
	rm -rf .venv
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete