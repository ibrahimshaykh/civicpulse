.PHONY: up down logs ps offline

up:
	docker compose up -d --build

down:
	docker compose down

logs:
	docker compose logs -f

ps:
	docker compose ps

# DK-06: brings up ollama (profile "offline") and pulls the model
# Settings.ollama_model defaults to, so TRIAGE_PROVIDER=ollama works with
# no network calls to Groq or anywhere else.
offline:
	docker compose --profile offline up -d ollama
	docker compose exec ollama ollama pull llama3.2:1b
