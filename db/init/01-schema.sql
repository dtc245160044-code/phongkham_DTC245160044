CREATE TABLE doctors (
  id SERIAL PRIMARY KEY,
  full_name VARCHAR(100) NOT NULL,
  specialty VARCHAR(100) NOT NULL,
  phone VARCHAR(20)
);

CREATE TABLE patients (
  id SERIAL PRIMARY KEY,
  full_name VARCHAR(100) NOT NULL,
  birth_date DATE,
  gender VARCHAR(10),
  phone VARCHAR(20),
  address TEXT
);

CREATE TABLE appointments (
  id SERIAL PRIMARY KEY,
  patient_id INT NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
  doctor_id  INT NOT NULL REFERENCES doctors(id)  ON DELETE CASCADE,
  appointment_time TIMESTAMP NOT NULL,
  reason TEXT,
  status VARCHAR(20) NOT NULL DEFAULT 'pending'
);

INSERT INTO doctors(full_name, specialty, phone) VALUES
  ('BS. Nguyễn Văn An', 'Nội khoa', '0901000001'),
  ('BS. Trần Thị Mai', 'Nhi khoa', '0901000002'),
  ('BS. Lê Văn Hùng', 'Ngoại khoa', '0901000003');

INSERT INTO patients(full_name, birth_date, gender, phone, address) VALUES
  ('Lê Văn Cường', '1990-05-12', 'Nam', '0912000001', 'Thái Nguyên'),
  ('Phạm Thị Dung', '1985-11-30', 'Nữ', '0912000002', 'Hà Nội');

INSERT INTO appointments(patient_id, doctor_id, appointment_time, reason) VALUES
  (1, 1, '2026-11-01 09:00', 'Khám tổng quát'),
  (2, 2, '2026-11-02 14:30', 'Tái khám');
