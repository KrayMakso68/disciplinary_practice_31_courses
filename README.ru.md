# Корпоративная система учёта эффективности и дисциплинарной практики персонала

<p align="center">
  <strong>Масштабируемая веб-платформа для контроля результатов работы сотрудников с рекурсивным моделированием оргструктуры предприятия</strong>
</p>

<p align="center">
  <a href="README.md"><b>English</b></a> | <a href="README.ru.md"><b>Русский</b></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Django-4.2+-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django" />
  <img src="https://img.shields.io/badge/django--mptt-Trees-green?style=for-the-badge" alt="django-mptt" />
  <img src="https://img.shields.io/badge/Bootstrap-5-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white" alt="Bootstrap 5" />
  <img src="https://img.shields.io/badge/docxtpl-Reporting-blue?style=for-the-badge" alt="docxtpl" />
  <img src="https://img.shields.io/badge/Matplotlib-Seaborn-orange?style=for-the-badge" alt="Matplotlib" />
</p>

---

## 🏢 О проекте

**Enterprise Hierarchical Workforce & Discipline Tracking System** — это production-ready веб-платформа, созданная для организаций с глубокой древовидной структурой (Центральный офис $\to$ Филиалы $\to$ Департаменты $\to$ Отделы $\to$ Рабочие группы). Платформа систематизирует фиксацию достижений и взысканий сотрудников, автоматизирует аудит дисциплины, строит динамическую аналитику и генерирует официальные сводные отчёты в формате Word (.docx).

Система решает ключевую архитектурную задачу строгого разграничения полномочий: каждый руководитель видит и администрирует исключительно своё подразделение и все вложенные дочерние команды без риска утечки данных соседних отделов.

---

## 🎥 Демонстрация работы

<p align="center">
  <img width="800" alt="Демонстрация работы системы" src="https://github.com/user-attachments/assets/f59e9849-2fc6-42cf-9d6e-1f7e4c570e10" />
</p>

> [!NOTE]
> *Видеодемонстрация ключевых сценариев использования платформы: сквозная навигация по MPTT-оргструктуре подразделений, фиксация событий и поощрений сотрудников, динамический расчёт аналитики и выгрузка executive-отчётов в DOCX.*

---

## ⚡ Ключевые инженерные и архитектурные особенности

### 1. Рекурсивное моделирование оргструктуры (`django-mptt`)
* Алгоритм **Modified Preorder Tree Traversal (MPTT)** обеспечивает выборку любых ветвей оргструктуры за константное количество запросов.
* Мгновенный обход дерева любой глубины (`get_descendants(include_self=True)`) без рекурсивных SQL-запросов и деградации производительности (чтение дерева за $O(1)$).
* Интерактивное управление иерархией отделов через `django-mptt-admin`.

<p align="center">
  <img width="520" alt="Иерархия дерева отделов в Django MPTT" src="https://github.com/user-attachments/assets/9bf7ce4b-dfbf-480d-ad28-0b02170e149e" />
</p>

### 2. Иерархический ролевой контроль доступа (RBAC)
* Строгие проверки прав на базе Django `UserPassesTestMixin`.
* Многоуровневая ролевая модель:
  * **Тимлид / Руководитель группы**: Просмотр и внесение записей строго для сотрудников своей команды.
  * **Руководитель направления / Директор**: Сводная видимость и контроль всех дочерних подотделов.
  * **Специалист / Сотрудник**: Доступ только к личному делу и персональной истории поощрений/замечаний.
* Непоследовательные slug-идентификаторы на базе транслитерации и соленых UUID для защиты от перебора ID (Insecure Direct Object Reference).

### 3. Автоматическая генерация отчётов в Word (`docxtpl`)
* Формирование документов `.docx` с корпоративным форматированием на основе динамических агрегаций из базы данных.
* Серверная генерация диаграмм на лету с помощью **Matplotlib** и **Seaborn** (работает в фоновом безголовом режиме через `plt.switch_backend('agg')`).
* Автоматическое внедрение сгенерированных графиков непосредственно в результирующий Word-шаблон.

### 4. Интерактивная аналитика и фильтрация по периодам
* Асинхронные AJAX-запросы для агрегации данных за произвольные диапазоны дат (достижения, замечания, устранения замечаний).
* Динамическая круговая диаграмма на клиенте на базе **Chart.js**.

