"""
Reconhecedor de Linguagem Regular (LR) - Validacao de CPF.
Modelo: automato finito deterministico.
Linguagem: L = { d1d2d3.d4d5d6.d7d8d9-d10d11 | di em {0,...,9} }.
"""

import sys

DIGITOS = set("0123456789")

# Estes estados sao os mesmos usados na tabela do relatorio.
ESTADO_ERRO = "q_err"
ESTADOS = {f"q{i}" for i in range(15)} | {ESTADO_ERRO}
ALFABETO = DIGITOS | {".", "-"}
ESTADO_INICIAL = "q0"
ESTADOS_FINAIS = {"q14"}


def construir_transicoes() -> dict:
    transicoes = {}

    # No relatorio, D representa qualquer digito. Aqui ficam os saltos com D.
    arcos_com_digitos = [
        ("q0", "q1"),
        ("q1", "q2"),
        ("q2", "q3"),
        ("q4", "q5"),
        ("q5", "q6"),
        ("q6", "q7"),
        ("q8", "q9"),
        ("q9", "q10"),
        ("q10", "q11"),
        ("q12", "q13"),
        ("q13", "q14"),
    ]

    for origem, destino in arcos_com_digitos:
        for digito in DIGITOS:
            transicoes[(origem, digito)] = destino

    # Os pontos e o hifen aparecem em posicoes fixas do formato do CPF.
    transicoes[("q3", ".")] = "q4"
    transicoes[("q7", ".")] = "q8"
    transicoes[("q11", "-")] = "q12"

    # Qualquer simbolo fora do esperado cai no estado de erro.
    for estado in ESTADOS:
        for simbolo in ALFABETO:
            transicoes.setdefault((estado, simbolo), ESTADO_ERRO)

    return transicoes


TRANSICOES = construir_transicoes()


def executar_automato(cadeia: str, detalhado: bool = False) -> dict:
    estado_atual = ESTADO_INICIAL
    passos = 0
    historico = [(estado_atual, None, None)]

    # Cada simbolo lido conta como um passo, como definido no relatorio.
    for simbolo in cadeia:
        proximo_estado = TRANSICOES.get((estado_atual, simbolo), ESTADO_ERRO)
        passos += 1
        historico.append((estado_atual, simbolo, proximo_estado))
        estado_atual = proximo_estado

        if detalhado:
            print(f"  Passo {passos:>2}: ({historico[-1][0]!r:>6}, {simbolo!r}) -> {estado_atual!r}")

    aceita = estado_atual in ESTADOS_FINAIS
    return {
        "aceita": aceita,
        "passos": passos,
        "historico": historico,
        "estado_final": estado_atual,
    }


def explicar(cadeia: str):
    print(f"\n=== Automato finito - CPF - Cadeia: {cadeia!r} ===")
    resultado = executar_automato(cadeia, detalhado=True)
    veredito = "ACEITA" if resultado["aceita"] else "REJEITA"
    print(f"Estado final: {resultado['estado_final']!r}  ->  {veredito}")
    print(f"Total de passos: {resultado['passos']}")
    return resultado


TESTES_PADRAO = [
    ("123.456.789-00", True),
    ("000.000.000-00", True),
    ("987.654.321-99", True),
    ("12345678900", False),
    ("12.345.678-90", False),
    ("123.456.789.00", False),
]


def executar_testes(testes=None):
    testes = testes or TESTES_PADRAO
    print("\n" + "=" * 60)
    print("BATERIA DE TESTES - Linguagem Regular (CPF)")
    print(f"{'Cadeia':<25} {'Esperado':<10} {'Obtido':<10} {'Passos':<8} {'OK?'}")
    print("-" * 70)

    todos_ok = True
    for cadeia, esperado in testes:
        resultado = executar_automato(cadeia)
        ok = resultado["aceita"] == esperado
        todos_ok = todos_ok and ok
        esperado_txt = "ACEITA" if esperado else "REJEITA"
        obtido_txt = "ACEITA" if resultado["aceita"] else "REJEITA"
        status = "OK" if ok else "FALHOU"
        print(f"{cadeia:<25} {esperado_txt:<10} {obtido_txt:<10} {resultado['passos']:<8} {status}")

    print("-" * 70)
    print(f"Resultado geral: {'TODOS OK' if todos_ok else 'FALHAS DETECTADAS'}\n")
    return todos_ok


if __name__ == "__main__":
    if len(sys.argv) > 1:
        explicar(sys.argv[1])
    else:
        explicar("123.456.789-00")
        explicar("12.34.56-78")
        print()
        executar_testes()
