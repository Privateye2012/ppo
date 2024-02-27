
# Sistema de Gestão de Armazem de material de jogo

Este sistema permite recolher toda a informação de materiais de jogo apreendidos

## Estrutura

O sistema é estruturado da seguinte forma:
* Modelo de dados - Uma classe para cada tipo de informação (auto, material, etc)
* DAO - Data Access Object para permitir gravar/ler a informação na base de dados
* TUI - Text User Interface que permite a navegação nos autos/termos de entrega/materiais
* TEST - Testes unitários e geração automática de dados para testes do TUI
* GUI - Graphical User Interface - Para permitir editar a informação em janelas gráfica
* Main - Ponto de entrada no programa

A estrutura da base de dados é similar às classes e está definida no ficheiro ama_db.sql

Nesta fase, apresenta-se a estrutura da informação e um esqueleto dos métodos que
se prevê implementar e que no final permitirão ler e gravar autos numa base de dados postgresql.

## Modelo de dados

O modelo de dados define as classes que descrevem os dados geridos e consequentemente
permitem instanciar os objectos concretos.

## Data Access Object

As operações sobre a base de dados são encapsuladas em classes que implementam os comportamentos
de interacção com a base de dados.

Foi implementado uma classe DAO genérica, na qual estão definidas todos os métodos que podem
ser reutilizados nos DAO(s) concretos (que sabem efectuar as operações CRUD sobre uma classe de
dados e correspondente tabela concretas).

Os DAOs concretos usam a herditariedade multipla para poder usar métodos do DAO genérico e da
classe concreta do modelo (que corresponde a cada uma das classes de modelo e tabelas).

Para simplificar o código das operações CRUD, foram reescritos alguns operadores, nomeadamente:
* "+" Executa uma inserção na base de dados
* "-" Remove uma linha da base de dados , por id
* "+=" Altera os dados de um objecto na tabela correspondente
* "<<" Lê um objecto da base de dados, por id

## Base de dados

O sistema está preparado para uma base de dados Postgresql. Foi testado usando
um container docker com a imagem oficial. Para tal foi executado o comando que
se segue:

```
docker run --name ppo2 -e POSTGRES_PASSWORD=postgres -d postgres
```

Para aceder ao cliente de SQL, dentro do container, que permite a execução de
query(s) é usado o comando que se segue:

```
docker exec -it ppo psql -U postgres
```

## Testes unitários

Os testes unitários estão implementados no módulo ama_test.py, na classe
TestAmaCRUD, que extende a unittest.TestCase, que por sua vez está
implementada na framework unittest.

O módulo verifica se está a ser executado como main e se sim, executa o main
da framework. A framework baseia-se nos nomes dos métodos que têm de começar
por test. Executa cada um dos testes de forma autónoma e independente.

```
if __name__ == '__main__':
    unittest.main()
```

Foram criados os métodos de setUp e tearDown para garantir que a condição
inicial da execução de cada teste é efectuada com a base de dados vazia.

Cada teste é auto contido e verifica se um aspecto concreto funciona
correctamente, por exemplo exste um teste para os autos e um para
os materiais.

Os testes uinitários são executados na linha de comando com a instrução
seguinte:

```
python3 ama_test.py
```

Se nenhuma situação excepcional for encontrada, deve o resultado apresentado
será algo como:

```
......
----------------------------------------------------------------------
Ran 6 tests in 0.208s

OK
```

## Dados de teste

Para não obrigar a uma tarefa morosa de inserção manual na base
de dados, foi feito um programa que gera um conjunto de dados
para poder testar o funcionamento de toda a aplicação, inclusivamente
os User Interfaces.

Para tal, foi criada uma classe que deve ser executada de forma autónoma
com a instrução que se segue:

```
python3 ama_gen_test_data.py
```
## TUI - Text User Interface

Para efeitos de validação das ligações dos dados e para permitir
verificar a coerência do modelo, e, de forma transitória até que
o GUI com o tkinter esteja correcto, foi criado um User interface
textual que permite navegar na árvore de informação, sempre
começando pelos autos existentes em base dados, e ao escolher cada
um deles podendo ver a informação dos termo de entrega e para cada
termo de entrega, os materiais correspondentes.

Para executar o Text User Interface, a instrução na linha de comando deve ser:

```
python3 ama_tui.py
```

### Módulos utilizador

Para gerar um relatório em formato excel, foi usado o módulo xlsxwriter.
Para o instalar:

```
pip install xlsxwriter
```

Para gerar o relatório em formato CSV foi usado o módulo csv.

## Conclusão

Durante a execução deste trabalho, foi possivel aprender na prática várias técnicas de programação
orientada a objectos.

__Abstração__ - Ao definir classes que definem os tipos de dados geridos, e os métodos para com eles
trabalhar.

__Herança__ Foram definidas classes que gerem a informação e implementam métodos de uma forma não concreta
e que são extendidos por classes concretas que os trabalham na sua plenitude.

__Polimorfismo__ Através da reescrita de métodos, nas classes concretas que completam os comportamentos gerais.

Foram ainda usados a reescrita de operadores, o que simplifica muito o código que usa as classe/objectos
concretos.

A utilização de um programa para gerir dados de teste e de uma framework de testes unitários permitiram
ter confiança de um elevado grau de qualidade do código implementado.