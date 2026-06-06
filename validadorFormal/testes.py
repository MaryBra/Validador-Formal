"""
testes.py - Roda a bateria completa lendo os arquivos testes/*.txt
Formato dos arquivos:
    cadeia<TAB>ACEITA   ou   cadeia<TAB>REJEITA
    Linhas começando com # são comentários e são ignoradas.
    Para a cadeia vazia use a linha:   <vazio><TAB>ACEITA  (ou REJEITA)
"""

import sys
import os

# Garante que src/ está no path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from regular        import run_dfa
from livre_contexto import run_pda
from recursiva      import run_tm

# ---------------------------------------------------------------------------
# Leitura dos arquivos de teste
# ---------------------------------------------------------------------------

def load_test_file(path: str) -> list[tuple[str, bool]]:
    """Lê um arquivo de testes e retorna lista de (cadeia, esperado_bool)."""
    tests = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) != 2:
                print(f"  [AVISO] Linha ignorada (formato inválido): {line!r}")
                continue
            cadeia, resultado = parts
            if cadeia == "<vazio>":
                cadeia = ""
            esperado = resultado.strip().upper() == "ACEITA"
            tests.append((cadeia, esperado))
    return tests

# ---------------------------------------------------------------------------
# Impressão de tabela de resultados
# ---------------------------------------------------------------------------

def print_table(title: str, tests: list, run_fn) -> bool:
    print(f"\n{'='*65}")
    print(f"  {title}")
    print(f"{'='*65}")
    print(f"  {'Cadeia':<25} {'Esperado':<10} {'Obtido':<10} {'Passos':<8} Resultado")
    print(f"  {'-'*60}")
    all_ok = True
    for cadeia, esperado in tests:
        r = run_fn(cadeia)
        ok = r["accepted"] == esperado
        all_ok = all_ok and ok
        exp_s = "ACEITA" if esperado else "REJEITA"
        obt_s = "ACEITA" if r["accepted"] else "REJEITA"
        flag  = "✓" if ok else "✗ FALHOU"
        print(f"  {cadeia:<25} {exp_s:<10} {obt_s:<10} {r['steps']:<8} {flag}")
    print(f"  {'-'*60}")
    print(f"  {'TODOS OK ✓' if all_ok else 'FALHAS DETECTADAS ✗'}")
    return all_ok

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

BASE = os.path.dirname(__file__)

RECONHECEDORES = [
    (
        "LR  - Linguagem Regular (CPF)",
        os.path.join(BASE, "testes", "testes_regular.txt"),
        run_dfa,
    ),
    (
        "LLC - Linguagem Livre de Contexto (Parênteses)",
        os.path.join(BASE, "testes", "testes_livre_contexto.txt"),
        run_pda,
    ),
    (
        "R   - Linguagem Recursiva (w#w)",
        os.path.join(BASE, "testes", "testes_recursiva.txt"),
        run_tm,
    ),
]

def main():
    print("\n" + "="*65)
    print("  VALIDADOR FORMAL - BATERIA COMPLETA DE TESTES")
    print("="*65)

    global_ok = True
    for title, path, run_fn in RECONHECEDORES:
        if not os.path.exists(path):
            print(f"\n[ERRO] Arquivo não encontrado: {path}")
            global_ok = False
            continue
        tests = load_test_file(path)
        ok = print_table(title, tests, run_fn)
        global_ok = global_ok and ok

    print("\n" + "="*65)
    if global_ok:
        print("  RESULTADO FINAL: TODOS OS TESTES PASSARAM ✓")
    else:
        print("  RESULTADO FINAL: EXISTEM FALHAS ✗")
    print("="*65 + "\n")
    return 0 if global_ok else 1

if __name__ == "__main__":
    sys.exit(main())
