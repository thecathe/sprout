# sprout
repo for containing stuff as i figure out linux




## manjaro setup steps
```sudo pacman -Syy```
```sudo pacman -S lightdm awesome xorg-server xterm kitty nvim```
### light dm
```sudo nano /etc/lightdm/lightdm.conf```
edit:
```autologin-user=
autologin-session=awesome
```

### autologin
```sudo groupadd -r autologin```
```sudo gpasswd -a cathe autologin```
```systemctl enable lightdm.service```


### awesome defaults
```mkdir ~/.config/awesome```
```cp /etc/xdg/awesome/rc.lua ~/.config/awesome```
edit: (todo)
```terminal = "kitty"
editor = nvim
```


```sudo reboot```


