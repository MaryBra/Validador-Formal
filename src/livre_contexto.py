"""
Reconhecedor de Linguagem Livre de Contexto (LLC).
Modelo: automato com pilha.
Linguagem: L = { w em Sigma* | os delimitadores (), [] e {} em w estao balanceados }.
"""

import sys

ESTADO_ERRO = "q_err"
ESTADOS = {"q0", "qf", ESTADO_ERRO}
ESTADO_INICIAL = "q0"
ESTADOS_FINAIS = {"qf"}

# A pilha comeca com Z, igual ao simbolo de fundo descrito no relatorio.
FUNDO_PILHA = "Z"
ABERTURA_FECHAMENTO = {"(": ")", "[": "]", "{": "}"}
FECHAMENTO_ABERTURA = {fechamento: abertura for abertura, fechamento in ABERTURA_FECHAMENTO.items()}

# Mesmo alfabeto do relatorio: delimitadores, letras, digitos e operadores basicos.
ALFABETO = set("()[]{}" + "abcdefghijklmnopqrstuvwxyz" + "ABCDEFGHIJKLMNOPQRSTUVWXYZ" + "+-*/0123456789")
ALFABETO_PILHA = {FUNDO_PILHA, "(", "[", "{"}
SIMBOLOS_COMUNS = ALFABETO - set(ABERTURA_FECHAMENTO) - set(FECHAMENTO_ABERTURA)
VAZIO = None

ACAO_EMPILHA = "empilha"
ACAO_DESEMPILHA = "desempilha"
ACAO_MANTEM = "mantem"


def construir_transicoes() -> dict:
    """
    Constroi a tabela de transicao do automato com pilha.

    Formato:
        transicoes[(estado, simbolo_entrada, topo_pilha)] = (proximo_estado, acao_pilha)
    """
    transicoes = {}

    # Aberturas empilham; simbolos comuns apenas passam pela entrada.
    for topo in ALFABETO_PILHA:
        for abertura in ABERTURA_FECHAMENTO:
            transicoes[("q0", abertura, topo)] = ("q0", (ACAO_EMPILHA, abertura))

        for simbolo_comum in SIMBOLOS_COMUNS:
            transicoes[("q0", simbolo_comum, topo)] = ("q0", (ACAO_MANTEM,))

    # Fechamentos so sao aceitos quando combinam com o topo da pilha.
    for fechamento, abertura_esperada in FECHAMENTO_ABERTURA.items():
        transicoes[("q0", fechamento, abertura_esperada)] = ("q0", (ACAO_DESEMPILHA,))
        for topo in ALFABETO_PILHA - {abertura_esperada}:
            transicoes[("q0", fechamento, topo)] = (ESTADO_ERRO, (ACAO_MANTEM,))

    # No fim da leitura, a cadeia aceita precisa deixar apenas o Z na pilha.
    transicoes[("q0", VAZIO, FUNDO_PILHA)] = ("qf", (ACAO_MANTEM,))
    for topo in ALFABETO_PILHA - {FUNDO_PILHA}:
        transicoes[("q0", VAZIO, topo)] = (ESTADO_ERRO, (ACAO_MANTEM,))

    for topo in ALFABETO_PILHA:
        for simbolo in ALFABETO | {VAZIO}:
            transicoes[(ESTADO_ERRO, simbolo, topo)] = (ESTADO_ERRO, (ACAO_MANTEM,))

    return transicoes


TRANSICOES = construir_transicoes()


def aplicar_acao_pilha(pilha: list[str], acao: tuple) -> None:
    if acao[0] == ACAO_EMPILHA:
        pilha.append(acao[1])
    elif acao[0] == ACAO_DESEMPILHA and pilha:
        pilha.pop()


def descrever_acao(acao: tuple) -> str:
    if acao[0] == ACAO_EMPILHA:
        return f"empilha {acao[1]}"
    if acao[0] == ACAO_DESEMPILHA:
        return "desempilha"
    return "mantem pilha"


