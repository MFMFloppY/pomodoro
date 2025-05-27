.DEFAULT_GOAL := help

APP = app
MAIN = main
ENV_FILE = ./.main.env


clean: 
	@echo "Cleaning up Python directories..."
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -r {} +
	find . -name "*.log" -delete
	find . -name "*.log.*" -delete
	find . -name ".ruff_cache" -type d -exec rm -r {} +

help: ## Выводит список доступных комманд
	@echo "Commands:"
	@grep -E '^[a-zA-Z0-9_-]+:.*?##' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'

update: ## Обновление пакета poetry до последней версии
	poetry self update

# Alembic команды:
createmigration: ## Генерирует миграцию в базу данных
	alembic revision --autogenerate -m $(MIGRATION)

applymigration: ## Применяет изменения к базе данных
	alembic upgrade head

downgrade: ## Откатывает базу данных до указанной ревизии
	alembic downgrade $(REVISION)

# Запуск и остановка основного приложения:
run: ## Запуск приложения 
	uvicorn $(MAIN):$(APP) --reload --host 127.0.0.1 --port 8000 --timeout-graceful-shutdown 15 & echo $$! > uvicorn.pid

stop: ## Вырубает все к хуям 
	@echo "Stopping Uvicorn..."
	@if [ -f uvicorn.pid ]; then \
        kill $$(cat uvicorn.pid) && \
        rm -f uvicorn.pid; \
    else \
        echo "No running process found"; \
    fi

## После вылета терминала, проверь убит ли процесс "netstat -ano | find "LISTEN"", если процесс на ...:8000 запущен, используй "make stop"!!!

# Docker-compose команды:
up: ## Запуск контейнера базы данных
	docker-compose up

down: ## Остановка контейнера базы данных
	docker-compose down