<p align="center">
  <img width="700" alt="Дашборд аналитики эффективности" src="https://github.com/KrayMakso68/disciplinary_practice_31_courses/assets/58968205/1b0c8078-a434-4c50-aec9-f6931cebb1fa" />
</p>

---

## 🏛️ Архитектура системы и потоки данных

```mermaid
flowchart TD
    subgraph Client["Веб-браузер"]
        AUTH_UI["Авторизация и сессии"]
        DASH["Оргструктура и личные дела"]
        STATS_UI["Аналитика и выбор диапазона дат"]
    end

    subgraph Django_App["Django-приложение"]
        AUTH_VIEW["Шлюз аутентификации / CustomLogin"]
        TREE_LOGIC["Иерархический RBAC\n(UserPassesTestMixin)"]
        MPTT_ENGINE["Движок обхода дерева django-mptt\n(Category.get_descendants)"]
        DOCX_ENGINE["DocxTemplate & Matplotlib/Seaborn\n(Генерация отчётов и диаграмм)"]
    end

    subgraph Storage["Хранилище данных и шаблоны"]
        DB[("Реляционная БД\n(MPTT Nested Sets)")]
        DOCX_TPL["Шаблон Word\n(Statistica_template.docx)"]
    end

    AUTH_UI --> AUTH_VIEW
    DASH --> TREE_LOGIC
    TREE_LOGIC --> MPTT_ENGINE
    MPTT_ENGINE <--> DB
    STATS_UI -->|AJAX-запрос диапазона дат| MPTT_ENGINE
    STATS_UI -->|Запрос экспорта отчёта| DOCX_ENGINE
    DOCX_ENGINE --> DOCX_TPL
    DOCX_ENGINE -->|Возврат файла .docx| STATS_UI
```

---

## 📂 Структура проекта

```
disciplinary_practice_31_courses/
├── disciplinary_practice/     # Конфигурация и настройки проекта
│   ├── settings.py           # Настройки с поддержкой .env (SECRET_KEY, DEBUG)
│   ├── urls.py               # Корневые маршруты URL
│   ├── wsgi.py               # Точка входа WSGI
│   └── asgi.py               # Точка входа ASGI
├── docs/                      # Медиа-материалы (GIF / видео) и документация
├── main/                      # Основное бизнес-приложение
│   ├── models.py             # Модели Category (MPTT), CustomUser, Note
│   ├── views.py              # Представления RBAC, AJAX-аналитика, экспорт Docx
│   ├── forms.py              # Формы авторизации и добавления записей
│   ├── admin.py              # Конфигурация Django & MPTT админ-панели
│   ├── static/               # CSS, JS (Chart.js, Bootstrap 5), docx-шаблоны
│   └── templates/            # Корпоративные шаблоны интерфейса
├── .env.template             # Образец переменных окружения
├── requirements.txt          # Зависимости Python
└── manage.py                 # CLI управления Django
```

---

## 🚀 Руководство по установке и запуску

### 1. Предварительные требования
* Python 3.10 или выше
* Git

### 2. Клонирование и настройка виртуального окружения
```bash
# Переход в папку с проектом
cd disciplinary_practice_31_courses

# Создание виртуального окружения
python -m venv venv

# Активация виртуального окружения
# Для Linux/macOS:
source venv/bin/activate
# Для Windows (PowerShell):
.\venv\Scripts\Activate.ps1
```

### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 4. Настройка переменных окружения
Скопируйте `.env.template` в `.env` и настройте параметры:
```bash
cp .env.template .env
```

Отредактируйте `.env`:
```env
SECRET_KEY=generate_a_secure_random_key_here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

### 5. Применение миграций и создание суперпользователя
```bash
# Применение миграций базы данных
python manage.py makemigrations
python manage.py migrate

# Создание администратора
python manage.py createsuperuser
```

### 6. Запуск сервера разработки
```bash
python manage.py runserver
```

Откройте в браузере:
* **Основной интерфейс**: `http://127.0.0.1:8000/`
* **Админ-панель**: `http://127.0.0.1:8000/admin/`

---

## 📄 Лицензия
Проект распространяется под открытой лицензией **MIT License**.
