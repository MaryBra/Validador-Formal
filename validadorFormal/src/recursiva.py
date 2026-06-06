"""
Reconhecedor de Linguagem Recursiva (R)
Modelo: Máquina de Turing (MT)
Linguagem: L = { w#w | w ∈ {0,1}* }

Estratégia:
  1. Ler o primeiro símbolo não-marcado de w1 (antes de #), marcá-lo com X.
  2. Atravessar a fita até após o # para encontrar o símbolo correspondente em w2.
  3. Verificar igualdade e marcá-lo com X.
  4. Voltar ao início e repetir.
  5. Ao fim, verificar se todos os símbolos de ambos os lados foram marcados.
"""

import sys

# ---------------------------------------------------------------------------
# Símbolos
# ---------------------------------------------------------------------------

BLANK   = "_"    # símbolo branco (□)
MARKED  = "X"    # símbolo marcado

SIGMA   = {"0", "1", "#"}                        # alfabeto de entrada
GAMMA   = {"0", "1", "#", MARKED, BLANK}          # alfabeto da fita

# ---------------------------------------------------------------------------
# Estados
# ---------------------------------------------------------------------------
# q0  -> lê próximo símbolo não-marcado em w1
# q1  -> lembrou '0', cruzando para w2
# q2  -> lembrou '1', cruzando para w2
# q3  -> busca '0' em w2 (após cruzar #)
# q4  -> busca '1' em w2 (após cruzar #)
# q5  -> volta para a esquerda após marcar em w2
# q6  -> verificação final: todos marcados?
# qa  -> aceita
# qr  -> rejeita

STATES       = {"q0","q1","q2","q3","q4","q5","q6","qa","qr"}
INITIAL      = "q0"
FINAL_STATES = {"qa"}

# ---------------------------------------------------------------------------
# Tabela de transição completa
# delta[estado][símbolo] = (escreve, move, próx_estado)
# move: 'R' = direita, 'L' = esquerda
# ---------------------------------------------------------------------------

DELTA = {
    # --- q0: procura próximo não-marcado antes do '#' ---
    "q0": {
        "0": ("X", "R", "q1"),   # marcou 0, vai buscar 0 em w2
        "1": ("X", "R", "q2"),   # marcou 1, vai buscar 1 em w2
        "X": ("X", "R", "q0"),   # pula marcado
        "#": ("#", "R", "q6"),   # chegou no #, vai verificar se w2 acabou
        BLANK: (BLANK, "R", "qr"),
    },
    # --- q1: lembrou '0', atravessa até após '#' ---
    "q1": {
        "0": ("0", "R", "q1"),
        "1": ("1", "R", "q1"),
        "X": ("X", "R", "q1"),
        "#": ("#", "R", "q3"),   # passou o '#', agora busca '0' em w2
        BLANK: (BLANK, "R", "qr"),
    },
    # --- q2: lembrou '1', atravessa até após '#' ---
    "q2": {
        "0": ("0", "R", "q2"),
        "1": ("1", "R", "q2"),
        "X": ("X", "R", "q2"),
        "#": ("#", "R", "q4"),   # passou o '#', agora busca '1' em w2
        BLANK: (BLANK, "R", "qr"),
    },
    # --- q3: busca '0' em w2 ---
    "q3": {
        "X": ("X", "R", "q3"),   # pula já-marcados
        "0": ("X", "L", "q5"),   # achou o 0, marca e volta
        "1": ("1", "R", "qr"),   # incompatível -> rejeita
        BLANK: (BLANK, "R", "qr"),
        "#": ("#", "R", "qr"),
    },
    # --- q4: busca '1' em w2 ---
    "q4": {
        "X": ("X", "R", "q4"),   # pula já-marcados
        "1": ("X", "L", "q5"),   # achou o 1, marca e volta
        "0": ("0", "R", "qr"),   # incompatível -> rejeita
        BLANK: (BLANK, "R", "qr"),
        "#": ("#", "R", "qr"),
    },
    # --- q5: volta para o início (esquerda) ---
    "q5": {
        "0": ("0", "L", "q5"),
        "1": ("1", "L", "q5"),
        "X": ("X", "L", "q5"),
        "#": ("#", "L", "q5"),
        BLANK: (BLANK, "R", "q0"),  # chegou ao início da fita -> recomeça
    },
    # --- q6: verifica se w2 está todo marcado (cadeia vazia ou igual) ---
    "q6": {
        "X": ("X", "R", "q6"),
        BLANK: (BLANK, "R", "qa"),  # w2 todo marcado -> aceita
        "0": ("0", "R", "qr"),      # w2 ainda tem símbolos -> rejeita
        "1": ("1", "R", "qr"),
    },
    # --- estados finais (sem transições necessárias) ---
    "qa": {},
    "qr": {},
}

