BackupPC push to Influxdb
===

[![langage](https://img.shields.io/badge/Langage-Python-purple.svg)](https://python.org/)
[![pg3.io](https://img.shields.io/badge/made%20by-PG3-orange.svg)](https://twitter.com/pg3io/)
[![Apache 2.0 Licence](https://img.shields.io/hexpm/l/plug.svg)](LICENCE)

Script status backuppc jobs to influxdb.

# Dependences
* Install ``requirements.txt``
```
pip3 install -r requirements.txt
```

# Settings script
* Move files ``notify.py`` and ``config.py`` in ``/usr/local/share/``
* write influxdb access
```
INFLUXDB_USER="influxdb username"
INFLUXDB_PASSWORD="influxdb password"
INFLUXDB_HOSTNAME="influxdb hostname"
INFLUXDB_PORT="influxdb port"
DATABASE_NAME="database name"
```

# Settings BackupPC
Add in BackupPC ***Edit config > Backup Settings***

In ``DumpPreUserCmd`` and ``DumpPostUserCmd``
```
/usr/local/share/notify.py --xferok $xferOK --host $host --type $type --client $client --user $user --moreusers $moreUsers --hostip $hostIP --share $share --xfermethod $XferMethod --sshpath $sshPath --cmdtype $cmdType
```

# License
Licence projet [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0) for details [LICENSE](LICENSE).

# Informations sur l'auteur
This project was created by [PG3](https://pg3.io) in January 2021.
