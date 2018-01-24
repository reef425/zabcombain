# ZABCOMBAIN #

pypi version 1.0.0

## Requirements
* Python >=3
* Tested against Zabbix 1.8 through 3.4
* wxPython python library  
Download: https://wxpython.org/pages/downloads/

## Documentation ##
### Getting Started

Download the zip file, or `git clone` the project **zabcombain**.
Navigate to the project folder.

In the console
```bash
$ pip setup.py install
```
Run util:
```bash
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
> * The Tick ***'Contin.'***, allows to clear the fields of the input/output.

#### The Ping page

> * Click ***'update'***.
> * Select ***'host group'***.
> * Select ***'hosts'***.
> * Click ***'ping'***.
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
