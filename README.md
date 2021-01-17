BackupPC push to Influxdb
===

[![langage](https://img.shields.io/badge/Langage-Python-purple.svg)](https://python.org/)
[![pg3.io](https://img.shields.io/badge/made%20by-PG3-orange.svg)](https://twitter.com/pg3io/)
[![Apache 2.0 Licence](https://img.shields.io/hexpm/l/plug.svg)](LICENCE)

Script d'écriture dans Influxdb des états de *prés/post* job BackupPC.

# Dépendences
* Installation ``requirements.txt``
```
pip3 install -r requirements.txt
```

# Paramétrages
* Placer les fichiers ``notify.py`` et ``config.py`` dans ``/usr/local/share/``
* Définir la chaine de connexion à influxdb
```
INFLUXDB_USER="influxdb username"
INFLUXDB_PASSWORD="influxdb password"
INFLUXDB_HOSTNAME="influxdb hostname"
INFLUXDB_PORT="influxdb port"
DATABASE_NAME="database name"
```

# Déclaration paramétrages
Ajouter dans la consôle BackuppPC ***Edit config > Backup Settings***

Ajouter dans ``DumpPreUserCmd`` et ``DumpPostUserCmd``
```
/usr/local/share/notify.py --xferok $xferOK --host $host --type $type --client $client --hostip $hostIP --share $share --xfermethod $XferMethod --sshpath $sshPath --cmdtype $cmdType
```

