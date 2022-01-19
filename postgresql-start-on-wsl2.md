How to start Postgres service?
===

Methods to start postgresql:
1. ```sudo pg_ctlcluster 12 main start```
2. ```sudo service postgresql start```

Writing a simple Shell Script
---
Edit ```.bashrc``` file located in ```/home/<username>/``` and write some lines of code:
```
if ! pgrep -x "postgres" >/dev/null; then
    sudo pg_ctlcluster 13 main start
    echo "postgres service started using: sudo pg_ctlcluster 13 main start"
fi
```
Note: change version of postgresql

We are going to create a file in sudoers.d since we don’t want to modify it with the operating system file. This will prevent any issue if the operating system needs to update the actual sudoers file in the event of upgrades. First, we need to create a file where will put the filename as skip_sudo_pg.

```
$ sudo visudo -f /etc/sudoers.d/skip_sudo_pg
```
Then, the content of the file
```
%sudo   ALL=(ALL) NOPASSWD:/usr/bin/pg_ctlcluster
```
To test the result, from your terminal:
```
exit
wsl --shutdown
```
Restart ```wsl```
```
wsl
```

Thank you for reading this article.