# ---------------------------------------------------------------------------
# Simulador da Máquina de Turing
# ---------------------------------------------------------------------------

def run_tm(input_str: str, verbose: bool = False, max_steps: int = 100_000) -> dict:
    """
    Executa a MT sobre input_str.
    Retorna dict com: accepted, steps, trace.
    """
    # Fita como lista; posição 0 = célula mais à esquerda
    tape    = list(input_str) if input_str else [BLANK]
    head    = 0
    state   = INITIAL
    steps   = 0
    trace   = []

    while state not in {"qa", "qr"} and steps < max_steps:
        # Estende a fita com branco se necessário
        while head >= len(tape):
            tape.append(BLANK)
        if head < 0:
            tape.insert(0, BLANK)
            head = 0

        symbol = tape[head]
        trans  = DELTA.get(state, {}).get(symbol)

        if trans is None:
            # Transição não definida -> rejeita
            state = "qr"
            break

        write, move, next_state = trans
        steps += 1   # 1 passo = leitura + escrita + movimento

        if verbose:
            tape_str = "".join(tape)
            pointer  = " " * head + "^"
            print(f"  Passo {steps:>4}: estado={state!r}, lê={symbol!r}, "
                  f"escreve={write!r}, move={move}, -> {next_state!r}")
            print(f"           Fita: {tape_str}")
            print(f"                 {pointer}")

        trace.append({
            "step": steps, "state": state, "read": symbol,
            "write": write, "move": move, "next": next_state,
            "head": head, "tape": "".join(tape),
        })

        tape[head] = write
        head = head + 1 if move == "R" else head - 1
        state = next_state

    accepted = state in FINAL_STATES
    return {"accepted": accepted, "steps": steps, "trace": trace, "final_state": state}

# ---------------------------------------------------------------------------
# Execução passo a passo legível
# ---------------------------------------------------------------------------

def explain(input_str: str):
    label = repr(input_str) if input_str else "'#' (cadeia vazia)"
    print(f"\n=== MT - w#w - Cadeia: {input_str!r} ===")
    result = run_tm(input_str, verbose=True)
    verdict = "ACEITA ✓" if result["accepted"] else "REJEITA ✗"
    print(f"Estado final: {result['final_state']!r}  ->  {verdict}")
    print(f"Total de passos: {result['steps']}")
    return result

# ---------------------------------------------------------------------------
# Bateria de testes padrão
# ---------------------------------------------------------------------------

DEFAULT_TESTS = [
    ("#",        True),    # w = ε  ->  #  (aceita, ambos os lados vazios)
    ("0#0",      True),
    ("101#101",  True),
    # rejeições
    ("0#1",      False),
    ("101#100",  False),
    ("01#011",   False),
]

def run_tests(tests=None):
    tests = tests or DEFAULT_TESTS
    print("\n=== BATERIA DE TESTES - Linguagem Recursiva (w#w) ===")
    print(f"{'Cadeia':<20} {'Esperado':<10} {'Obtido':<10} {'Passos':<8} {'OK?'}")
    print("-" * 60)
    all_ok = True
    for cadeia, esperado in tests:
        r = run_tm(cadeia)
        ok = r["accepted"] == esperado
        all_ok = all_ok and ok
        exp_s = "ACEITA" if esperado else "REJEITA"
        obt_s = "ACEITA" if r["accepted"] else "REJEITA"
        flag  = "✓" if ok else "✗ FALHOU"
        print(f"{cadeia:<20} {exp_s:<10} {obt_s:<10} {r['steps']:<8} {flag}")
    print("-" * 60)
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
        explain("101#101")
        explain("101#100")
        print()
        run_tests()
