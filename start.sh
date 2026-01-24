#!/bin/bash
set -e

echo "===================================="
echo "Starting MariaDB"
echo "===================================="

# Variables Render ou defaults
DB_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD:-rootpassword}
DB_NAME=${MYSQL_DATABASE:-digichees_db}
DB_USER=${MYSQL_USER:-tlamo123}
DB_PASSWORD=${MYSQL_PASSWORD:-Admin123!}

# Initialiser la DB si vide
if [ ! -d "/var/lib/mysql/mysql" ]; then
    echo "Initializing MariaDB..."
    mariadb-install-db --user=mysql --basedir=/usr --datadir=/var/lib/mysql
fi

# Lancer MariaDB
mariadbd-safe &
echo "Waiting for MariaDB..."
until mariadb-admin ping --silent; do
    sleep 1
done

echo "MariaDB is ready"

# Setup DB + user
mariadb -u root <<EOF
ALTER USER 'root'@'localhost' IDENTIFIED BY '${DB_ROOT_PASSWORD}';
CREATE DATABASE IF NOT EXISTS ${DB_NAME};
CREATE USER IF NOT EXISTS '${DB_USER}'@'%' IDENTIFIED BY '${DB_PASSWORD}';
GRANT ALL PRIVILEGES ON ${DB_NAME}.* TO '${DB_USER}'@'%';
FLUSH PRIVILEGES;
EOF

# Run init.sql
echo "Running init.sql..."
mariadb -u root -p${DB_ROOT_PASSWORD} ${DB_NAME} < /init.sql || true

echo "===================================="
echo "Starting FastAPI"
echo "===================================="

exec uvicorn src.main:app --host 0.0.0.0 --port 8000
