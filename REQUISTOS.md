# Requisitos TP1:

- Implementar um client TCP para fazer requisições de arquivos ao servidor; [FEITO]

  - O client deve estabelecer conexão com o servidor; [FEITO]

  - o client pode enviar o comando "list" e assim receber uma lista de todos os arquivos presentes na cache do servidor; [FEITO]

  - Em seguida enviar o nome do arquivo requerido; [FEITO]

  - O client então recebe o arquivo retornado pelo servidor; [FEITO]

- Implementar um servidor TCP multithread que serve arquivos; [FEITO]

  - O servidor então busca primeiramente numa memória cache pelo arquivo e o enviar se encontrar; [FEITO]

  - O servidor deve possuir uma função que retorne ao cliente uma lista contendo os nome dos arquivos no cache do servidor; [FEITO]

  - O padrão da linha de comando a ser seguido deve ser: **./tcp_client server_host server_port list**[FEITO]

  - Não encontrado o arquivo, o servidor busca então em uma determinada pasta e retorna o arquivo se encontrado; [FEITO]

  - Não encontrado em nenhum dos casos o servidor retorna uma mensagem de "File not found";[FEITO]

  - Se o arquivo for encontrado ele é retornado ao cliente pela mesma conexão e colocado em cache caso não esteja; [FEITO]

  - A memória cache deve ter no máximo 64MB. Se o arquivo é maior que 64MB, ele não deve ser inserido na memória cache; [FEITO]

  - Se o tamanho da memória for exceder 64MB ao inserir o arquivo na memória, o programador deve abrir espaço na memória cache para que o arquivo possa ser inserido sem exceder os 64MB; IMPORTANTE QUE A MEMÓRIA CACHE NUNCA ULTRAPASSE 64MB! [FEITO]
