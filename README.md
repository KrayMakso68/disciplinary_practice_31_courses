# Enterprise Hierarchical Workforce & Discipline Tracking System

<p align="center">
  <strong>Scalable corporate workforce performance and discipline management platform with recursive organizational hierarchy modeling</strong>
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

## 🏢 Overview

**Enterprise Hierarchical Workforce & Discipline Tracking System** is a production-oriented web platform designed for enterprises with deep organizational structures (Headquarters $\to$ Branches $\to$ Departments $\to$ Operational Units). It enables companies to systematize performance evaluations, maintain auditable records of commendations and disciplinary measures, generate compliance reports, and visualize workforce metrics across hierarchical tiers.

The platform solves the challenge of strictly delegating visibility and authority: department heads can only inspect and record events for employees within their specific organizational branch and descendant subunits.

---

## 🎥 Демонстрация работы / Live Demo

<p align="center">
  <img width="850" alt="Enterprise Workforce & Discipline Tracking System Demo" src="docs/demo.gif" />
</p>

> [!NOTE]
> *Видео и GIF демонстрации работы платформы (навигация по MPTT-оргструктуре, фиксация событий, расчёт аналитики и генерация DOCX-отчётов) размещены в каталоге [`docs/`](docs/).*

---

## ⚡ Key Engineering Features

### 1. Recursive Hierarchy Modeling (`django-mptt`)
* Implements **Modified Preorder Tree Traversal (MPTT)** for high-efficiency querying of multi-level corporate structures.
* Rapidly traverses arbitrary organizational depths (`get_descendants(include_self=True)`) without recursive database queries or performance penalties ($O(1)$ read complexity for descendant trees).
* Features interactive nested administrative management via `django-mptt-admin`.

<p align="center">
  <img width="520" alt="Tree Hierarchy in Django MPTT" src="https://github.com/user-attachments/assets/9bf7ce4b-dfbf-480d-ad28-0b02170e149e" />
</p>

### 2. Hierarchical Role-Based Access Control (RBAC)
* Granular permission gates enforced through Django's `UserPassesTestMixin`.
* Multi-tier role ladder:
  * **Team Lead / Head of Unit**: Visibility and record management confined strictly to their unit.
  * **Department Head / Director**: Aggregated overview of all descendant branches.
  * **Staff Specialist**: Personal discipline and commendation history ledger.
* Non-sequential slug generation using UUID-salted transliteration to protect against ID enumeration.

### 3. Automated Executive Document Generation (`docxtpl`)
* Generates formatted, executive-ready `.docx` compliance documents populated dynamically from database statistics.
* Server-side on-the-fly data visualization via **Matplotlib** and **Seaborn** (headless backend rendering with `plt.switch_backend('agg')`).
* Dynamic embedding of generated analytics charts directly into the target document template.

### 4. Interactive Analytics & Date Filtering
* Asynchronous AJAX queries for instant period aggregation (commendations, disciplinary notes, resolution of prior penalties).
* Dynamic donut chart visualization rendered on the client via **Chart.js**.

<p align="center">
  <img width="700" alt="Workforce Discipline Tracking Dashboard" src="https://github.com/KrayMakso68/disciplinary_practice_31_courses/assets/58968205/1b0c8078-a434-4c50-aec9-f6931cebb1fa" />
</p>

---

## 🏛️ System Architecture & Data Flow

```mermaid
flowchart TD
    subgraph Client["Web Browser"]
        AUTH_UI["Authentication & Login"]
        DASH["Workforce Tree & Records"]
        STATS_UI["Interactive Analytics & Date-Range Picker"]
    end

    subgraph Django_App["Django Application"]
        AUTH_VIEW["CustomLogin / Auth Gate"]
        TREE_LOGIC["Hierarchical RBAC\n(UserPassesTestMixin)"]
        MPTT_ENGINE["django-mptt Tree Traversal\n(Category.get_descendants)"]
        DOCX_ENGINE["DocxTemplate & Matplotlib/Seaborn\n(Automated Chart Generation)"]
    end

    subgraph Storage["Persistence & Templates"]
        DB[("Relational Database\n(MPTT Nested Sets)")]
        DOCX_TPL["Word Template\n(Statistica_template.docx)"]
    end

    AUTH_UI --> AUTH_VIEW
    DASH --> TREE_LOGIC
    TREE_LOGIC --> MPTT_ENGINE
    MPTT_ENGINE <--> DB
    STATS_UI -->|AJAX Date-Range Query| MPTT_ENGINE
    STATS_UI -->|Export Report Request| DOCX_ENGINE
    DOCX_ENGINE --> DOCX_TPL
    DOCX_ENGINE -->|Returns .docx Download| STATS_UI
```

---

## 📂 Project Structure

```
disciplinary_practice_31_courses/
├── disciplinary_practice/     # Project configuration & settings
│   ├── settings.py           # Environment-configured settings (SECRET_KEY, DEBUG)
│   ├── urls.py               # Root URL declarations
│   ├── wsgi.py               # WSGI production entrypoint
│   └── asgi.py               # ASGI asynchronous entrypoint
├── docs/                      # Demonstration media (GIF / video) and project assets
├── main/                      # Core business application
│   ├── models.py             # Category (MPTT), CustomUser, Note models
│   ├── views.py              # RBAC views, AJAX analytics, Docx export
│   ├── forms.py              # Authenticated user & record forms
│   ├── admin.py              # Django & MPTT admin configuration
│   ├── static/               # CSS, JS (Chart.js, Bootstrap 5), docx templates
│   └── templates/            # Corporate UI templates & error layouts
├── .env.template             # Environment variables blueprint
├── requirements.txt          # Python dependencies
└── manage.py                 # Django management CLI
```

---

## 🚀 Setup & Installation Guide

### 1. Prerequisites
* Python 3.10 or higher
* Git

### 2. Clone and Setup Environment
```bash
# Navigate to the project directory
cd disciplinary_practice_31_courses

# Create a Python virtual environment
python -m venv venv

# Activate the virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.template` to `.env` and configure your settings:
```bash
cp .env.template .env
```

Edit `.env`:
```env
SECRET_KEY=generate_a_secure_random_key_here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

### 5. Apply Migrations & Initialize
```bash
# Apply database migrations
python manage.py makemigrations
python manage.py migrate

# Create an administrator account
python manage.py createsuperuser
```

### 6. Run the Development Server
```bash
python manage.py runserver
```

Open your browser and navigate to:
* **Application**: `http://127.0.0.1:8000/`
* **Admin Portal**: `http://127.0.0.1:8000/admin/`

---

## 📄 License
This project is open-source and licensed under the **MIT License**.