def executar_automato_com_pilha(cadeia: str, detalhado: bool = False) -> dict:
    estado_atual = ESTADO_INICIAL
    pilha = [FUNDO_PILHA]
    passos = 0
    historico = []

    # Cada transicao, inclusive empilhar e desempilhar, entra na contagem de passos.
    for simbolo in cadeia:
        estado_anterior = estado_atual
        pilha_anterior = list(pilha)
        topo = pilha[-1] if pilha else FUNDO_PILHA

        if simbolo not in ALFABETO:
            proximo_estado, acao = (ESTADO_ERRO, (ACAO_MANTEM,))
            rotulo_acao = "simbolo invalido"
        else:
            proximo_estado, acao = TRANSICOES.get(
                (estado_atual, simbolo, topo),
                (ESTADO_ERRO, (ACAO_MANTEM,)),
            )
            rotulo_acao = descrever_acao(acao)

        passos += 1
        aplicar_acao_pilha(pilha, acao)
        historico.append((estado_anterior, simbolo, pilha_anterior, proximo_estado, rotulo_acao, list(pilha)))
        estado_atual = proximo_estado

        if detalhado:
            print(
                f"  Passo {passos:>2}: ({estado_anterior!r}, {simbolo!r}, pilha={pilha_anterior}) "
                f"-> {proximo_estado!r}, {rotulo_acao}, pilha={pilha}"
            )

        if estado_atual == ESTADO_ERRO:
            break

    if estado_atual != ESTADO_ERRO:
        # Esta transicao vazia e a verificacao final mostrada no relatorio.
        estado_anterior = estado_atual
        pilha_anterior = list(pilha)
        topo = pilha[-1] if pilha else FUNDO_PILHA
        proximo_estado, acao = TRANSICOES.get(
            (estado_atual, VAZIO, topo),
            (ESTADO_ERRO, (ACAO_MANTEM,)),
        )
        passos += 1
        aplicar_acao_pilha(pilha, acao)
        rotulo_acao = "transicao vazia"
        historico.append((estado_anterior, "EPS", pilha_anterior, proximo_estado, rotulo_acao, list(pilha)))
        estado_atual = proximo_estado

        if detalhado:
            print(
                f"  Passo {passos:>2}: ({estado_anterior!r}, EPS, pilha={pilha_anterior}) "
                f"-> {proximo_estado!r}, {rotulo_acao}, pilha={pilha}"
            )

    aceita = estado_atual in ESTADOS_FINAIS
    return {
        "aceita": aceita,
        "passos": passos,
        "historico": historico,
        "estado_final": estado_atual,
    }


def explicar(cadeia: str):
    print(f"\n=== Automato com pilha - Delimitadores balanceados - Cadeia: {cadeia!r} ===")
    resultado = executar_automato_com_pilha(cadeia, detalhado=True)
    veredito = "ACEITA" if resultado["aceita"] else "REJEITA"
    print(f"Estado final: {resultado['estado_final']!r}  ->  {veredito}")
    print(f"Total de passos: {resultado['passos']}")
    return resultado


TESTES_PADRAO = [
    ("(a+b)", True),
    ("((x+y)*z)", True),
    ("{[(x+y)]}", True),
    ("((a+b)", False),
    ("[a+b))", False),
    ("{(a+b]}", False),
]


def executar_testes(testes=None):
    testes = testes or TESTES_PADRAO
    print("\n=== BATERIA DE TESTES - LLC (Delimitadores balanceados) ===")
    print(f"{'Cadeia':<25} {'Esperado':<10} {'Obtido':<10} {'Passos':<8} {'OK?'}")
    print("-" * 70)
    todos_ok = True

    for cadeia, esperado in testes:
        resultado = executar_automato_com_pilha(cadeia)
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
        explicar("((x+y)*z)")
        explicar("((a+b)")
        print()
        executar_testes()
