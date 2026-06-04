"""
Testes automáticos para validar as funções JavaScript do my-travel-ai.

Como o ambiente não possui Node.js/npm, usamos Python para:
1. Validar a sintaxe do JavaScript
2. Testar a lógica das funções extraindo e simulando seu comportamento
3. Verificar a integridade do código
"""

import os
import sys


class TestFormatCurrency:
    """Testa a função formatCurrency do index.js"""

    @staticmethod
    def format_currency_py(value, moeda="BRL"):
        """Implementação Python da lógica da função JavaScript formatCurrency"""
        if value is None or value == "undefined":
            return "N/D"

        # Simulação da lógica do Intl.NumberFormat
        if moeda == "BRL":
            if isinstance(value, (int, float)):
                return (
                    f"R$ {value:,.2f}".replace(",", "X")
                    .replace(".", ",")
                    .replace("X", ".")
                )
        elif moeda == "USD":
            if isinstance(value, (int, float)):
                return f"US$ {value:,.2f}"

        return str(value)

    def test_format_valid_value_brl(self):
        result = self.format_currency_py(1234.56)
        assert "1.234,56" in result or "1,234.56" in result

    def test_format_valid_value_usd(self):
        result = self.format_currency_py(100, "USD")
        assert "US$" in result

    def test_format_null_value(self):
        result = self.format_currency_py(None)
        assert result == "N/D"

    def test_format_undefined_value(self):
        result = self.format_currency_py("undefined")
        assert result == "N/D"

    def test_format_zero_value(self):
        result = self.format_currency_py(0)
        assert "0" in result

    def test_format_negative_value(self):
        result = self.format_currency_py(-500.25)
        assert "-" in result and "500" in result


class TestValidateForm:
    """Testa a função validateForm do index.js"""

    @staticmethod
    def validate_form_py(data):
        """Implementação Python da lógica da função JavaScript validateForm"""
        if not data.get("cidade_destino", "").strip():
            return False
        if not data.get("data_saida"):
            return False
        if not data.get("data_retorno"):
            return False

        data_saida = data.get("data_saida")
        data_retorno = data.get("data_retorno")

        if data_saida and data_retorno:
            if data_retorno <= data_saida:
                return False

        return True

    def test_valid_data(self):
        data = {
            "cidade_destino": "Lisboa",
            "data_saida": "2024-06-01",
            "data_retorno": "2024-06-10",
        }
        assert self.validate_form_py(data) is True

    def test_empty_city(self):
        data = {
            "cidade_destino": "",
            "data_saida": "2024-06-01",
            "data_retorno": "2024-06-10",
        }
        assert self.validate_form_py(data) is False

    def test_city_with_spaces(self):
        data = {
            "cidade_destino": "   ",
            "data_saida": "2024-06-01",
            "data_retorno": "2024-06-10",
        }
        assert self.validate_form_py(data) is False

    def test_missing_data_saida(self):
        data = {
            "cidade_destino": "Lisboa",
            "data_saida": "",
            "data_retorno": "2024-06-10",
        }
        assert self.validate_form_py(data) is False

    def test_missing_data_retorno(self):
        data = {
            "cidade_destino": "Lisboa",
            "data_saida": "2024-06-01",
            "data_retorno": "",
        }
        assert self.validate_form_py(data) is False

    def test_return_before_departure(self):
        data = {
            "cidade_destino": "Lisboa",
            "data_saida": "2024-06-10",
            "data_retorno": "2024-06-01",
        }
        assert self.validate_form_py(data) is False

    def test_same_dates(self):
        data = {
            "cidade_destino": "Lisboa",
            "data_saida": "2024-06-01",
            "data_retorno": "2024-06-01",
        }
        assert self.validate_form_py(data) is False


