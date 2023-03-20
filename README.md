# TEC502_2023_1_p1
Sistema de comunicação entre medidores de energia simulados, um servidor baseado em sockets, e clientes seguindo o protocolo HTTP

## Requisitos

* Python 3.10

## Medidor

O medidor envia mensagems em formato CSV (Código do medidor;Horário de medição;Valor da medição), e utiliza a porta 1330 com comunicação UDP.

## Rotas Suportadas

Para comunicação entre clientes/funcionários e servidor, o servidor faz comunicação TCP na porta 2126, utilizando as seguintes rotas HTTP.

### /loginCliente (POST)

* Parâmetros de Request: codigo
* Parâmetros de Response: resultado

Descrição: Realiza o login de um cliente no sistema se existir um medidor com o código fornecido.

### /loginFuncionario (POST)

* Parâmetros de Request: matricula, senha
* Parâmetros de Response: resultado

Descrição: Realiza o login de um cliente no sistema se existir uma conta de funcionário com o par de matricula e senha inseridos.

### /cadastrarFuncionario (POST)

* Parâmetros de Request: matricula, nome, senha, auth
* Parâmetros de Response: resultado

Descrição: O servidor tenta criar um novo funcionário. Se já existe um funcionário com a matrícula inserida, o cadastro não ocorre.

### /cadastrarMedidor (POST)

* Parâmetros de Request: codigo
* Parâmetros de Response: resultado

Descrição: O servidor tenta criar um novo funcionário. Se já existe um medidor com o código fornecido, o cadastro não ocorre.

### /historico (POST)

* Parâmetros de Request: prazo
* Parâmetros de Response: resultado, media, Medias de consumo

Descrição: O servidor retorna as médias de consumo de um medidor em kW/h, e a média entre esses dias. O número de dias calculados é determinado pelo prazo. Caso um dos valores fique acima da média do prazo, o servidor informa que houve uma grande variação no consumo.

### /fatura (GET) 

* Parâmetros de Response: resultado, fatura

Descrição: O servidor soma o consumo do último mês de um medidor e retorna a fatura em R$.
