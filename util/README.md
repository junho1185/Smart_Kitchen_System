# Raspberry Pi initial Setting

## git installation

``` 
sudo apt update && sudo apt upgrade
```
```
sudo apt install git
```

## Create SSH Key
```
ssh-keygen -t rsa -b 4096
```
Just press enters afterwards.

View the generated SSH key by the following command.
```
cat /home/pi/.ssh/id_rsa.pub
```

## Clone Repository
Clone this repository.

## Install necesarry libraries
```
pip install -r requirements.txt
```

## Set Default Display

## Disable Double Touch behavior
Modify [input] section in `~/.kivy/config.ini` 
```
[input]
%(name)s = probesysfs,provider=hidinput
mouse = mouse
# mtdev_%(name)s = probesysfs,provider=mtdev 
hid_%(name)s = probesysfs,provider=hidinput
```
