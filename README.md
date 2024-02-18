# Bancos de Dados Relacionais (MySQL) na AWS com Amazon RDS

## Serviços utilizados

- Amazon RDS
- AWS Lambda
- MySQL Workbench

## Criando o banco de dados no Amazon RDS

- AWS Console -> Amazon RDS -> Create database -> Standard create -> MySQL -> Versão padrão -> Free Tier -> DB instance identifier [nome_da_instância] -> Master username [admin] -> Master password [sua_senha_forte] -> DB instance size - padrão -> Storage - configurações padrão -> Connectivity - vpc padrão -> Publicly accessible [yes] -> VPC Security - padrão -> Database authentication [password authentication] -> Create database
- Selecionar o DB criado -> Connectivity & security -> Copiar endpoint.

### No MySQL Workbench

- MySQL Connections -> New -> Connection name [nome_da_instancia] -> Hostname - colar o endpoint copiado no passo anterior -> Username [admin] -> Teste Connection -> Password [sua_senha]

#### Em caso de problemas na conexão

- Security -> VPC security groups -> Acessar o SG criado -> Inbound -> Edit -> Add rule -> type [All traffic] -> Source [Anywhere] -> Save
#OBS: Em ambientes produtivos não deixamos os acessos liberados dessa forma, utilizamos o conceito de menor privilégio.

### No MySQL Workbench

- Selecionar a conexão criada -> Password [sua_senha_forte]

## Criando queries

 - Criar um database:
 
    ```CREATE DATABASE NOME_DO_SEU_BANCO;```

- Acessar o db criado

    ```USE NOME_DO_SEU_BANCO;```

- Criar uma tabela de usuários

   ```
   CREATE TABLE user (
     id bigint(20) NOT NULL, 
     email varchar(40) NOT NULL,
     username varchar(15) NOT NULL,
     password varchar(100) NOT NULL,
     PRIMARY KEY (id)
   );
   ```
    
- Criar uma tabela de carrinho de compras
    
   ```
   CREATE TABLE role (
     id bigint(20) NOT NULL,
     name varchar(60) NOT NULL, 
     PRIMARY KEY (id)
   );
   ```
- Criar uma tabela associativa entre as tabelas user e roles

    ```
    CREATE TABLE user_roles (
      user_id bigint(20) NOT NULL,
      role_id bigint(20) NOT NULL,
      FOREIGN KEY (user_id) REFERENCES user (id) ON DELETE RESTRICT ON UPDATE CASCADE,
      FOREIGN KEY (role_id) REFERENCES role (id) ON DELETE RESTRICT ON UPDATE CASCADE,
      PRIMARY KEY (user_id, role_id)
    );
    ```
- Descrevendo o esquema de uma tabela 
 
   ```
   CREATE TABLE user_roles (
     user_id bigint(20) NOT NULL,
     role_id bigint(20) NOT NULL,
     FOREIGN KEY (user_id) REFERENCES user (id) ON DELETE RESTRICT ON UPDATE CASCADE,
     FOREIGN KEY (role_id) REFERENCES role (id) ON DELETE RESTRICT ON UPDATE CASCADE,
     PRIMARY KEY (user_id, role_id)
   );
   ```
  
- Inserindo dados em tabelas

  ```
  INSERT INTO user VALUES (1, 'arimateia.junior@arijrtechnology.com', 'Arimateia', 'db@123');
  INSERT INTO user VALUES (2, 'ana.beatriz@arijrtechnology.com', 'Beatriz', 'db@123');
  INSERT INTO user VALUES (3, 'newdon@arijrtechnology.com', 'Newdon', 'db@123');
  INSERT INTO user VALUES (4, 'joana@arijrtechnology.com', 'Joana', 'db@123');
  INSERT INTO user VALUES (5, 'janaina@arijrtechnology.com', 'Janaina', 'db@123');
  INSERT INTO user VALUES (6, 'theo@arijrtechnology.com', 'Theo', 'db@123');

  INSERT INTO role VALUES (3, 'ADMIN');
  INSERT INTO role VALUES (4, 'USER');

  INSERT INTO user_roles VALUES (1, 3);
  INSERT INTO user_roles VALUES (2, 4);
  INSERT INTO user_roles VALUES (3, 4);
  INSERT INTO user_roles VALUES (4, 3);
  INSERT INTO user_roles VALUES (5, 4);
  INSERT INTO user_roles VALUES (6, 4);
  ```
  
- Selecionando todos os registros de uma tabela

  ```
  SELECT * FROM [table_name];
  ```
- Selecionando dados da tabela associativa

  ```
  SELECT user.id, user.email, user.username, role.id AS role_id, role.name AS role_name
  FROM user 
  JOIN user_roles on (user.id=user_roles.user_id)
  JOIN role on (role.id=user_roles.role_id);
  ```

## Realizando queries no Amazon RDS a partir de uma função no AWS Lambda

### Criando a função Lambda

 - Acessar o AWS Lambda console -> Create function -> Author from scratch -> Function name [nome_da_funcao] -> Runtime - Python3.9 -> Create new role from AWS policy template -> Role name [nome_da_role] -> Create function

### Configurando permissões de acesso ao RDS

- Selecionar a função criada -> Configuration -> Permissions -> Selecionar a função criada e abrir no console do AWS IAM
- Attach policies -> Pesquisar pela policy AWSLambdaVPCAccessExecutionRole -> Attach policy

### Desenvolvendo o código da função Lambda

- Editor de código da função criada -> Inserir o código disponível na pasta ```src``` deste projeto

### Importando a biblioteca ```pymysql``` utilizando Lambda Layers

- Lambda Dashboard -> Layers -> Create layer -> Name [nome_da_layer] -> Upload a .zip file - o arquivo ```pymsql-python.zip``` está disponível na pasta ```src``` do projeto -> Compatible architectures x86_64 -> Compatible runtimes - Python 3.9 -> Create
- Lambda Dashboard -> selecionar a função criada -> Layers -> Add a layer -> Custom layers -> selecionar o layer criado anteriormente -> Add

### Testando a função criada

- Test -> New event -> Template -> Hello World -> Name [test] -> Save changes -> Test
