#!/usr/bin/env bash
# run.sh — Script para instalar dependências e iniciar o servidor TravelAI

set -e

VENV_DIR=".venv"
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║   ✈️  TravelAI — Agente de Viagens        ║"
echo "╚══════════════════════════════════════════╝"
echo ""

cd "$PROJECT_DIR"

# Verifica uv
if ! command -v uv &>/dev/null; then
  echo "❌ 'uv' não encontrado. Instale com: curl -Ls https://astral.sh/uv | bash"
  exit 1
fi

echo "📦 Instalando dependências..."
uv venv "$VENV_DIR" --python 3.11 2>/dev/null || uv venv "$VENV_DIR" 2>/dev/null || true
uv pip install -r requirements.txt --quiet

echo ""
echo "✅ Dependências instaladas!"
echo ""

# Aviso sobre GEMINI_API_KEY
if [ -z "$GEMINI_API_KEY" ]; then
  echo "ℹ️  GEMINI_API_KEY não configurada."
  echo "   A aplicação rodará com o motor de heurística local."
  echo "   Para usar Gemini LLM real: export GEMINI_API_KEY=sua_chave"
else
  echo "🤖 GEMINI_API_KEY detectada! Usando Google Gemini como motor de IA."
fi

echo ""
echo "🚀 Iniciando servidor em http://127.0.0.1:8000"
echo "   Acesse a interface web em http://127.0.0.1:8000"
echo "   Documentação da API em   http://127.0.0.1:8000/docs"
echo ""
echo "   Pressione Ctrl+C para encerrar."
echo ""

uv run uvicorn main:app --host 127.0.0.1 --port 8000 --reload