# ZABCOMBAIN #
## About
This program helps you to generate reports, and adds the results of the ping command.
For example, we get such a results:

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

## Dependences
* Python >=3
* Tested against Zabbix 1.8 through 3.4
* Python3-dev packages for linux

## Dependent packages in pip
* pyzabbix - automatically installs
* wxPython - can be manually set

For Windows and MacOS
> To install wxPython, type the command:
```
pip install -U wxPython
```

For Linux
> To install wxPython, type the command:
```
pip install -U \
    -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/(osname) \
    wxPython
```
Instead (osname) you should choose from:
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
>More can be read here:
https://wxpython.org/pages/downloads/


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
