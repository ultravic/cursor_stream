# Testes
Os testes abaixo foram realizados no laboratório 1-2 do departamento de informática da UFPR em 4 máquinas diferentes.
O servidor foi a máquina h17 em todos os testes.


## Teste 1 -  1 cliente
Esse é um teste simples, apenas para demonstrar o funcionamento do sistema.
O servidor inicia e logo depois o cliente inicia ocorre cerca de 1m30s de streaming.
Não ocorreram perdas.


### Logs
Os demais logs dos testes seguem um padrão parecido. 
Para fins de demonstração exibiremos os logs destes testes aqui. 
Os demais terão links para os logs.

**Servidor**
```log
06-07-2019 20:08:14 [INFO]: Socket created
06-07-2019 20:08:14 [INFO]: Mouse listener started
06-07-2019 20:08:14 [INFO]: First packet sent succefuly
06-07-2019 20:09:46 [INFO]: Last packet sent id:507443
06-07-2019 20:09:46 [INFO]: Mouse listener closed
06-07-2019 20:09:46 [INFO]: Socket closed
06-07-2019 20:09:46 [INFO]: Closing server
```

**Cliente**
```log
06-07-2019 20:08:16 [INFO]: Socket created
06-07-2019 20:08:16 [INFO]: Socket connection succeeded
06-07-2019 20:08:16 [INFO]: First packet received id:9153
06-07-2019 20:09:44 [INFO]: Last packet received id:499925
06-07-2019 20:09:44 [INFO]: Number of packets received is 490773
06-07-2019 20:09:44 [INFO]: Number of packets missing is 0
06-07-2019 20:09:44 [INFO]: Number of packets out of order is 0
06-07-2019 20:09:44 [INFO]: Number of clicks received is 2
06-07-2019 20:09:44 [INFO]: Number of scrolls received is 20
06-07-2019 20:09:46 [INFO]: Socket closed
06-07-2019 20:09:46 [INFO]: Closing client

```

### Imagens
| Cursor Heatmap  | Click Heatmap | Scroll Heatmap |
| ------------- | ------------- | ------------- |
| ![Heatmap](https://ultravic.github.io/cursor_stream/tests/test_01/h18_cursor_heat.jpg) | ![Heatmap](https://ultravic.github.io/cursor_stream/tests/test_01/h18_press_heat.jpg)  | ![Heatmap](https://ultravic.github.io/cursor_stream/tests/test_01/h18_scroll_heat.jpg)  |


## Teste 2 -  3 clientes simultâneos
Este foi o cenário onde testamos por mais tempo, iniciamos a transmissão quando os 3 clientes já estavam escutando, e terminamos a transmissão pelo servidor.

Os clientes tiveram resultados similares, porém é possível perceber a perda de datagramas em quantidades e momentos distintos.

### Logs
- [Servidor](tests/test_02/server.log)
- [Cliente (h15)](tests/test_02/h15_client.log)
- [Cliente (h16)](tests/test_02/h16_client.log)
- [Cliente (h18)](tests/test_02/h18_client.log)

### Imagens
| Heatmap | Host 15 | Host 16 | Host 18 |
| :------------ | ------------- | ------------- | ------------- |
| Cursor  | ![Cursor Heatmap h15](https://ultravic.github.io/cursor_stream/tests/test_02/h15_cursor_heat.jpg) | ![Cursor Heatmap h16](https://ultravic.github.io/cursor_stream/tests/test_02/h16_cursor_heat.jpg) | ![Cursor Heatmap h18](https://ultravic.github.io/cursor_stream/tests/test_02/h18_cursor_heat.jpg) |
| Click  | ![Click Heatmap h15](https://ultravic.github.io/cursor_stream/tests/test_02/h15_press_heat.jpg) | ![Click Heatmap h16](https://ultravic.github.io/cursor_stream/tests/test_02/h16_press_heat.jpg) | ![Click Heatmap h18](https://ultravic.github.io/cursor_stream/tests/test_02/h18_press_heat.jpg) |
| Scroll | ![Scroll Heatmap h15](https://ultravic.github.io/cursor_stream/tests/test_02/h15_scroll_heat.jpg) | ![Scroll Heatmap h16](https://ultravic.github.io/cursor_stream/tests/test_02/h16_scroll_heat.jpg) | ![Scroll Heatmap h18](https://ultravic.github.io/cursor_stream/tests/test_02/h18_scroll_heat.jpg) |

## Teste 3 - Tempo de envio de 3 segundos
Um teste com envio de poucos datagramas (a cada 3 segundos).
Muita informação foi perdida (não datagramas), gerando heatmaps inconsistentes.

### Logs
- [Servidor](tests/test_03/server.log)
- [Cliente](tests/test_03/h16_client.log)

### Imagens
| Cursor Heatmap  | Click Heatmap | Scroll Heatmap |
| ------------- | ------------- | ------------- |
| ![Heatmap](https://ultravic.github.io/cursor_stream/tests/test_03/h16_cursor_heat.jpg) | ![Heatmap](https://ultravic.github.io/cursor_stream/tests/test_03/h16_press_heat.jpg)  | ![Heatmap](https://ultravic.github.io/cursor_stream/tests/test_03/h16_scroll_heat.jpg)  |


## Teste 4 - 3 sessões de envio com tempo entre datagramas variável
Nesse cénário de teste, fizemos 3 sessões de transmissão no servidor, com um cliente escutando desde o começo.
A primeira como o tempo de envio de 3 segundos, outra com o tempo padrão (0.0001 segundos) e uma terceira com 1 segundo.

O resultado do heatmap foi coerente, porém notamos um problema que acabamos por não tratar. 
Quando um servidor reinicia a transmissão, acabamos por não limpar algumas estruturas de dados, e isso acabou resultando em um problema no número de datagramas perdidos.

### Logs
- [Servidor](tests/test_04/server.log)
- [Cliente](tests/test_04/h16_client.log)

### Imagens
| Cursor Heatmap  | Click Heatmap | Scroll Heatmap |
| ------------- | ------------- | ------------- |
| ![Heatmap](https://ultravic.github.io/cursor_stream/tests/test_04/h16_cursor_heat.jpg) | ![Heatmap](https://ultravic.github.io/cursor_stream/tests/test_04/h16_press_heat.jpg)  | ![Heatmap](https://ultravic.github.io/cursor_stream/tests/test_04/h16_scroll_heat.jpg)  |



