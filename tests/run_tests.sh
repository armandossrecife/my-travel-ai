#!/bin/bash

echo "🧪 MY TRAVEL AI - SUITE DE TESTES"
echo "=================================="
echo ""

# Cores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Diretório base - usar caminho absoluto do script
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Navega para a raiz do projeto
cd "$PROJECT_ROOT"

# Verifica se está no diretório correto
if [ ! -d "tests" ]; then
    echo "Erro: Diretório 'tests/' não encontrado. Execute a partir do diretório correto."
    echo "Diretório atual: $(pwd)"
    exit 1
fi

echo "Diretório do projeto: $(pwd)"
echo ""

# 1. Testes do Backend (API + Agentes)
echo -e "${YELLOW}📦 Executando Testes do Backend...${NC}"
echo "----------------------------------------"
python -m pytest tests/backend/ -v --tb=short
BACKEND_RESULT=$?

if [ $BACKEND_RESULT -eq 0 ]; then
    echo -e "${GREEN}✅ Testes do Backend: PASSOU${NC}"
else
    echo -e "${RED}❌ Testes do Backend: FALHOU${NC}"
fi

echo ""

# 2. Testes do Frontend
echo -e "${YELLOW}🌐 Executando Testes do Frontend...${NC}"
echo "----------------------------------------"
python -m pytest tests/frontend/ -v --tb=short
FRONTEND_RESULT=$?

if [ $FRONTEND_RESULT -eq 0 ]; then
    echo -e "${GREEN}✅ Testes do Frontend: PASSOU${NC}"
else
    echo -e "${RED}❌ Testes do Frontend: FALHOU${NC}"
fi

echo ""

# 3. Testes de Integração (opcional, pode demorar)
echo -e "${YELLOW}🔗 Executando Testes de Integração...${NC}"
echo "----------------------------------------"
python -m pytest tests/integration/ -v --tb=short
INTEGRATION_RESULT=$?

if [ $INTEGRATION_RESULT -eq 0 ]; then
    echo -e "${GREEN}✅ Testes de Integração: PASSOU${NC}"
else
    echo -e "${RED}❌ Testes de Integração: FALHOU${NC}"
fi

echo ""
echo "=================================="
echo -e "${YELLOW}📊 RESUMO DOS TESTES${NC}"
echo "=================================="

if [ $BACKEND_RESULT -eq 0 ]; then
    echo -e "Backend:  ${GREEN}PASSOU${NC}"
else
    echo -e "Backend:  ${RED}FALHOU${NC}"
fi

if [ $FRONTEND_RESULT -eq 0 ]; then
    echo -e "Frontend: ${GREEN}PASSOU${NC}"
else
    echo -e "Frontend: ${RED}FALHOU${NC}"
fi

if [ $INTEGRATION_RESULT -eq 0 ]; then
    echo -e "Integração: ${GREEN}PASSOU${NC}"
else
    echo -e "Integração: ${RED}FALHOU${NC}"
fi

echo ""
echo "=================================="

# Exit com erro se algum teste falhou
if [ $BACKEND_RESULT -ne 0 ] || [ $FRONTEND_RESULT -ne 0 ] || [ $INTEGRATION_RESULT -ne 0 ]; then
    exit 1
fi

exit 0
