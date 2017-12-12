# Projeto para o Trabalho de Graduação em Engenharia de Computação

Projeto de robô seguidor de linha utilizando visão computacional (OpenCV) e redes neurais (Keras + TensorFlow) embarcados em Raspberry Pi 3

### Conteúdo das pastas

- <b>controller_arduino</b>: código para ser executado no Arduino

- <b>controller_raspberry</b>: códigos para serem executados na Raspberry Pi

- <b>controller_server</b>: códigos para serem executados no Servidor

- <b>ProjetoProteus</b>: arquivos do projeto no Proteus para confecção da PCB (CI L293D)

### Passos de execução

1. Carregue o arquivo communicationArduino.ino na placa Arduino

2. Salve os arquivos da pasta controller_raspberry na placa Raspberry Pi e execute o script communicationRaspberry.py

3. Salve os arquivos da pasta controller_server no computador Servidor e execute o script communicationServer.py

### Requisitos de instalação

Arduino:
  - Biblioteca IRemote.h

Raspberry Pi e Servidor:
  - OpenCV
  - Keras + Tensorflow
  - Numpy
  - Scikit-learn