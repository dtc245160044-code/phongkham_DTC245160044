# Hệ thống Quản lý Phòng khám – Đề 8

Sinh viên: Lưu Thanh Huyền – MSSV: DTC245160044 – Lớp: KHMT K23A

## Thành phần
Flask, PostgreSQL, pgAdmin, Nginx (HTTPS tự ký + security headers).

## Yêu cầu
Ubuntu 24.04, Docker Engine + Docker Compose plugin, Git, openssl.

## Chạy hệ thống
    git clone <url-repo> && cd <thư-mục>
    ./scripts/gen-env.sh
    ./scripts/gen-cert.sh
    docker compose up -d --build

## Địa chỉ truy cập
- Web: https://localhost (chấp nhận cảnh báo chứng chỉ tự ký)
- pgAdmin: http://127.0.0.1:5050 (tài khoản trong file .env)

## Dừng / xóa
    docker compose down       # giữ dữ liệu
    docker compose down -v    # xóa cả dữ liệu
