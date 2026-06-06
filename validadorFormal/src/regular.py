"""
Reconhecedor de Linguagem Regular (LR) - Validação de CPF
Modelo: DFA (Autômato Finito Determinístico)
Linguagem: L = { d1d2d3.d4d5d6.d7d8d9-d10d11 | di ∈ {0,...,9} }
"""

import sys

DIGITS = set("0123456789")

# Estados: q0..q14, q_err
# q0  -> início
# q1..q3  -> primeiros 3 dígitos
# q4  -> primeiro ponto
# q5..q7  -> próximos 3 dígitos
# q8  -> segundo ponto
# q9..q11 -> próximos 3 dígitos
# q12 -> hífen
# q13..q14 -> últimos 2 dígitos
# q_err -> estado de erro (morto)

STATES       = {f"q{i}" for i in range(15)} | {"q_err"}
SIGMA        = DIGITS | {".", "-"}
INITIAL      = "q0"
FINAL_STATES = {"q14"}

def _build_transitions():
    delta = {}

    # Arcos para dígitos nos grupos
    # grupo 1: q0 -> q1 -> q2 -> q3
    for src, dst in [("q0","q1"), ("q1","q2"), ("q2","q3"),
                     ("q4","q5"), ("q5","q6"), ("q6","q7"),
                     ("q8","q9"), ("q9","q10"), ("q10","q11"),
                     ("q12","q13"), ("q13","q14")]:
        for d in DIGITS:
            delta[(src, d)] = dst

    # Separadores
    delta[("q3",  ".")] = "q4"
    delta[("q7",  ".")] = "q8"
    delta[("q11", "-")] = "q12"

    # Tudo que não está definido vai para q_err
    for state in STATES:
        for sym in SIGMA:
            if (state, sym) not in delta:
                delta[(state, sym)] = "q_err"

    return delta

DELTA = _build_transitions()

# ---------------------------------------------------------------------------
# Simulador do DFA
# ---------------------------------------------------------------------------

def run_dfa(input_str: str, verbose: bool = False) -> dict:
    """
    Executa o DFA sobre input_str.
    Retorna dict com: accepted, steps, trace.
    """
    state   = INITIAL
    steps   = 0
    trace   = [(state, None, None)]   # (estado, símbolo lido, próx estado)

    for symbol in input_str:
        if symbol not in SIGMA:
            # Símbolo fora do alfabeto -> rejeita imediatamente
            next_state = "q_err"
        else:
            next_state = DELTA.get((state, symbol), "q_err")

        steps += 1   # uma leitura de símbolo com mudança de estado = 1 passo
        trace.append((state, symbol, next_state))
        state = next_state

        if verbose:
            print(f"  Passo {steps:>2}: ({trace[-1][0]!r:>6}, {symbol!r}) -> {state!r}")

    accepted = state in FINAL_STATES
    return {"accepted": accepted, "steps": steps, "trace": trace, "final_state": state}

# ---------------------------------------------------------------------------
# Execução passo a passo legível
# ---------------------------------------------------------------------------

def explain(input_str: str):
    print(f"\n=== DFA - CPF - Cadeia: {input_str!r} ===")
    result = run_dfa(input_str, verbose=True)
    verdict = "ACEITA ✓" if result["accepted"] else "REJEITA ✗"
    print(f"Estado final: {result['final_state']!r}  ->  {verdict}")
    print(f"Total de passos: {result['steps']}")
    return result

# ---------------------------------------------------------------------------
# Bateria de testes padrão
# ---------------------------------------------------------------------------

DEFAULT_TESTS = [
    # (cadeia, esperado)
    ("123.456.789-00", True),
    ("000.000.000-00", True),
    ("987.654.321-99", True),
    # rejeições
    ("12345678900",    False),
    ("12.345.678-90",  False),
    ("123.456.789.00", False),
]

def run_tests(tests=None):
    tests = tests or DEFAULT_TESTS
    print("\n{'='*60}")
    print("BATERIA DE TESTES - Linguagem Regular (CPF)")
    print(f"{'Cadeia':<25} {'Esperado':<10} {'Obtido':<10} {'Passos':<8} {'OK?'}")
    print("-" * 70)
    all_ok = True
    for cadeia, esperado in tests:
        r = run_dfa(cadeia)
        ok = r["accepted"] == esperado
        all_ok = all_ok and ok
        exp_s = "ACEITA" if esperado else "REJEITA"
        obt_s = "ACEITA" if r["accepted"] else "REJEITA"
        flag  = "✓" if ok else "✗ FALHOU"
        print(f"{cadeia:<25} {exp_s:<10} {obt_s:<10} {r['steps']:<8} {flag}")
    print("-" * 70)
    print(f"Resultado geral: {'TODOS OK ✓' if all_ok else 'FALHAS DETECTADAS ✗'}\n")
    return all_ok

# ---------------------------------------------------------------------------
# Ponto de entrada
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cadeia = sys.argv[1]
        explain(cadeia)
    else:
        # Mostra execução passo a passo de uma aceita e uma rejeitada
        explain("123.456.789-00")
        explain("12.34.56-78")
        print()
        run_tests()
