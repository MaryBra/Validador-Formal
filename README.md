# Validador Formal

Validador Formal em 3 níveis, implementando 3 reconhecedores formais para cada nível da hierarquia de Chomsky.

## Níveis implementados

| Nível | Linguagem | Modelo | Problema |
|--------|-----------|---------|-----------|
| LR | Regular | DFA | Formato de CPF (ddd.ddd.ddd-dd) |
| LLC | Livre de Contexto | PDA | Parênteses/colchetes/chaves balanceadas |
| R | Recursiva | MT | Cópia de cadeia `w#w`, onde `w ∈ {0,1}*` |

## Pré-requisitos

Arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

*(A instalação não é obrigatória para execução dos testes básicos.)*

## Estrutura do projeto

```text
projeto/
├── README.md
├── requirements.txt
├── testes.py                        # roda a bateria completa
├── src/
│   ├── regular.py                   # reconhecedor LR (DFA - CPF)
│   ├── livre_contexto.py            # reconhecedor LLC (PDA - parênteses)
│   └── recursiva.py                 # reconhecedor R (MT - w#w)
├── testes/
│   ├── testes_regular.txt
│   ├── testes_livre_contexto.txt
│   └── testes_recursiva.txt
├── diagramas/
│   └── (diagramas PNG/SVG/PDF aqui)
└── relatorio/
    └── relatorio.pdf
```

## Como executar

### Bateria completa (todos os 3 reconhecedores)

```bash
python testes.py
```

### Reconhecedores individuais

#### LR - CPF

```bash
python src/regular.py "565.646.646-88"
python src/regular.py "52.15.15-54"
```

#### LLC - Parênteses balanceados

```bash
python src/livre_contexto.py "((x+y)*z)"
python src/livre_contexto.py "((aa+b)"
```

#### R - Cadeia w#w

```bash
python src/recursiva.py "101#101"
python src/recursiva.py "101#100"
```

### Execução sem argumentos

Sem argumentos, cada script executa:

- Uma cadeia aceita
- Uma cadeia rejeitada
- Uma bateria interna de testes

```bash
python src/regular.py
python src/livre_contexto.py
python src/recursiva.py
```

## Definição de "passo"

| Modelo | Passo |
|---------|--------|
| DFA | Cada leitura de símbolo com mudança de estado |
| PDA | Cada transição + cada empilhamento/desempilhamento |
| MT | Cada movimento da cabeça (leitura + escrita + deslocamento) |
