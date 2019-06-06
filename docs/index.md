# Servidor/Client UDP/IP: Stream de eventos de mouse
Os programas aqui discutidos implementam um sistema de servidor e de cliente *UDP/IP* multicast para um stream de eventos do mouse. Os eventos trabalhados são o da posição do mouse, pressionar e soltar o botão esquerdo e a rolagem. O objetivo final é criar um mapa de calor para cada tipo de evento para analisar essa transmissão.

## Requisitos
Os requisitos para a execução dos códigos são as bibliotecas:
- PyAutoGUI
- xlib
- pynput
- numpy
- matplotlib
- scipy
- logging

É possível fazer a instalação dessas bibliotecas utilizando o pip da forma:
> $ pip3 install -r requirements.txt

## Funcionamento
### Configurações
Os programas possuem um arquivo de configurações chamado **settings.py**. Nesse arquivo é
possível definir porta, grupo e ttl padrão, como também o tempo de transmissão dos pacotes. Também define-se os arquivos em que serão salvos os *logs* do servidor e do cliente e os arquivos dos gráficos dos mapas de calor. Por fim, também são definidos 
os tipos de mensagens de ajuda, o padrão da mensagem dos *logs* e o nível da mensagem dos
logs a serem apresentadas.

A presentação do *log* depende do nível definido no **settings.py**. Os *logs* são produzidos utilizando a biblioteca *logging*, dessa forma, os niveis de mensagens são: DEBUG - apresentará as informações de inicializações, finalizações, erros e pacotes perdidos e fora de ordem, eventos do mouse; INFO - apresentará as informações de inicializações, finalizações, erros e pacotes perdidos e fora de ordem; CRITICAL - apresentará as informações de erros e pacotes perdidos e fora de ordem; e ERRO.

### Servidor
O servidor está implementado no arquivo **server.py**

### Cliente
O cliente está implementado no arquivo **client.py**

## Testes
### Teste com um cliente

### Teste com 3 clientes simultâneos

### Teste com tempo de envido de 3 segundos

# Conclusão
