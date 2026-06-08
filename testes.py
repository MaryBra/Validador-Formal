"""
testes.py - Roda a bateria completa lendo os arquivos testes/*.txt.

Formato dos arquivos:
    cadeia<TAB>ACEITA
    cadeia<TAB>REJEITA

Linhas com # e sem TAB sao comentarios. A cadeia "#" e aceita como teste
quando aparece no formato:
    #<TAB>ACEITA
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from livre_contexto import executar_automato_com_pilha as executar_livre_contexto
from recursiva import executar_maquina_turing as executar_recursiva
from regular import executar_automato as executar_regular


def carregar_arquivo_testes(caminho: str) -> list[tuple[str, bool]]:
    """Le um arquivo de testes e retorna uma lista de (cadeia, esperado_bool)."""
    testes = []
    with open(caminho, encoding="utf-8") as arquivo:
        for linha in arquivo:
            linha = linha.rstrip("\n")
            # Linhas de comentario podem comecar com #, mas a cadeia "#" tambem e teste.
            if not linha or (linha.startswith("#") and "\t" not in linha):
                continue

            partes = linha.split("\t")
            if len(partes) != 2:
                print(f"  [AVISO] Linha ignorada (formato invalido): {linha!r}")
                continue

            cadeia, resultado = partes
            if cadeia == "<vazio>":
                cadeia = ""

            # O relatorio compara esperado, obtido e quantidade de passos.
            esperado = resultado.strip().upper() == "ACEITA"
            testes.append((cadeia, esperado))

    return testes


def imprimir_tabela(titulo: str, testes: list[tuple[str, bool]], funcao_executar) -> bool:
    print(f"\n{'=' * 65}")
    print(f"  {titulo}")
    print(f"{'=' * 65}")
    print(f"  {'Cadeia':<25} {'Esperado':<10} {'Obtido':<10} {'Passos':<8} Resultado")
    print(f"  {'-' * 60}")

    todos_ok = True
    for cadeia, esperado in testes:
        # Cada reconhecedor devolve o mesmo formato de resultado.
        resultado = funcao_executar(cadeia)
        ok = resultado["aceita"] == esperado
        todos_ok = todos_ok and ok

        esperado_txt = "ACEITA" if esperado else "REJEITA"
        obtido_txt = "ACEITA" if resultado["aceita"] else "REJEITA"
        status = "OK" if ok else "FALHOU"
        print(f"  {cadeia:<25} {esperado_txt:<10} {obtido_txt:<10} {resultado['passos']:<8} {status}")

    print(f"  {'-' * 60}")
    print(f"  {'TODOS OK' if todos_ok else 'FALHAS DETECTADAS'}")
    return todos_ok


PASTA_BASE = os.path.dirname(__file__)

RECONHECEDORES = [
    (
        "LR  - Linguagem Regular (CPF)",
        os.path.join(PASTA_BASE, "testes", "testes_regular.txt"),
        executar_regular,
    ),
    (
        "LLC - Linguagem Livre de Contexto (Delimitadores)",
        os.path.join(PASTA_BASE, "testes", "testes_livre_contexto.txt"),
        executar_livre_contexto,
    ),
    (
        "R   - Linguagem Recursiva (w#w)",
        os.path.join(PASTA_BASE, "testes", "testes_recursiva.txt"),
        executar_recursiva,
    ),
]


def principal() -> int:
    print("\n" + "=" * 65)
    print("  VALIDADOR FORMAL - BATERIA COMPLETA DE TESTES")
    print("=" * 65)

    resultado_geral = True
    for titulo, caminho, funcao_executar in RECONHECEDORES:
        if not os.path.exists(caminho):
            print(f"\n[ERRO] Arquivo nao encontrado: {caminho}")
            resultado_geral = False
            continue

        testes = carregar_arquivo_testes(caminho)
        resultado = imprimir_tabela(titulo, testes, funcao_executar)
        resultado_geral = resultado_geral and resultado

    print("\n" + "=" * 65)
    if resultado_geral:
        print("  RESULTADO FINAL: TODOS OS TESTES PASSARAM")
    else:
        print("  RESULTADO FINAL: EXISTEM FALHAS")
    print("=" * 65 + "\n")
    return 0 if resultado_geral else 1


if __name__ == "__main__":
    sys.exit(principal())
