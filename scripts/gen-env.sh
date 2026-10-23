#!/usr/bin/env bash
set -e
[ -f .env ] && { echo ".env đã tồn tại, không ghi đè"; exit 1; }
rand() { openssl rand -hex 16; }
cat > .env <<EOF
POSTGRES_DB=clinic
POSTGRES_USER=clinic_admin
POSTGRES_PASSWORD=$(rand)
APP_DB_USER=app_user
APP_DB_PASSWORD=$(rand)
EXPORTER_DB_PASSWORD=$(rand)
PGADMIN_DEFAULT_EMAIL=admin@phongkham.vn
PGADMIN_DEFAULT_PASSWORD=$(rand)
GRAFANA_ADMIN_PASSWORD=$(rand)
EOF
chmod 600 .env
echo "Đã tạo .env"
