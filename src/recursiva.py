"""Reconhecedor R para L = { w#w | w em {0,1}* }, usando maquina de Turing."""

import sys

# O relatorio usa X para posicoes ja comparadas e branco para o fim da fita.
BRANCO = "_"
MARCADO = "X"
DIREITA = "R"
ESQUERDA = "L"

ALFABETO_ENTRADA = {"0", "1", "#"}
ALFABETO_FITA = {"0", "1", "#", MARCADO, BRANCO}

ESTADO_ACEITACAO = "qa"
ESTADO_REJEICAO = "qr"
ESTADOS = {"q0", "q1", "q2", "q3", "q4", "q5", "q6", ESTADO_ACEITACAO, ESTADO_REJEICAO}
ESTADO_INICIAL = "q0"
ESTADOS_FINAIS = {ESTADO_ACEITACAO}

# Tabela de transicoes da maquina de Turing apresentada no relatorio.
# transicoes[estado][simbolo] = (escreve, move, proximo_estado)
TRANSICOES = {
    # q0 procura o proximo simbolo ainda nao marcado do lado esquerdo.
    "q0": {
        "0": (MARCADO, DIREITA, "q1"),
        "1": (MARCADO, DIREITA, "q2"),
        MARCADO: (MARCADO, DIREITA, "q0"),
        "#": ("#", DIREITA, "q6"),
        BRANCO: (BRANCO, DIREITA, ESTADO_REJEICAO),
    },
    # q1 foi escolhido depois de marcar um 0 na primeira parte.
    "q1": {
        "0": ("0", DIREITA, "q1"),
        "1": ("1", DIREITA, "q1"),
        MARCADO: (MARCADO, DIREITA, "q1"),
        "#": ("#", DIREITA, "q3"),
        BRANCO: (BRANCO, DIREITA, ESTADO_REJEICAO),
    },
    # q2 foi escolhido depois de marcar um 1 na primeira parte.
    "q2": {
        "0": ("0", DIREITA, "q2"),
        "1": ("1", DIREITA, "q2"),
        MARCADO: (MARCADO, DIREITA, "q2"),
        "#": ("#", DIREITA, "q4"),
        BRANCO: (BRANCO, DIREITA, ESTADO_REJEICAO),
    },
    # q3 procura o 0 correspondente no lado direito.
    "q3": {
        MARCADO: (MARCADO, DIREITA, "q3"),
        "0": (MARCADO, ESQUERDA, "q5"),
        "1": ("1", DIREITA, ESTADO_REJEICAO),
        "#": ("#", DIREITA, ESTADO_REJEICAO),
        BRANCO: (BRANCO, DIREITA, ESTADO_REJEICAO),
    },
    # q4 procura o 1 correspondente no lado direito.
    "q4": {
        MARCADO: (MARCADO, DIREITA, "q4"),
        "1": (MARCADO, ESQUERDA, "q5"),
        "0": ("0", DIREITA, ESTADO_REJEICAO),
        "#": ("#", DIREITA, ESTADO_REJEICAO),
        BRANCO: (BRANCO, DIREITA, ESTADO_REJEICAO),
    },
    # q5 volta ate o inicio para comparar o proximo simbolo.
    "q5": {
        "0": ("0", ESQUERDA, "q5"),
        "1": ("1", ESQUERDA, "q5"),
        MARCADO: (MARCADO, ESQUERDA, "q5"),
        "#": ("#", ESQUERDA, "q5"),
        BRANCO: (BRANCO, DIREITA, "q0"),
    },
    # q6 verifica se nao sobrou nada sem marcar no lado direito.
    "q6": {
        MARCADO: (MARCADO, DIREITA, "q6"),
        BRANCO: (BRANCO, DIREITA, ESTADO_ACEITACAO),
        "0": ("0", DIREITA, ESTADO_REJEICAO),
        "1": ("1", DIREITA, ESTADO_REJEICAO),
        "#": ("#", DIREITA, ESTADO_REJEICAO),
    },
    ESTADO_ACEITACAO: {},
    ESTADO_REJEICAO: {},
}


