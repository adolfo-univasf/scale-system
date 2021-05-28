# scale-system


1°  Ir na pasta sd onde a maquina que roda o vagrant está

2°  Dar um git clone do projeto em uma pasta "resources" dentro da pasta "sd" 

3°  Voltar para a pasta sd  e abrir o terminal

4°  executar o comando para iniciar o vagrant : vagrant up

5°  executar o comando: vagrant ssh

6°  cd /vagrant/resources

7°  cd scale-system/

8°  Instalar as  dependências necessárias utilizando o comando:    pip install -r requirements.txt

9°  Digitar o comando:    python manage.py runserver 0:8000

10° Abrir o navegador e digitar: 192.168.200.11:8000

**
Caso de erro vá até a pasta scalesystem dentro da scale-system  e abra o arquivo settings.py e adicione o ip que está configurado no Vagrant