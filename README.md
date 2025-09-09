# 🛒 Procurement Automation Backend

Backend-приложение для автоматизации закупок в розничной сети на Django Rest Framework.

## 🚀 Возможности

- ✅ Управление пользователями (клиенты, поставщики, администраторы)
- ✅ Каталог товаров с характеристиками
- ✅ Корзина покупок и оформление заказов
- ✅ Импорт/экспорт товаров (YAML, Excel)
- ✅ Email уведомления (подтверждение заказов, накладные администратору)
- ✅ Восстановление пароля и верификация email через API
- ✅ REST API с документацией (Swagger)
- ✅ Асинхронные задачи (Celery + Redis)
- ✅ Docker контейнеризация

## 📋 Требования

- Python 3.10+
- PostgreSQL 13+
- Redis
- Docker и Docker Compose (опционально)

## 🛠️ Установка и запуск

1. **Клонирование и настройка**
```bash
git clone <repository-url>
cd procurement_backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt

cp .env.example .env
