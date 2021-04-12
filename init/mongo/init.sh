#!/usr/bin/env bash
echo "Creating mongo users..."
mongo admin -u root -p mongo2020 << EOF
use admin
db.createUser({user: 'chao', pwd: 'mongo2020', roles:[{role:'readWrite',db:'stock'}]})
EOF
echo "Mongo users created."