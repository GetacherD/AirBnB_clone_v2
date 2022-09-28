#!/usr/bin/env bash
#setup new server
# check for nginx installation, install if not installed
if ! nginx -v &>/dev/null ;
then
        apt-get -y update
        apt-get install -y nginx
fi

# create required folder and index file
#create /data folder
if [ ! -d /data/ ];
then
        mkdir /data
fi

#create subfolders
if [ ! -d /data/web_static/ ];
then
        mkdir -p /data/wed_static/
fi

if [ ! -d /data/web_static/releases/ ];
then
        mkdir -p /data/web_static/releases/
fi
if [ ! -d /data/web_static/shared/ ];
then
        mkdir -p /data/web_static/shared/
fi
if [ ! -d /data/web_static/releases/test/ ]
then
        mkdir -p /data/web_static/releases/test/
fi
if [ ! -d /data/web_static/current/ ];
then
        mkdir -p /data/web_static/current/
fi
ln -sf /data/web_static/releases/test/ /data/web_static/current/
chown -R ubuntu /data/
chgrp -R ubuntu /data/
# update nginx configuration

# check alias first
# check if /etc/nginx/conf.d/default.conf
if [ -f /etc/nginx/conf.d/default.conf ];
then
        server=0
        duplicate=0
        exists=0
        while IFS= read -r line;
        do
                if [[ "$line" =~ \ *location\ /hbnb_static* ]];
                then
                        exists=1
                fi
        done </etc/nginx/conf.d/default.conf
        if [ "$exists" == 0 ]
        then
                touch backup.conf
                printf  "">backup.conf
                while IFS=  read -r line;
                do
                        if [[ "$line" =~ ^server* ]];
                        then
                                server=1

                        fi
                        if [[ "$line" =~  \ *location* ]]
                        then
                                if [ "$server" == 1 ]
                                then
                                        if [ "$duplicate" == 0 ]
                                        then
                                                printf "\
        location /hbnb_static {
                alias /data/web_static/current/;
                }\n">>backup.conf
                                        duplicate=1
                                        fi
                                fi
                        fi
                        echo "$line" >> backup.conf
                done </etc/nginx/conf.d/default.conf
                truncate -s 0 /etc/nginx/conf.d/default.conf
                cat backup.conf >> /etc/nginx/conf.d/default.conf
        fi
fi
# update nginx configuration
# check alias first and file /etc/nginx/sites-available/default.conf
if [ -f /etc/nginx/sites-available/default.conf ];
then
        server=0
        duplicate=0
        exists=0
        while IFS= read -r line;
        do
                if [[ "$line" =~ \ *location\ /hbnb_static* ]];
                then
                        exists=1
                fi
        done </etc/nginx/sites-available/default.conf
        if [ "$exists" == 0 ]
        then
                touch backup.conf
                printf  "">backup.conf
                while IFS=  read -r line;
                do
                        if [[ "$line" =~ ^server* ]];
                        then
                                server=1

                        fi
                        if [[ "$line" =~  \ *location* ]]
                        then
                                if [ "$server" == 1 ]
                                then
                                        if [ "$duplicate" == 0 ]
                                        then
                                                printf "\
        location /hbnb_static {
                alias /data/web_static/current/;
                }\n">>backup.conf
                                        duplicate=1
                                        fi
                                fi
                        fi
                        echo "$line" >> backup.conf
                done </etc/nginx/sites-available/default.conf
                truncate -s 0 /etc/nginx/sites-available/default.conf
                cat backup.conf >> /etc/nginx/sites-available/default.conf
        fi
fi
