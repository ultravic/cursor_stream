# Servidor/Client UDP/IP: Stream de eventos do mouse
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

A apresentação do *log* depende do nível definido no **settings.py**. Os *logs* são produzidos utilizando a biblioteca *logging*, dessa forma, os niveis de mensagens são: *DEBUG* - apresentará as informações de inicializações, finalizações, erros e pacotes perdidos e fora de ordem, eventos do mouse; *INFO* - apresentará as informações de inicializações, finalizações, erros e pacotes perdidos e fora de ordem; *CRITICAL* - apresentará as informações de erros e pacotes perdidos e fora de ordem; e *ERROR*.

### Servidor
O servidor está implementado no arquivo **server.py**. Para saber como executar o servidor na linha de comando, basta digitar:
> $ python3 server.py --help
Esse comando apresentará as opções para utilização e os seus significados.
> $ python3 <server> [[-p <port>], [-t <ttl>], [-g <group>], [-i <seconds>]]
O servidor possui em **settings.py** as variáveis padrão para cada opção, dessa forma, basta executar somente o arquvio servidor. As opções do terminal são: *port* - a porta a ser utilizada; *ttl* - time to live dos pacotes; *group* - endereço de grupo para multicast; *seconds* - tempo entre envio dos pacotes. 

### Cliente
O cliente está implementado no arquivo **client.py**

## Testes
### Teste com um cliente

### Teste com 3 clientes simultâneos

### Teste com tempo de envido de 3 segundos

# Conclusão
