#!/bin/bash
cd /home/cooiky/backup
now=$(date +"%Y-%m-%d_%H:%M:%S")
file=cooiky_databasename_$now.sql.gz
mysqldump -u databaseusername -pdatabasepassword databasename | gzip > $file #-p与密码间无空格