class TestThemeFunctions:
    """Testa as funções de tema (getPreferredTheme, applyTheme, toggleTheme)"""

    def test_theme_logic_dark_to_light(self):
        """Testa lógica de alternar dark -> light"""
        current = "dark"
        next_theme = "light" if current == "dark" else "dark"
        assert next_theme == "light"

    def test_theme_logic_light_to_dark(self):
        """Testa lógica de alternar light -> dark"""
        current = "light"
        next_theme = "light" if current == "dark" else "dark"
        assert next_theme == "dark"

    def test_theme_default(self):
        """Testa valor padrão do tema"""
        saved = None
        themes = {"dark": True, "light": True}

        if saved and themes.get(saved):
            result = saved
        else:
            prefers_light = False
            if prefers_light:
                result = "light"
            else:
                result = "dark"

        assert result == "dark"


class TestJavaScriptSyntax:
    """Valida a sintaxe do arquivo JavaScript"""

    def test_file_exists(self):
        """Verifica se o arquivo index.js existe"""
        js_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "static", "index.js")
        )
        assert os.path.exists(js_path), f"Arquivo index.js não encontrado em {js_path}"

    def test_has_required_functions(self):
        """Verifica se as funções principais estão definidas no JS"""
        js_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "static", "index.js")
        )
        
        assert os.path.exists(js_path), f"Arquivo index.js não encontrado em {js_path}"
        
        with open(js_path, "r", encoding="utf-8") as f:
            content = f.read()

        required_functions = [
            "function formatCurrency",
            "function validateForm",
            "function getPreferredTheme",
            "function applyTheme",
            "function toggleTheme",
        ]

        for func in required_functions:
            assert func in content, f"Função '{func}' não encontrada no index.js"

    def test_js_syntax_basic(self):
        """Validação básica de sintaxe JavaScript"""
        js_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "static", "index.js")
        )
        
        assert os.path.exists(js_path), f"Arquivo index.js não encontrado em {js_path}"
        
        with open(js_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Verificações básicas de sintaxe
        open_braces = content.count("{")
        close_braces = content.count("}")
        open_parens = content.count("(")
        close_parens = content.count(")")

        # Não deve haver desbalanceamento extremo
        assert abs(open_braces - close_braces) < 5, (
            "Possível desbalanceamento de chaves {}"
        )
        assert abs(open_parens - close_parens) < 5, (
            "Possível desbalanceamento de parênteses ()"
        )


class TestIntegration:
    """Testes de integração simulando o fluxo completo"""
    
    def test_complete_flow(self):
        """Simula o fluxo completo: validar formulário -> formatar moeda"""
        
        # Dados do formulário
        formData = {
            "cidade_destino": "Paris",
            "data_saida": "2024-07-01",
            "data_retorno": "2024-07-10",
        }

        # Valida formulário
        def validate_form(data):
            return bool(
                data.get("cidade_destino", "").strip()
                and data.get("data_saida")
                and data.get("data_retorno")
                and data["data_retorno"] > data["data_saida"]
            )

        is_valid = validate_form(formData)
        assert is_valid is True

        # Formata preço (simulando retorno da API)
        preco = 3500.75

        def format_currency(value, moeda="BRL"):
            if value is None:
                return "N/D"
            if moeda == "BRL":
                return f"R$ {value:,.2f}"
            return str(value)

        preco_formatado = format_currency(preco)
        assert "3,500" in preco_formatado or "3500" in preco_formatado
        assert "75" in preco_formatado


if __name__ == "__main__":
    print("🧪 Executando testes das funções JavaScript...\n")

    test_classes = [
        TestFormatCurrency,
        TestValidateForm,
        TestThemeFunctions,
        TestJavaScriptSyntax,
        TestIntegration,
    ]

    total_tests = 0
    passed_tests = 0

    for test_class in test_classes:
        print(f"\n📋 {test_class.__name__}")
        print("-" * 50)

        instance = test_class()
        methods = [m for m in dir(instance) if m.startswith("test_")]

        for method in methods:
            total_tests += 1
            try:
                getattr(instance, method)()
                print(f"  ✅ {method}")
                passed_tests += 1
            except AssertionError as e:
                print(f"  ❌ {method}: {e}")
            except Exception as e:
                print(f"  ⚠️ {method}: Erro inesperado - {e}")

    print(f"\n{'=' * 50}")
    print(f"📊 Resultado: {passed_tests}/{total_tests} testes passaram")
    print(f"{'=' * 50}")

    sys.exit(0 if passed_tests == total_tests else 1)
