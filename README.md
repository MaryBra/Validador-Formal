# Validador-Formal

Validador Formal em 3 níveis - implementando 3 reconhecedores formais para cada nível da hierarquia de Chomsky:

Nível  |  Linguagem          | Modelo   |   Problema
_______| ____________________| _________| ______________________________________________
LR     |  Regular            | DFA      |   Formato de CPF (ddd.ddd.ddd-dd)
LLC    |  Livre de Contexto  | PDA      |   Parênteses/colchetes/chaves balanceadas
R      |  Recursiva          | MT       |   Cópia de cadeia w#w onde W E {0,1}*

#Pré requisitos:

Arquivo "requirements.txt" -> pip install -r requirements.txt (não é obrigatório a execução)

#Estrutura do projeto

projeto/
├── README.md
├── requirements.txt
├── testes.py                        # roda a bateria completa
├── src/
│   ├── regular.py                   # reconhecedor LR (DFA - CPF)
│   ├── livre_contexto.py            # reconhecedor LLC (PDA - parênteses)
│   └── recursiva.py                 # reconhecedor R  (MT  - w#w)
├── testes/
│   ├── testes_regular.txt
│   ├── testes_livre_contexto.txt
│   └── testes_recursiva.txt
├── diagramas/
│   └── (diagramas PNG/SVG/PDF aqui)
└── relatorio/
    └── relatorio.pdf

# Como executar

Bateria completa (todos os 3 reconhecedores)

bash -> python testes.py

Reconhecedor individual com passo a passo de execução dos modelos

#LR - CPF
python src/regular.py "565.646.646.88"
python src/regular.py "52.15.15-54"

#LCC - Parênteses
python src/livre_contexto.py "((x+y)*z)"
python scr/livre_contexto.py "((aa+b)"

#R - w#w
python src/recursiva.py "101#101"
python src/recursiva.py "101#100"

Sem argumento, cada script roda seu próprio modelo (cadeia aceita + cadeia rejeitada + bateria interna):

python src/regular.py
python src/livre_contexto.py
python src/recursiva.py


Definição de "passo" de acordo com as especificações do projeto:

Modelo | Passo
_______| ________________________________________________________
DFA    | Cada leitura de símbolo com mudança de estado
PDA    | Cada transição + cada empilhamento/desempilhameto
MT     | Cada movimento da cabeça (leitura + escrita + deslocamento)


    
