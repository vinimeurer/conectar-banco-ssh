
# Documentação do Código ConectarBanco com SSHTunnelForwarder

Este código Python tem como objetivo estabelecer e manter uma conexão SSH segura entre uma máquina local e um banco de dados remoto, através do uso de um túnel SSH. Utiliza a biblioteca `sshtunnel` para criar o túnel e a biblioteca `paramiko` para lidar com autenticação via chave privada SSH. O código foi estruturado em uma classe chamada `ConectarBanco`, que facilita o processo de conectar-se aos servidores e manter a conexão ativa.

Abaixo, segue uma explicação detalhada sobre como usar e alterar os campos necessários para configurar o código corretamente.

## Requisitos

Antes de executar o código, você precisa ter as seguintes dependências instaladas:

1.  **`sshtunnel`**: Para criar o túnel SSH.
2.  **`paramiko`**: Para lidar com a autenticação SSH.

Para instalar as dependências, execute o seguinte comando no terminal:

```bash
pip install sshtunnel paramiko
``` 

## Estrutura do Código

O código está estruturado na classe `ConectarBanco`, com os seguintes métodos principais:

-   **`__init__`**: Construtor da classe que inicializa as variáveis e configura a chave SSH.
-   **`conectar`**: Estabelece o túnel SSH.
-   **`manter_conexao`**: Mantém o túnel SSH ativo, verificando a cada 10 segundos se a conexão está viva.
-   **`fechar_conexao`**: Fecha o túnel SSH.

Abaixo está a explicação detalhada de como configurar e usar o código.

----------

## Como Usar

### Passo 1: Alterar Variáveis de Conexão

No código, existem variáveis de configuração que precisam ser alteradas para corresponder à sua infraestrutura e autenticação SSH.

#### 1.1 Definindo os parâmetros de SSH

A primeira coisa a fazer é configurar os parâmetros de SSH no bloco `__main__`:

```python
ssh_host = ''       # Host do SSH (ex: 'ssh.exemplo.com')
ssh_port = 22       # Porta do SSH (geralmente 22, mas pode ser outra dependendo do servidor)
ssh_username = ''   # Usuário SSH (ex: 'usuario_ssh')
ssh_key_path = ''   # Caminho para a chave privada SSH (ex: '/path/to/key.pem')
``` 

-   **`ssh_host`**: O endereço IP ou nome de domínio do servidor SSH. Este é o servidor intermediário pelo qual você acessará o banco de dados.
-   **`ssh_port`**: A porta SSH usada para a conexão. O valor padrão é 22, mas pode ser alterado se o servidor SSH usar uma porta diferente.
-   **`ssh_username`**: O nome de usuário para autenticação SSH. Esse nome de usuário deve ser válido no servidor SSH.
-   **`ssh_key_path`**: O caminho para a chave privada SSH (geralmente um arquivo `.pem` ou `.key`). Essa chave é usada para autenticação ao servidor SSH.

#### 1.2 Configurando os Hosts dos Bancos de Dados

Dentro do método `__init__` da classe `ConectarBanco`, há quatro variáveis representando os hosts dos bancos de dados:

```python
self.hostBanco1 = 'host'
self.hostBanco2 = 'host'
self.hostBanco3 = 'host'
self.hostBanco4 = 'host'
``` 

Esses valores devem ser alterados para os endereços IP ou domínios dos servidores de banco de dados que você deseja acessar. Caso você tenha menos ou mais servidores de banco de dados, basta ajustar a quantidade dessas variáveis.

#### 1.3 Alterando Portas Locais e Remotas

No código, os bancos de dados remotos estão sendo mapeados para portas locais específicas. O mapeamento é feito da seguinte forma:

```python
remote_bind_addresses=[
	(self.hostBanco1, 3306), 
	(self.hostBanco2, 3306),
	(self.hostBanco3, 3306), 
	(self.hostBanco4, 3306)
]

local_bind_addresses=[
	('127.0.0.1', 4400), 
	('127.0.0.1', 4500), 
	('127.0.0.1', 4600), 
	('127.0.0.1', 4700)
]
``` 

-   **`remote_bind_addresses`**: Define os endereços e portas remotas do banco de dados. O código está configurado para se conectar a quatro bancos de dados na porta padrão MySQL (`3306`), mas você pode alterar a porta caso seu banco de dados utilize outra.
    
-   **`local_bind_addresses`**: Define os endereços e portas locais para os quais as conexões SSH serão encaminhadas. Neste caso, as portas locais são 4400, 4500, 4600 e 4700, mas é possível alterar para a porta que desejar.. O valor `127.0.0.1` refere-se ao endereço de loopback (localhost), e cada porta local será mapeada para um banco de dados remoto correspondente.
    

Se você precisar de mais ou menos bancos de dados, adicione ou remova as entradas de ambos os arrays, certificando-se de que o número de entradas em `remote_bind_addresses` e `local_bind_addresses` seja o mesmo.

----------

### Passo 2: Executando o Código

Uma vez que você configurou todos os parâmetros corretamente, pode executar o código. Isso irá iniciar a conexão SSH e configurar os túneis para acessar os bancos de dados. O fluxo do código será o seguinte:

1.  **Conexão SSH**: A função `conectar()` é chamada para tentar estabelecer a conexão SSH. Se a conexão falhar, o código tentará reconectar após 5 segundos.
2.  **Manter a Conexão**: A função `manter_conexao()` mantém a conexão viva, verificando a cada 10 segundos se o túnel está ativo. Se o túnel for fechado ou perdido, o código tentará reconectar automaticamente.