def executar_maquina_turing(cadeia: str, detalhado: bool = False, limite_passos: int = 100_000) -> dict:
    fita = list(cadeia) if cadeia else [BRANCO]
    cabeca = 0
    estado_atual = ESTADO_INICIAL
    passos = 0
    historico = []

    # Cada volta executa um movimento da cabeca, que e o passo usado no relatorio.
    while estado_atual not in {ESTADO_ACEITACAO, ESTADO_REJEICAO} and passos < limite_passos:
        # A fita cresce quando a cabeca passa da parte ja criada.
        while cabeca >= len(fita):
            fita.append(BRANCO)
        if cabeca < 0:
            fita.insert(0, BRANCO)
            cabeca = 0

        simbolo = fita[cabeca]
        transicao = TRANSICOES.get(estado_atual, {}).get(simbolo)

        if transicao is None:
            estado_atual = ESTADO_REJEICAO
            break

        escrita, movimento, proximo_estado = transicao
        passos += 1

        if detalhado:
            fita_txt = "".join(fita)
            ponteiro = " " * cabeca + "^"
            print(
                f"  Passo {passos:>4}: estado={estado_atual!r}, le={simbolo!r}, "
                f"escreve={escrita!r}, move={movimento}, -> {proximo_estado!r}"
            )
            print(f"           Fita: {fita_txt}")
            print(f"                 {ponteiro}")

        historico.append(
            {
                "passo": passos,
                "estado": estado_atual,
                "le": simbolo,
                "escreve": escrita,
                "movimento": movimento,
                "proximo": proximo_estado,
                "cabeca": cabeca,
                "fita": "".join(fita),
            }
        )

        fita[cabeca] = escrita
        cabeca = cabeca + 1 if movimento == DIREITA else cabeca - 1
        estado_atual = proximo_estado

    aceita = estado_atual in ESTADOS_FINAIS
    return {
        "aceita": aceita,
        "passos": passos,
        "historico": historico,
        "estado_final": estado_atual,
    }


def explicar(cadeia: str):
    print(f"\n=== Maquina de Turing - w#w - Cadeia: {cadeia!r} ===")
    resultado = executar_maquina_turing(cadeia, detalhado=True)
    veredito = "ACEITA" if resultado["aceita"] else "REJEITA"
    print(f"Estado final: {resultado['estado_final']!r}  ->  {veredito}")
    print(f"Total de passos: {resultado['passos']}")
    return resultado


TESTES_PADRAO = [
    ("#", True),
    ("0#0", True),
    ("101#101", True),
    ("0#1", False),
    ("101#100", False),
    ("01#011", False),
]


def executar_testes(testes=None):
    testes = testes or TESTES_PADRAO
    print("\n=== BATERIA DE TESTES - Linguagem Recursiva (w#w) ===")
    print(f"{'Cadeia':<20} {'Esperado':<10} {'Obtido':<10} {'Passos':<8} {'OK?'}")
    print("-" * 60)
    todos_ok = True

    for cadeia, esperado in testes:
        resultado = executar_maquina_turing(cadeia)
        ok = resultado["aceita"] == esperado
        todos_ok = todos_ok and ok
        esperado_txt = "ACEITA" if esperado else "REJEITA"
        obtido_txt = "ACEITA" if resultado["aceita"] else "REJEITA"
        status = "OK" if ok else "FALHOU"
        print(f"{cadeia:<20} {esperado_txt:<10} {obtido_txt:<10} {resultado['passos']:<8} {status}")

    print("-" * 60)
    print(f"Resultado geral: {'TODOS OK' if todos_ok else 'FALHAS DETECTADAS'}\n")
    return todos_ok


if __name__ == "__main__":
    if len(sys.argv) > 1:
        explicar(sys.argv[1])
    else:
        explicar("101#101")
        explicar("101#100")
        print()
        executar_testes()
