# Project_TI

Este é um projeto Python que usa Flask e MySQL para criar um aplicativo web. Este aplicativo permite que os usuários se cadastrem, façam login e consultem informações de posição de veículos através de uma API externa, além de plotar trajetos de veículos em um mapa.


### 📋 Pré-requisitos

Para garantir o funcionamento adequado do site, você precisa das seguintes dependências:

```
Python 3+
Flask 
MySQL
gmplot
geopy
marshmallow
requests
mysql-connector-python

```

Você também precisará de um servidor MySQL rodando localmente com um banco de dados chamado 'db_ti' e uma tabela 'cadastro' com campos 'user' e 'password'. Ajuste a variável db_config no código com as configurações do seu servidor MySQL.

Além disso, você deve preencher as variáveis loginwr e passwordwr com suas credenciais para a API da Webrota.


### 🔧 Site operacional

Você pode executar o projeto usando o comando:


```
python nome_do_seu_arquivo.py
```
Isto irá iniciar o servidor Flask na porta 8000. Abra o navegador e acesse localhost:8000 para visualizar o aplicativo.



## ⚙️ Executando os testes

Para testar a funcionalidade completa deste projeto, você precisará seguir os passos abaixo:

- `1`: Insira suas credenciais de acesso à API da Webrota no código fonte do projeto.
- `2`: Execute o servidor do aplicativo localmente. Acessando a interface do usuário por meio do navegador, você verá uma tela de login.
- `3`: Se ainda não tiver uma conta, você pode criar uma clicando no link de cadastro. Insira um nome de usuário e uma senha para criar uma nova conta.
- `4`: Após a criação da conta, você pode fazer login inserindo suas credenciais na tela de login.
- `5`: Após o login, você será redirecionado para a tela de posição. A partir daí, você pode inserir uma placa exata que esteja cadastrada no sistema da Webrota, que tenha um 1* rastreador instalado e que tenha percorrido um trajeto no dia 3 de julho de 2023, entre 00:00 e 23:59.
- `6`:Clique em "Search" após inserir a placa do veículo. O programa buscará as informações de posição do veículo nesse período e exibirá o trajeto no mapa, além de informar a distância total percorrida pelo veículo nesse dia.

**Por favor, observe que para um teste bem-sucedido, é fundamental que a placa inserida esteja de acordo com os critérios mencionados no passo 5. 
Este projeto foi desenvolvido com base nos dados disponíveis na API da Webrota e, portanto, seu funcionamento correto depende da disponibilidade e precisão desses dados.**

 



## 🛠️ Construído com

Mencione as ferramentas que você usou para criar seu projeto

* **[Python]** - Linguagem de programação usada
* **[Flask]** - Framework web usado para desenvolver o aplicativo
* **[MySQL]** - Sistema de gerenciamento de banco de dados usado
* **[gmplot]** - Biblioteca Python para plotar dados no Google Maps
* **[geopy]** - Biblioteca Python para operações geoespaciais
* **[marshmallow]** - Biblioteca Python para validação de dados, serialização/desserialização e transformação de objetos complexos para tipos de dados Python
* **[requests]** - Biblioteca Python para fazer requisições HTTP de maneira simples
* **[mysql-connector-python]** - Conector MySQL para Python






## ✒️ Autores

* [Vinicius Jose] - Trabalho Inicial - [https://github.com/ViniciusJBSilva]
