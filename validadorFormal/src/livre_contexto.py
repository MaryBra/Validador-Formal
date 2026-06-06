"""
Reconhecedor de Linguagem Livre de Contexto (LLC)
Modelo: PDA (Autômato com Pilha)
Linguagem: L = { w ∈ Σ* | os delimitadores (), [] e {} em w estão balanceados }
"""

import sys

# ---------------------------------------------------------------------------
# Definição explícita do PDA como dados
# ---------------------------------------------------------------------------

STATES       = {"q0", "qf", "q_err"}
INITIAL      = "q0"
FINAL_STATES = {"qf"}
STACK_BOTTOM = "Z"          # marcador de fundo da pilha

# Símbolos de abertura e seus respectivos fechamentos
OPEN_CLOSE = {"(": ")", "[": "]", "{": "}"}
CLOSE_OPEN = {v: k for k, v in OPEN_CLOSE.items()}

# Alfabeto de entrada aceito (delimitadores + letras + operadores comuns)
SIGMA = set("()[]{}" + "abcdefghijklmnopqrstuvwxyz" + "+-*/= ,;0123456789")

# ---------------------------------------------------------------------------
# Transições do PDA descritas como dados
# A função de transição é:
#   delta(estado, símbolo, topo_pilha) = (próx_estado, ação_pilha)
# ação_pilha:
#   ("push", sym)  -> empilha sym
#   ("pop",)       -> desempilha
#   ("noop",)      -> não mexe na pilha
#   ("accept",)    -> aceita (pilha vazia + fim)
# ---------------------------------------------------------------------------

def _transition(state: str, symbol: str | None, stack: list) -> tuple:
    """
    Retorna (next_state, stack_action) ou lança exceção em erro.
    symbol=None indica fim da entrada (ε-transição de aceitação).
    """
    top = stack[-1] if stack else None

    if state == "q0":
        if symbol is None:
            # Fim da entrada: aceita apenas se pilha está vazia (só Z)
            if top == STACK_BOTTOM:
                return ("qf", ("pop",))
            else:
                return ("q_err", ("noop",))

        if symbol in OPEN_CLOSE:
            return ("q0", ("push", symbol))

        if symbol in CLOSE_OPEN:
            esperado = CLOSE_OPEN[symbol]   # abre que corresponde
            if top == esperado:
                return ("q0", ("pop",))
            else:
                return ("q_err", ("noop",))

        # Qualquer outro símbolo do alfabeto -> ignora (não afeta pilha)
        if symbol in SIGMA:
            return ("q0", ("noop",))

    # Caso não coberto
    return ("q_err", ("noop",))

# ---------------------------------------------------------------------------
# Simulador do PDA
# ---------------------------------------------------------------------------

def run_pda(input_str: str, verbose: bool = False) -> dict:
    """
    Executa o PDA sobre input_str.
    Retorna dict com: accepted, steps, trace.
    """
    state  = INITIAL
    stack  = [STACK_BOTTOM]
    steps  = 0
    trace  = []

    for symbol in input_str:
        if symbol not in SIGMA:
            state = "q_err"
            steps += 1
            trace.append((state, symbol, list(stack), "q_err", "símbolo inválido"))
            break

        old_state = state
        old_stack = list(stack)
        next_state, action = _transition(state, symbol, stack)
        steps += 1   # cada transição = 1 passo

        # Aplica ação na pilha
        if action[0] == "push":
            stack.append(action[1])
            steps += 1   # empilhamento conta como passo adicional
            action_str = f"push({action[1]})"
        elif action[0] == "pop":
            stack.pop()
            steps += 1   # desempilhamento conta como passo adicional
            action_str = f"pop()"
        else:
            action_str = "noop"

        trace.append((old_state, symbol, old_stack, next_state, action_str))
        state = next_state

        if verbose:
            print(f"  Passo {steps:>2}: ({old_state!r}, {symbol!r}, pilha={old_stack}) "
                  f"-> {next_state!r}, {action_str}, pilha={stack}")

        if state == "q_err":
            break

    # ε-transição ao fim da entrada
    if state != "q_err":
        old_state = state
        old_stack = list(stack)
        next_state, action = _transition(state, None, stack)
        steps += 1

        if action[0] == "pop":
            stack.pop()
            steps += 1
            action_str = "pop() [ε fim]"
        else:
            action_str = "noop [ε fim]"

        trace.append((old_state, "ε", old_stack, next_state, action_str))
        state = next_state

        if verbose:
            print(f"  Passo {steps:>2}: ({old_state!r}, ε, pilha={old_stack}) "
                  f"-> {next_state!r}, {action_str}, pilha={stack}")

    accepted = state in FINAL_STATES
    return {"accepted": accepted, "steps": steps, "trace": trace, "final_state": state}

# ---------------------------------------------------------------------------
# Execução passo a passo legível
# ---------------------------------------------------------------------------

def explain(input_str: str):
    print(f"\n=== PDA - Parênteses Balanceados - Cadeia: {input_str!r} ===")
    result = run_pda(input_str, verbose=True)
    verdict = "ACEITA ✓" if result["accepted"] else "REJEITA ✗"
    print(f"Estado final: {result['final_state']!r}  ->  {verdict}")
    print(f"Total de passos: {result['steps']}")
    return result

# ---------------------------------------------------------------------------
# Bateria de testes padrão
# ---------------------------------------------------------------------------

DEFAULT_TESTS = [
    ("(a+b)",          True),
    ("((x+y)*z)",      True),
    ("{[(x+y)]}",      True),
    # rejeições
    ("((a+b)",         False),
    ("[a+b))",         False),
    ("{(a+b]}",        False),
]

def run_tests(tests=None):
    tests = tests or DEFAULT_TESTS
    print("\n=== BATERIA DE TESTES - LLC (Parênteses Balanceados) ===")
    print(f"{'Cadeia':<25} {'Esperado':<10} {'Obtido':<10} {'Passos':<8} {'OK?'}")
    print("-" * 70)
    all_ok = True
    for cadeia, esperado in tests:
        r = run_pda(cadeia)
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
        explain("((x+y)*z)")
        explain("((a+b)")
        print()
        run_tests()
