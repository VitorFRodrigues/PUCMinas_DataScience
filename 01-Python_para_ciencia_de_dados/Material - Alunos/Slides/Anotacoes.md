# Passos para criar máquina virtual

1. Instalar Python na máquina
 
2. criar pasta VIRTUALENVS e abrir ela no cmd

3. Instalar virtual env na máquina
```
pip install virtualenv
```
 
4. Dentro de uma pasta, criar uma virtual env exemplo: 
```
virtualenv -p python3 pucminas
```
 
5. Para acessar a virtual env criada dentro da pasta em que estão os envs principal digite
```
pucminas\scripts\activate
```
 
6. Para ver as bibliotecas instaladas digite o comando:
```
pip list
```
 
7. Para instalar uma biblioteca digite: no caso (“ipykernel”) é uma biblioteca
 
```
pip install ipykernel
```
 
8. Identificando e ativando a virtual env no sistema
 
```
python -m ipykernel install –-user –-name=pucminas
```
