# Validador Formal

Validador Formal em 3 níveis, implementando 3 reconhecedores formais para cada nível da hierarquia de Chomsky.

## Níveis implementados

| Nível | Linguagem | Modelo | Problema |
| --- | --- | --- | --- |
| LR | Regular | DFA | Formato de CPF (`ddd.ddd.ddd-dd`) |
| LLC | Livre de Contexto | PDA | Parênteses, colchetes e chaves balanceadas |
| R | Recursiva | MT | Cópia de cadeia `w#w`, onde `w` pertence a `{0,1}*` |

## Pré-requisitos

Arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

A instalação não é obrigatória para execução dos testes básicos.

## Estrutura do projeto

```text
projeto/
├── README.md
├── requirements.txt
├── testes.py                        # roda a bateria completa
├── src/
│   ├── regular.py                   # reconhecedor LR (DFA - CPF)
│   ├── livre_contexto.py            # reconhecedor LLC (PDA - delimitadores)
│   └── recursiva.py                 # reconhecedor R (MT - w#w)
├── testes/
│   ├── testes_regular.txt
│   ├── testes_livre_contexto.txt
│   └── testes_recursiva.txt
├── diagramas/
│   ├── dfa_regular.svg
│   ├── pda_livre_contexto.svg
│   └── mt_recursiva.svg
└── relatorio.pdf
```

## Como executar

### Bateria completa

Roda os testes dos 3 reconhecedores:

```bash
python testes.py
```

## Reconhecedores individuais

### LR - CPF

```bash
python src/regular.py "565.646.646-88"
python src/regular.py "52.15.15-54"
```

### LLC - Delimitadores balanceados

```bash
python src/livre_contexto.py "((x+y)*z)"
python src/livre_contexto.py "((aa+b)"
```

### R - Cadeia w#w

```bash
python src/recursiva.py "101#101"
python src/recursiva.py "101#100"
```

## Execução sem argumentos

Sem argumentos, cada script executa:

- uma cadeia aceita;
- uma cadeia rejeitada;
- uma bateria interna de testes.

```bash
python src/regular.py
python src/livre_contexto.py
python src/recursiva.py
```

## Definição de passo

| Modelo | Passo |
| --- | --- |
| DFA | Cada leitura de símbolo da entrada com mudança de estado |
| PDA | Cada transição do PDA, incluindo empilhamento, desempilhamento ou transição vazia |
| MT | Cada movimento da cabeça sobre a fita, com leitura, escrita e deslocamento |

O módulo `re` do Python não é usado como reconhecedor principal.
