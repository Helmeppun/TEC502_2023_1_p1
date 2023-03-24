# TEC502_2023_1_p1
Sistema de comunicação entre medidores de energia simulados, um servidor baseado em sockets, e clientes seguindo o protocolo HTTP

## Requisitos

* Python 3.10

Certifique-se que o medidor está conectado no endereço IP correto ao iniciar o programa.

## Medidor

O medidor envia mensagems em formato CSV (Código do medidor;Horário de medição;Valor da medição), e utiliza a porta 1330 com comunicação UDP. Mensagens são enviadas a cada 10 segundos. Medidores suportam 2 modos de operação: manual e automático. Ao iniciar o algoritmo do medidor, é necessário especificar um código para o mesmo. Após isso, o medidor gera valores aleatórios de consumo de energia e permite que o usuário insira valores manualmente, criando uma lista de valores a serem enviados que esvazia a cada 10 segundos.

Também existe um medidor completamente automático, que não recebe código ou medidas inseridas. Ele determina seu própio código aleatoriamente e envia mensagens automaticamente.

## Servidor

O servidor é composto de 2 threads, 2 arquivos .json que representam uma base de dados, e uma API REST. O servidor tem a capacidade de criar mais threads durante a execução.

* Thread UDP: Socket na porta 1330. Recebe mensagens dos medidores e insere as medidas em medidores.json através da API.
* Thread TCP: Socket na porta 2126. Procura por conexões com clientes. Caso o servidor aceite uma conexão, ele cria 1 thread para tratar futuras mensagens do cliente.
* Thread Cliente: Recebe Requests e envia Responses HTTP através da API. Dependendo do conteúdo das Requests, o servidor pode fazer alterações tanto em medidores.json como funcionarios.json.

## API

Após decodificar uma Request e verificar seu metódo (POST, GET, PUT, etc.), o servidor verifica se a rota é suportada pela API e utiliza a mesma para fazer manipulações na base de dados e gerar uma Response HTTP, que é enviada de volta ao cliente pelo socket TCP. A API do projeto é REST, mas não RESTful, pois o servidor pode manter dados de sessão de um cliente. Seguem as rotas da API.

### /loginCliente

  > POST /loginCliente HTTP/1.1
  
  > Host: 172.61.301.3:2126
  
  > User-Agent: exemplo/README
  
  > Content-Type: application/json
  
  > Accept: \*/\*
  
  > Content-Length: 15
  
  >{"codigo": "2"}


Descrição: Procura um medidor com o código fornecido na base de dados. Caso encontrado, o servidor inicia uma sessão para o cliente, para que ele não precise
inserir o código do seu medidor em outras operações.


### /loginFuncionario

> POST /loginFuncionario HTTP/1.1

> Host: 172.61.301.3:2126

> User-Agent: exemplo/README

> Content-Type: application/json

> Accept: */*

> Content-Length: 38

> {"matricula": "0954", "senha": "0504"}

Descrição: Realiza o login de um cliente no sistema se existir uma conta de funcionário com o par de matricula e senha inseridos.

### /cadastrarFuncionario

> POST /cadastrarFuncionario HTTP/1.1

> Host: 172.61.301.3:2126

> User-Agent: exemplo/README

> Content-Type: application/json

> Accept: */*

> Content-Length: 69

> {"matricula": "12036", "nome": "Marcos Valle", "senha": "sambadeverao2", "auth": "1"}

Descrição: Tenta criar um novo funcionário na base de dados. Se já existe um funcionário com a matrícula inserida, o cadastro não ocorre. Esta operação só pode ser feita por um funcionário com nível de autorização 2.

### /cadastrarMedidor

> POST /cadastrarMedidor HTTP/1.1

> Host: 172.61.301.3:2126

> User-Agent: exemplo/README

> Content-Type: application/json

> Accept: */*

> Content-Length: 16

> {"codigo": "85"}

Descrição: Tenta criar um novo medidor na base de dados. Se já existe um medidor com o código fornecido, o cadastro não ocorre.

### /historico

> POST /historico HTTP/1.1

> Host: 172.61.301.3:2126

> User-Agent: exemplo/README

> Content-Type: application/json

> Accept: */*

> Content-Length: 14

> {"prazo": "7"}

Descrição: O servidor retorna as médias de consumo de um medidor em kW/h, e a média entre esses dias. O número de dias calculados é determinado pelo prazo. Caso um dos valores fique acima da média do prazo, o servidor informa que houve uma grande variação no consumo.

### /fatura

> GET /fatura HTTP/1.1

> Host: 172.61.301.3:2126

> User-Agent: exemplo/README

> Accept: */*

* Parâmetros de Response: resultado, fatura

Descrição: O servidor soma o consumo do último mês de um medidor e retorna a fatura em R$.

### inserirMedida

>2;2023-03-23 20:29:49.060113;7.77

Esse metódo da API é para os medidores, que não se comunicam com HTTP. Medições só são inseridas na base de dados se o código fornecido pelo medidor estiver cadastrado.

## Docker

Comando docker para container do servidor:

> docker run helmeppun/p1redesgn:1.0

Comando docker para container do medidor:

>docker run -it helmeppun/p1redesmed:2.0

Comando docker para container do medidor compátivel com portainer

>docker run helmeppun/p1redesmedauto:1.0

## Resultados

* O problema cumpre a maioria dos requisitos, mas faltou a possibilidade de alterar a frequência de envio dos medidores.
* Quando os medidores estão na base de dados, eles tem um atributo de atividade, que indica se um medidor está funcionando ou não. O plano era adicionar uma rota do funcionário para desativar medidores que não funcionam, fazendo com que a API não insira medidas destes medidores quebrados, mantendo a integridade de dados. Isso pode ser implementado em futuras versões.