### Passo 3: Fechando a Conexão

Se você deseja fechar a conexão SSH de forma manual, pode chamar a função `fechar_conexao()`. Esta função irá parar o túnel e exibir a mensagem de que a conexão foi fechada.

----------

## Explicação dos Métodos

### `__init__(self, ssh_host, ssh_port, ssh_username, ssh_key_path)`

Este é o método de inicialização da classe. Ele recebe como parâmetros as informações de conexão SSH (host, porta, usuário e caminho da chave SSH) e inicializa a chave RSA e as variáveis para os hosts do banco de dados.

### `conectar(self)`

O método `conectar()` cria o túnel SSH com as configurações definidas. Ele usa o `SSHTunnelForwarder` para criar um túnel SSH entre o servidor local e os servidores de banco de dados remotos.

-   Caso a conexão SSH falhe, o código tenta reconectar após 5 segundos, repetindo esse processo até conseguir conectar.

### `manter_conexao(self)`

Este método mantém a conexão SSH ativa, verificando a cada 10 segundos se o túnel está funcionando corretamente. Se o túnel for fechado ou a conexão for perdida, ele tenta reconectar.

### `fechar_conexao(self)`

Este método fecha o túnel SSH de forma segura quando a execução do script for interrompida ou quando não for mais necessário manter a conexão ativa.


## Exemplos de Uso

Digamos que você tem as seguintes configurações:

-   **Servidor SSH (intermediário)**: `ssh.exemplo.com`
-   **Usuário SSH**: `usuario_ssh`
-   **Caminho para a chave privada**: `C:\Chave.pem`
-   **Bancos de Dados**:
    -   **Banco 1**: Rodando no servidor `dbserver1.exemplo.com` na porta `3306`
    -   **Banco 2**: Rodando no servidor `dbserver2.exemplo.com` na porta `3306`
    -   **Banco 3**: Rodando no servidor `dbserver3.exemplo.com` na porta `3306`

Agora, você deseja acessar esses bancos de dados localmente na sua máquina nas portas `4400`, `4500` e `4600`, respectivamente.

### Passo a Passo

1.  **Alterando as variáveis no código**:

No código, você precisa preencher as variáveis com as informações reais de conexão. Aqui está o que você faria:

```python
if __name__ == "__main__":
    ssh_host = 'ssh.exemplo.com'    # Host do SSH
    ssh_port = 22                   # Porta do SSH (geralmente 22, mas pode ser outra)
    ssh_username = 'usuario_ssh'    # Nome de usuário SSH
    ssh_key_path = 'C://Chave.pem'  # Caminho para a chave privada SSH

    manager = ConectarBanco(ssh_host, ssh_port, ssh_username, ssh_key_path)
    manager.conectar()  		# Estabelece o túnel SSH
    manager.manter_conexao()  	# Mantém o túnel ativo
``` 

2.  **Alterando os hosts dos bancos de dados**:

Agora, você precisa garantir que o código esteja apontando para os servidores de banco de dados corretos. No caso, você possui 3 bancos de dados:

```python
self.hostBanco1 = 'dbserver1.exemplo.com'  # Banco 1
self.hostBanco2 = 'dbserver2.exemplo.com'  # Banco 2
self.hostBanco3 = 'dbserver3.exemplo.com'  # Banco 3
``` 

3.  **Portas locais e remotas**:

Em seguida, você precisa garantir que as portas locais correspondam às que você deseja usar para se conectar aos bancos de dados. Como você quer acessar os 3 bancos na sua máquina local, mapeie as portas locais como `4400`, `4500` e `4600`:

```python
# Bancos remotos
remote_bind_addresses=[
	(self.hostBanco1, 3306), 
	(self.hostBanco2, 3306), 
	(self.hostBanco3, 3306)
]  

# Portas locais
local_bind_addresses=[
	('127.0.0.1', 4400), 
	('127.0.0.1', 4500), 
	('127.0.0.1', 4600)
]  
``` 

Isso significa que, após o túnel ser estabelecido, você poderá acessar os bancos de dados da seguinte forma:

-   O **Banco 1** estará disponível na sua máquina local na porta `4400` (acesso via `127.0.0.1:4400`).
-   O **Banco 2** estará disponível na sua máquina local na porta `4500` (acesso via `127.0.0.1:4500`).
-   O **Banco 3** estará disponível na sua máquina local na porta `4600` (acesso via `127.0.0.1:4600`).

4.  **Acessando os Bancos de Dados Localmente**:

Agora que o túnel SSH está configurado e ativo, você pode usar qualquer cliente de banco de dados local (como MySQL Workbench, DBeaver ou até mesmo a linha de comando) para se conectar aos bancos de dados usando os seguintes parâmetros de conexão:

-   **Banco 1**: `127.0.0.1:4400`
-   **Banco 2**: `127.0.0.1:4500`
-   **Banco 3**: `127.0.0.1:4600`

Esses endereços locais serão encaminhados para os bancos de dados remotos através do túnel SSH.

## Conclusão

Este código é útil para configurar túneis SSH para acessar servidores de banco de dados de forma segura. Certifique-se de configurar corretamente os parâmetros de SSH, os hosts de banco de dados e as portas locais. Com isso, você será capaz de estabelecer conexões seguras e manter essas conexões ativas com o código fornecido.