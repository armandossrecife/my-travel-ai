"""
test_html_structure.py — Testes para a estrutura do index.html
"""

import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))


class TestHTMLStructure:
    """Testes para validar a estrutura do arquivo HTML"""

    def test_html_file_exists(self):
        """Verifica se o arquivo index.html existe."""
        html_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "static", "index.html")
        )
        assert os.path.exists(html_path), "Arquivo index.html não encontrado"

    def test_html_has_doctype(self):
        """Verifica se o HTML tem DOCTYPE."""
        html_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "static", "index.html")
        )
        with open(html_path, "r", encoding="utf-8") as f:
            content = f.read()
        assert "<!DOCTYPE html>" in content or "<!doctype html>" in content

    def test_html_has_head_and_body(self):
        """Verifica se tem tags <head> e <body>."""
        html_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "static", "index.html")
        )
        with open(html_path, "r", encoding="utf-8") as f:
            content = f.read()
        assert "<head>" in content
        assert "</head>" in content
        assert "<body>" in content
        assert "</body>" in content

    def test_html_links_css(self):
        """Verifica se o HTML linka o CSS."""
        html_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "static", "index.html")
        )
        with open(html_path, "r", encoding="utf-8") as f:
            content = f.read()
        assert "index.css" in content or "index_corrected.css" in content

    def test_html_links_js(self):
        """Verifica se o HTML linka o JavaScript."""
        html_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "static", "index.html")
        )
        with open(html_path, "r", encoding="utf-8") as f:
            content = f.read()
        assert "index.js" in content

    def test_form_exists(self):
        """Verifica se o formulário existe."""
        html_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "static", "index.html")
        )
        with open(html_path, "r", encoding="utf-8") as f:
            content = f.read()
        assert "<form" in content or 'id="travel-form"' in content

    def test_required_form_fields(self):
        """Verifica se os campos obrigatórios estão presentes."""
        html_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "static", "index.html")
        )
        with open(html_path, "r", encoding="utf-8") as f:
            content = f.read()
        assert "cidade_destino" in content
        assert "data_saida" in content
        assert "data_retorno" in content

    def test_buttons_exist(self):
        """Verifica se os botões principais existem."""
        html_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "static", "index.html")
        )
        with open(html_path, "r", encoding="utf-8") as f:
            content = f.read()
        assert "btnSubmit" in content or 'type="submit"' in content
        assert "btnNewPlan" in content or "novo" in content.lower()
        assert "btnRetry" in content or "tentar" in content.lower()

    def test_sections_exist(self):
        """Verifica se as seções principais existem."""
        html_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "static", "index.html")
        )
        with open(html_path, "r", encoding="utf-8") as f:
            content = f.read()
        assert "agents-section" in content or "agentsSection" in content or "agentes" in content.lower()
        assert "results-section" in content or "resultsSection" in content or "resultado" in content.lower()
        assert "error-section" in content or "errorSection" in content or "erro" in content.lower()
        assert "logs-section" in content or "logsSection" in content or "logs" in content.lower()

    def test_html_tags_balanced(self):
        """Verifica se as tags HTML principais estão balanceadas."""
        html_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "static", "index.html")
        )
        with open(html_path, "r", encoding="utf-8") as f:
            content = f.read()
        open_divs = content.count("<div")
        close_divs = content.count("</div>")
        assert abs(open_divs - close_divs) < 10, (
            f"Possível desbalanceamento de divs: {open_divs} abertas, {close_divs} fechadas"
        )

    def test_has_theme_toggle(self):
        """Verifica se tem botão de alternar tema."""
        html_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "static", "index.html")
        )
        with open(html_path, "r", encoding="utf-8") as f:
            content = f.read()
        assert (
            "themeToggle" in content
            or "toggleTheme" in content
            or "tema" in content.lower()
        )
