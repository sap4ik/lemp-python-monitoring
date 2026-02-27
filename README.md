# LEMP Python Monitoring Project
![Python](https://img.shields.io/badge/Python-3.12-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-lightgrey)
![Prometheus](https://img.shields.io/badge/Prometheus-2.52-orange)
![Grafana](https://img.shields.io/badge/Grafana-10.2-brightgreen)
![License](https://img.shields.io/badge/License-MIT-green)


# О проекте
Полноценный production-ready стек для мониторинга Linux-сервера и Python-приложения. Проект развёрнут с нуля на виртуальной машине и включает в себя:

- Веб-приложение на **Flask** + **Gunicorn**
- Веб-сервер **Nginx** (reverse proxy)
- База данных **MySQL** с подключением из Python
- Мониторинг сервера: **Prometheus** + **Node Exporter** + **Grafana**
- Автоматические алерты в **Telegram** через **Alertmanager**
- Скрипты автоматизации деплоя и проверки здоровья
- Система резервного копирования (бэкапы БД и конфигов)


# Функциональность
# Мониторинг (Prometheus + Grafana)
- Метрики сервера: CPU, RAM, Disk, Network (Node Exporter)
- Метрики Python-приложения: количество запросов, время ответа, ошибки
- Дашборд **Node Exporter Full (ID 1860)** + кастомные панели


# Алерты (Alertmanager + Telegram)
- Мгновенные уведомления при падении приложения или перегрузке CPU
- Автоматическое уведомление о восстановлении


# Логирование (Logrotate)
- Ротация логов Python-приложения (ежедневно, хранение 7 дней)


# Автоматизация (Bash-скрипты)
- `deploy.sh` — обновление кода, бэкап БД, перезапуск
- `health_check.sh` — проверка сервисов, автоперезапуск
- `system_backup.sh` — полное резервное копирование (ежедневное/еженедельное)


# Стек технологий
| Компонент | Технология |
|-----------|------------|
| ОС | Ubuntu 22.04 LTS |
| Веб-сервер | Nginx |
| Бэкенд | Python 3.12 + Flask + Gunicorn |
| База данных | MySQL / MariaDB |
| Мониторинг | Prometheus, Node Exporter, Grafana |
| Алерты | Alertmanager, Telegram Bot |
| Автоматизация | Bash, systemd, cron, logrotate |


# Структура проекта
lemp-python-monitoring/
├── .gitignore
├── README.md
├── app.py
├── requirements.txt
├── scripts/
│   ├── deploy.sh
│   ├── health_check.sh
│   └── system_backup.sh
├── config/
│   ├── nginx.conf
│   ├── prometheus.yml
│   ├── alertmanager.yml
│   └── alert_rules.yml
└── screenshots/
    ├── grafana-dashboard.png
    └── telegram-alert.png



# Быстрый старт
1. *Клонировать репозиторий*
   ```bash
   git clone https://github.com/sap4ik/lemp-python-monitoring.git
   cd lemp-python-monitoring
   ```

2. *Настроить виртуальное окружение*
   ```bash 
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. *Запустить через Gunicorn*
   ```bash
   gunicorn -w 4 -b 127.0.0.1:8000 app:app
   ```
4. *Настроить Nginx - (см. config/nginx.conf)*

5. *Запустить мониторинг: Prometheus, Node Exporter, Grafana - systemd юниты* 
   ```bash
   sudo systemctl start prometheus node_exporter grafana-server
   ```

# Promql-запросы 
   ```promql
   # Загрузка CPU
   100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
   
   # Использование памяти
   (node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / 1024 / 1024
   
   # Сетевой трафик
   rate(node_network_receive_bytes_total{device!="lo"}[5m])

   # Запросы к Python-приложению 
   rate(flask_http_request_total[5m])


# Тестирование алертов
   ```bash
   # Остановить приложение
   sudo systemctl stop python-app

   # Через 1 минуту должно прийти уведомление в Telegram
   # Запустить обратно
   sudo systemctl start python-app

   # Придёт уведомление о восстановлении


# Полезные команды
   ```bash
   # Статусы сервисов
   sudo systemctl status prometheus
   sudo systemctl status grafana-server
   sudo systemctl status alertmanager
   sudo systemctl status python-app

   # Логи
   sudo journalctl -u prometheus -f
   sudo tail -f /var/log/nginx/error.log

   # Бэкапы
   ls -la /backups/daily/


# Контакты
- *GitHub*: @sap4ik(https://github.com/sap4ik)
- *Telegram*: @Ssssssssssap (https://t.me/Ssssssssssap)

# Лицензия
MIT License. Подробнее в файле [LICENSE](LICENSE).






