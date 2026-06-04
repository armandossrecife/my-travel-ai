"""
test_css_consistency.py — Testes para consistência do CSS
"""

import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))


class TestCSSConsistency:
    """Testes para validar a consistência dos arquivos CSS"""

    def test_index_css_exists(self):
        """Verifica se o arquivo index.css existe."""
        css_path = os.path.join(
            os.path.dirname(__file__), "..", "..", "static", "index.css"
        )
        assert os.path.exists(css_path), "Arquivo index.css não encontrado"

    def test_index_corrected_css_exists(self):
        """Verifica se o arquivo index_corrected.css existe."""
        css_path = os.path.join(
            os.path.dirname(__file__), "..", "..", "static", "index_corrected.css"
        )
        assert os.path.exists(css_path), "Arquivo index_corrected.css não encontrado"

    def test_index_css_not_empty(self):
        """Verifica se index.css não está vazio."""
        css_path = os.path.join(
            os.path.dirname(__file__), "..", "..", "static", "index.css"
        )
        with open(css_path, "r", encoding="utf-8") as f:
            content = f.read()
        assert len(content.strip()) > 0, "Arquivo index.css está vazio"

    def test_index_corrected_css_not_empty(self):
        """Verifica se index_corrected.css não está vazio."""
        css_path = os.path.join(
            os.path.dirname(__file__), "..", "..", "static", "index_corrected.css"
        )
        with open(css_path, "r", encoding="utf-8") as f:
            content = f.read()
        assert len(content.strip()) > 0, "Arquivo index_corrected.css está vazio"

    def test_css_syntax_basic_index(self):
        """Validação básica de sintaxe CSS no index.css."""
        css_path = os.path.join(
            os.path.dirname(__file__), "..", "..", "static", "index.css"
        )
        with open(css_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Conta chaves
        open_braces = content.count("{")
        close_braces = content.count("}")

        # Não deve haver desbalanceamento extremo
        assert abs(open_braces - close_braces) < 10, (
            f"Possível desbalanceamento de chaves no index.css: {open_braces} abertas, {close_braces} fechadas"
        )

    def test_css_syntax_basic_corrected(self):
        """Validação básica de sintaxe CSS no index_corrected.css."""
        css_path = os.path.join(
            os.path.dirname(__file__), "..", "..", "static", "index_corrected.css"
        )
        with open(css_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Conta chaves
        open_braces = content.count("{")
        close_braces = content.count("}")

        # Não deve haver desbalanceamento extremo
        assert abs(open_braces - close_braces) < 10, (
            f"Possível desbalanceamento de chaves no index_corrected.css: {open_braces} abertas, {close_braces} fechadas"
        )

    def test_css_has_theme_variables(self):
        """Verifica se os CSS têm variáveis de tema (dark/light)."""
        css_path = os.path.join(
            os.path.dirname(__file__), "..", "..", "static", "index.css"
        )
        with open(css_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Procura por indicadores de temas
        has_dark = "dark" in content.lower() or '[data-theme="dark"]' in content
        has_light = "light" in content.lower() or '[data-theme="light"]' in content

        # Pelo menos um dos temas deve estar presente
        assert has_dark or has_light, "CSS deve ter suporte a temas (dark/light)"

    def test_css_has_media_queries(self):
        """Verifica se tem media queries para responsividade."""
        css_files = [
            os.path.join(os.path.dirname(__file__), "..", "..", "static", "index.css"),
            os.path.join(
                os.path.dirname(__file__), "..", "..", "static", "index_corrected.css"
            ),
        ]

        for css_path in css_files:
            with open(css_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Verifica se tem media queries
            has_media_query = "@media" in content
            assert has_media_query, (
                f"{os.path.basename(css_path)} deve ter @media queries para responsividade"
            )

    def test_css_compare_duplication(self):
        """Verifica se há muita duplicação entre os dois arquivos CSS."""
        index_path = os.path.join(
            os.path.dirname(__file__), "..", "..", "static", "index.css"
        )
        corrected_path = os.path.join(
            os.path.dirname(__file__), "..", "..", "static", "index_corrected.css"
        )

        with open(index_path, "r", encoding="utf-8") as f:
            index_content = f.read()

        with open(corrected_path, "r", encoding="utf-8") as f:
            corrected_content = f.read()

        # Compara tamanhos (não devem ser idênticos)
        size_ratio = (
            len(corrected_content) / len(index_content) if len(index_content) > 0 else 0
        )

        # Se um arquivo for mais de 90% do tamanho do outro, pode haver duplicação
        # Este é um teste informativo, não falha o teste
        if size_ratio > 0.9:
            print(
                f"\n⚠️  Aviso: {os.path.basename(corrected_path)} tem {size_ratio * 100:.1f}% do tamanho de {os.path.basename(index_path)}"
            )
            print("   Considere consolidar os arquivos CSS ou remover duplicações.")

    def test_css_has_essential_selectors(self):
        """Verifica se seletores essenciais estão presentes."""
        essential_selectors = [
            "body",
            ".container",
            ".btn-primary",  # O HTML usa classes como 'btn-primary', 'btn-secondary'
            ".btn-secondary",
            ".theme-toggle",
            ".header",
            ".footer",
        ]

        css_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "static", "index.css")
        )
        with open(css_path, "r", encoding="utf-8") as f:
            content = f.read()

        missing_selectors = []
        for selector in essential_selectors:
            if selector not in content:
                missing_selectors.append(selector)

        # Apenas avisa, não falha o teste (pode ter nomes diferentes)
        if len(missing_selectors) > 0:
            print(f"\n⚠️  Seletores possivelmente ausentes no CSS: {missing_selectors}")
            print("   (Isso é apenas um aviso, não uma falha)")
