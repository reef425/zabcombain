# ZABCOMBAIN #
## О программе
Эта программа помогает формировать отчеты, и добавляет результаты работы комнады пинг.
Например получаем такой вывод:

```
name     :Z. server
hostname :Z. server
issue    :Disk I/O is overloaded on Z. server
agetime  :4d 1h 18m
PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data.
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.309 ms
64 bytes from 127.0.0.1: icmp_seq=2 ttl=64 time=0.281 ms
64 bytes from 127.0.0.1: icmp_seq=3 ttl=64 time=0.173 ms

--- 127.0.0.1 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 1999ms
rtt min/avg/max/mdev = 0.173/0.254/0.309/0.060 ms
```

pypi version 1.0.2

## Зависимости
* Python >=3
* Tested against Zabbix 1.8 through 3.4
* Пакты python3-dev для linux

## Зависимые пакеты в pip
* pyzabbix - устанавливается автоматически
* wxPython - устанавливается вручную

Для Windows и MacOS
> Что бы установить wxPython, наберите команду:
```
pip install -U wxPython
```

Для  Linux

> Что бы установить wxPython, наберите команду:
```
pip install -U \
    -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/(osname) \
    wxPython
```
Вместо (osname) надо выбрать из:
>* centos-7
>* debian-8
>* debian-9
>* fedora-23
>* fedora-24
>* fedora-26
>* fedora-27
>* ubuntu-14.04
>* ubuntu-16.04  
>
>
>Подробнее можно почитать здесь: https://wxpython.org/pages/downloads/

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
LGPL 2.1   http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html

Zabbix API Python Library.

Original Ruby Library is Copyright (C) 2009 Andrew Nelson nelsonab(at)red-tux(dot)net

Original Python Library is Copyright (C) 2009 Brett Lentz brett.lentz(at)gmail(dot)com

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
