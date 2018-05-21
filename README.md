# ZABCOMBAIN #
## About
This program helps you to generate reports, and adds the results of the ping command.
For example, we get such a results:

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
pypi version 2.0.1

## Dependences
* Python >=3
* Tested against Zabbix 1.8 through 3.4
* Python3-dev packages for linux

## Dependent packages in pip
* pyzabbix - automatically installs
* PyQt5 - can be manually set

For Linux, Windows and MacOS
> To install PyQt5, type the command:
```
pip install PyQt5
or
pip install -r requirements.txt
```

## Documentation ##
### Getting Started

* Download the `zip` file and unzip it. Go to the file folder `setup.py`.
* Or use `git` to clone the ** zabcombain** project. Go to the folder with the file `setup.py`.

In the console
```
$ python3 setup.py install
```
Run util:
```
$ zabcombain
```
#### Main page:
> * To connect to the server, you need to ***'settings'*** specify the server address.
> * Then enter the username and password to work.
> * After a successful connection, is displayed in the console ***connect***

#### Oreder page:
> * To generate the event data, copy data from ***dashboard - action***.

```
Z. server Disk I/O is overloaded on server Z. No 3d 23h 13m
```
> * Click ***'paste'*** to paste the data.
> * Click ***'proccess'*** that the data started to be processed.
> * Click ***'copy'*** to copy the processed data.
> * The Tick ***'Contin.'*** , allows to clear the fields of the input/output.

#### The Ping page

> * Click ***'update'*** .
> * Select ***'host group'*** .
> * Select ***'hosts'*** .
> * Click ***'ping'*** .
> * The program ping all interfaces on the host, the results are displayed in the console.


## License ##
GPL v.3
http://www.gnu.org/licenses/gpl-3.0.html
