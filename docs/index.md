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

`pip3 install -r requirements.txt`

## Configurações

[**implementação**](settings.py.md)

Os programas possuem um arquivo de configurações chamado [settings.py](https://github.com/ultravic/cursor_stream/blob/master/settings.py). Nesse arquivo é possível definir porta, grupo e ttl padrão, como também o tempo de transmissão dos datagramas. Também define-se os arquivos em que serão salvos os *logs* do servidor e do cliente e os arquivos dos gráficos dos mapas de calor. Por fim, também são definidos os tipos de mensagens de ajuda, o padrão da mensagem dos *logs* e o nível da mensagem dos logs a serem apresentadas.

A apresentação do *log* depende do nível definido no *settings*. Os *logs* são produzidos utilizando a biblioteca *logging*, dessa forma, os niveis de mensagens são: *DEBUG* - apresentará as informações de inicializações, finalizações, erros e datagramas perdidos e fora de ordem, eventos do mouse; *INFO* - apresentará as informações de inicializações, finalizações, erros e datagramas perdidos e fora de ordem; *CRITICAL* - apresentará as informações de erros e datagramas perdidos e fora de ordem; e *ERROR*.

## Execuções
### Servidor
O servidor está implementado no arquivo [server.py](https://github.com/ultravic/cursor_stream/blob/master/server.py). Para saber como executar o servidor na linha de comando, basta digitar:

`python3 server.py --help`

Esse comando apresentará as opções para utilização e os seus significados.

`server [[-p <port>], [-t <ttl>], [-g <group>], [-i <seconds>]]`

O servidor possui em *settings* as variáveis padrão para cada opção, dessa forma, basta executar somente o arquivo servidor. As opções do terminal são: *port* - a porta a ser utilizada; *ttl* - time to live dos datagramas; *group* - endereço de grupo para multicast; *seconds* - tempo entre envio dos datagramas.

Para finalizar o servidor, *Ctrl + C*.

### Cliente
O cliente está implementado no arquivo [client.py](https://github.com/ultravic/cursor_stream/blob/master/client.py). Para saber como executar o cliente na linha de comando, basta digitar:

`python3 client.py --help`

Esse comando apresentará as opções para utilização e os seus significados.

`<client> -h <server_name> [[-p <port>], [-g <group>], [-simage]]`

O cliente possui em *settings* as variáveis padrão para cada opção, exceto o nome do servidor à conectar e a opção de salvar imagem. Assim, uma execução do cliente deve possuir a opção *-h* e o nome do servidor. A opção *-simage* serve para salvar as imagens dos gráficos resultantes, sem essa opção, os gráficos são apresentados na tela.

Para finalizar o cliente, *Ctrl + C*.

## Funcionamento
### Servidor

[**implementação**](server.py.md)

O servidor faz inicialmente a verificação dos campos de opções caso seja necessário atualizar as variáveis padrão. Com isso, é criado um *socket* a partir da função *connection*. Esse *socket* é criado com o protocolo *UDP* e com a opção *multicast*. Após isso, é iniciado uma *thread* que ficará recebendo eventos do mouse. A *thread* atualizará a estrutura *data*, que contém as informações dos eventos que serão enviados em cada pacote pelo socket.

```python
data = {
    'id'    : 1,
    'mouse_position' : (0,0),
    'mouse_pressed' : False,
    'mouse_scrolled' : (False, ''),
    'screen_size' : (0, 0),
}
```

Com a variável *data* atualizada, o *socket* então envia o pacote para o grupo e porta definidos. Essas operações repetem-se a cada intervalo de tempo (definido em *settings* ou passado como parâmetro) até o servidor finalizar.

### Cliente

[**implementação**](client.py.md)

O cliente faz as verificações de opções, assim como o servidor, para atualizar possíveis variáveis. A conexão é criada na função *connection*, criando um *socket* *UDP* e vinculando-o ao grupo e porta definidos. Com isso, o cliente ficará esperando para receber o primeiro pacote. Esse pacote atualizará algumas variáveis utilitárias, escreverá possíveis mensagens de *log* e será guardado em um vetor de todos os datagramas. O próximo passo é um laço que fará as mesmas instruções de anteriormente, porém, verificará por datagramas perdidos e fora de ordem com um sistema de janela. Após a finalização do cliente, será feito as operações finais. Essas operações consistem em criar os gráficos com os dados recebidos para cada tipo de evento utilizando as bibliotecas *numpy* e *matplotlib*.

# Conclusão
Após realizarmos alguns testes, chegamos a conclusão que o UDP se mostra bem consistente com transmissão entre hosts da mesma rede, ocorrendo poucos datagramas, e não mostrando em nenhum momento datagramas fora de ordem.

Para os fins da aplicação (geração de heatmaps) os resultados sairam como o esperado.


# Testes
[Clique aqui para ir para os testes](tests.md)
