# Projeto de Circuitos Digitais

---

## Sobre

O presente projeto se refere à implementação requerida na conclusão da matéria de Laboratório de Circuitos Digitais
ministrada na UFLA - Universidade Federal de Lavras, Brasil - em 2024. A matéria diz respeito a descrição de hardware em
placas passíveis de reprogramação. Durante as aulas práticas que foram ministradas
pelo [Dr. Bruno de Abreu Silva](https://dcc.ufla.br/equipe/equipe/434-bruno-de-abreu-silva.html), utilizou-se de Verilog
a fim de descrever o funcionamento interno do hardware em placas do tipo FPGA, fabricadas pela Altera, do modelo
DE10-Lite, portanto, a presente implementação visa funcional, preferencialmente, no referido FPGA.

A ideia do projeto não é original, conforme acordado com o professor, implementamos o ministrado na última aula prática.
Não necessariamente visando a funcionalidade, mas explorar a possibilidade de uso do Amaranth no que tange à descrição
de hardware em outra linguagem, Python, no caso.

## Objetivos

Os objetivos do projeto se dividem em duas partes:

- Implementação do ministrado na última aula de Laboratório de Circuitos Digitais;
- Pesquisa quanto a possibilidade de uso de outras linguagens no processo de descrição de hardware;

### Implementação

O ministrado na última aula objetiva a criação de uma máquina de estados que exibe, por meio de um cabo VGA, um quadrado
passível de movimentação conforme o clock, reduzido, da placa e uso de botões a fim de definir a direção de movimento
com base em rotações à direita ou à esquerda. Parte expressiva do feito em aula fora implementado
por [Dr. Bruno de Abreu Silva](https://dcc.ufla.br/equipe/equipe/434-bruno-de-abreu-silva.html) - conta no repositório
sobre o diretório `base` -, feito em Verilog. Com base no fornecido os alunos Arthur Valadares Campideli e Hugo Prado
Lima transpilaram o conteúdo para Python com o uso de Amaranth.

[//]: # (### Pesquisa)

[//]: # (TODO: Testar e adicionar essa seção)

## Usando esse repositório

Para fazeres o uso deste repositório basta cloná-lo para a sua máquina, criar um ambiente virtual em python, instalar os
requisitos para o funcionamento que constam em [requirements.txt](requirements.txt). Em seguida, execute o script
principal - `main.py` -, usando o interpretador. Ele lhe retornará o uso da interface de linha de comando.

- **Parse**, esse comando traduz o implementado de python para Verilog. Recebe como argumento o arquivo de destino no
  qual o conteúdo deve ser escrito. Tal arquivo não deve ser pré-existente;
- **Simulate**, simula o projeto. Recebe um arquivo .vcd onde o conteúdo deve ser escrito. Tal arquivo não deve ser
  pré-existente.

## Arquivo .VCD

É um formato de arquivo que representa as varições de ondas ao longo do tempo dentro de um circuito digital, passível de
intepretação por, por exemplo, [Surfer](https://surfer-project.org).

## Autores

- Arthur Valadares Campideli
- Hugo Prado Lima