import sqlite3
from datetime import datetime
import config


def init_db():
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS services
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       name
                       TEXT
                       NOT
                       NULL,
                       category
                       TEXT,
                       price
                       REAL
                   )
                   ''')

    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS requests
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       user_id
                       INTEGER,
                       user_name
                       TEXT,
                       service_id
                       INTEGER,
                       status
                       TEXT
                       DEFAULT
                       'Новая',
                       created_at
                       TEXT,
                       FOREIGN
                       KEY
                   (
                       service_id
                   ) REFERENCES services
                   (
                       id
                   )
                       )
                   ''')

    cursor.execute("SELECT COUNT(*) FROM services")
    if cursor.fetchone()[0] == 0:
        test_services = [
            ('IT-Консалтинг', 'Консультации', 50000),
            ('Внедрение CRM', 'Интеграция', 150000),
            ('Техническая поддержка', 'Сопровождение', 30000),
            ('Аудит безопасности', 'Аудит', 80000)
        ]
        cursor.executemany("INSERT INTO services (name, category, price) VALUES (?, ?, ?)", test_services)

    conn.commit()
    conn.close()


def get_services():
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, category, price FROM services")
    services = cursor.fetchall()
    conn.close()
    return services


def create_request(user_id, user_name, service_id):
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute('''
                   INSERT INTO requests (user_id, user_name, service_id, status, created_at)
                   VALUES (?, ?, ?, ?, ?)
                   ''', (user_id, user_name, service_id, 'Новая', now))

    req_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return req_id


def get_user_requests(user_id):
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
                   SELECT r.id, s.name, r.status, r.created_at
                   FROM requests r
                            JOIN services s ON r.service_id = s.id
                   WHERE r.user_id = ?
                   ORDER BY r.created_at DESC LIMIT 5
                   ''', (user_id,))
    requests = cursor.fetchall()
    conn.close()
    return requests


def get_all_requests():
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
                   SELECT r.id, r.user_name, s.name, r.status, r.created_at
                   FROM requests r
                            JOIN services s ON r.service_id = s.id
                   ORDER BY r.created_at DESC
                   ''')
    requests = cursor.fetchall()
    conn.close()
    return requests