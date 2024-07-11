# MVP Backend - Taverna Virtual

Este projeto contempla os requisitos para a entrega do MVP da **Sprint II: Arquitetura de Software** do curso de Pós Graduação em Engenharia de Software da PUC RIO.

O objetivo é utilizar do conteúdo ensinado durante as aulas para a criação de uma single page application, contando com front e backend. Para que isso fosse possível, foi criada uma Taverna virtual, onde as bebidas podem ser adicionadas, consultadas, ou excluídas.

Mais especificamente, para os códigos aqui encaminhados, será explorado o **backend do MVP**.

---
## Como executar local

1. Clone este repositório para sua máquina, se ainda não o fez:
```
git clone https://github.com/seu-usuario/seu-repositorio.git
```

2. Atualizar todas as libs python listadas conforme o arquivo `requirements.txt`. Ou seja, execute, no ambiente escolhido, a instalação através do comando: 
```
pip install -r requirements.txt;
```
3. Para executar a API: 
```
flask run --host 0.0.0.0 --port 5000
```

Recomendá-se utilizar o comando abaixo, quando em modo de desenvolvimento:
```
flask run --host 0.0.0.0 --port 5000 --reload
```
Desta forma o servidor é reinicia automaticamente após mudanças no código fonte.


4. Acesse o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador de preferência para verificar a API em execução.

Posteriormente, basta testar quaisquer rotas da API que desejar para gerenciar a sua Taverna virtual. Cada rota tem sua devida descrição na documentação acessada.

## Executando a Aplicação com Docker

Você pode executar a aplicação Flask com Docker para garantir um ambiente consistente e manter os dados do banco de dados SQLite persistente. Siga as etapas abaixo para configurar e executar o contêiner Docker:

1. Certifique-se de que você tenha o Docker instalado em sua máquina. Se ainda não tiver, siga as instruções de instalação [aqui](https://docs.docker.com/get-docker/).

2. Clone este repositório para sua máquina, se ainda não o fez:
```
git clone https://github.com/seu-usuario/seu-repositorio.git
```

3. Navegue para o diretório do projeto:
```
cd seu-repositorio
```

4. Construa a imagem Docker usando o Dockerfile fornecido:
```
docker build -t nome_da_imagem .
```

5. Execute o contêiner Docker como administrador, mapeando a porta 5000 para o host e configurando um volume para persistir os dados do banco de dados:
```
docker run -p 5000:5000 -v $(pwd):/app nome_da_imagem

docker run -p 5000:5000 -v C:\seu-diretorio:/app backend
```

Agora, sua aplicação Flask deve estar em execução no contêiner Docker e acessível em http://127.0.0.1:5000 em seu navegador. Os dados do banco de dados SQLite serão persistentes e não serão perdidos entre as execuções do contêiner.

Lembre-se de que você pode personalizar o nome da imagem Docker (nome_da_imagem) e o caminho do banco de dados no seu código Flask, conforme necessário, para corresponder à estrutura do seu projeto.

Para encerrar a execução do contêiner, você pode pressionar Ctrl+C no terminal onde o contêiner está sendo executado.

Certifique-se de substituir `seu-usuario/seu-repositorio` pelo URL real do seu repositório GitHub e fazer quaisquer outras personalizações necessárias para refletir a estrutura e configuração do seu projeto.