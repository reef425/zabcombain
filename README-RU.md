# ZABCOMBAIN #
## О программе
Эта программа помогает формировать отчеты, и добавляет результаты работы комнады пинг.
Например получаем такой вывод:

```
name     :Zabbix server
hostname :Zabbix server

ZABBIX PING RESULT

PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data.
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.000 ms
64 bytes from 127.0.0.1: icmp_seq=2 ttl=64 time=0.774 ms
64 bytes from 127.0.0.1: icmp_seq=3 ttl=64 time=0.783 ms

--- 127.0.0.1 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2002ms
rtt min/avg/max/mdev = 0.000/0.519/0.783/0.367 ms

INTERFACES PING RESULT

PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data.
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.052 ms
64 bytes from 127.0.0.1: icmp_seq=2 ttl=64 time=0.078 ms
64 bytes from 127.0.0.1: icmp_seq=3 ttl=64 time=0.040 ms

--- 127.0.0.1 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2025ms
rtt min/avg/max/mdev = 0.040/0.056/0.078/0.018 ms
```

Zabcombain предпросмотр
![alt text][logo]

[logo]: https://github.com/reef425/zabcombain/blob/master/img/zabcombain-preview.gif "Главное окно"

pypi version 2.0.3

## Зависимости
* Python >=3
* Tested against Zabbix 1.8 through 3.4
* Пакты python3-dev для linux

## Зависимые пакеты в pip
* pyzabbix - устанавливается автоматически
* PyQt5 - устанавливается вручную

Для Linux, Windows и MacOS
> Что бы установить PyQt5, наберите команду:
```
pip install PyQt5
or
pip install -r requirements.txt
```
`

## Документация ##
### Начало работы

* Скачайте `zip` файл, разархивируйте его. Перейдите в папку с файлом `setup.py`.
* Или с помощью утилиты`git` клонируйте проект  **zabcombain**. Перейдите в папку с файлом setup.py.

В консоли наберите:
```
$ python3 setup.py install
```
Запуск программы:
```
$ zabcombain
```
#### Main page:
> * Для подключения к серверу необходимо в ***'settings'*** указать адрес сервера.
> * Далее ввести логин и пароль для работы.
> * После успешного подключения в консоль выводится ***connect***.

#### Oreder page:
> * Что бы сформировать данные о событии скопируйте данные из ***dashboard - action*** .

```
Z. server	Disk I/O is overloaded on Z. server	3d 23h 13m		No
```

> * Нажмите ***'paste'*** , чтобы вставить скопированные данные.
> * Нажмите ***'proccess'*** , чтобы данные начали обрабатываться.
> * Нажмите ***'copy'*** , чтобы скопировать обработанные данные.
> * Галочка ***'Contin.'*** , позволяет не очищать поля ввода/вывода.



#### Ping page

> * Нажмите ***'update'*** .
> * Выберите ***'host group'*** .
> * Выберите ***'hosts'*** .
> * Нажмите ***'ping'*** .
> * Программа пропингует все интерфейсы хоста, результаты выводит в консоль.


## License ##
GPL v.3
http://www.gnu.org/licenses/gpl-3.0.html
