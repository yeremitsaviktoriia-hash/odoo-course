# Odoo ERP-CRM — Library Rental

Навчальний проєкт із курсу «ERP-CRM системи».

**Версія:** Odoo 19 Community  
**Модуль:** `library_rental`  
**База даних:** `library_db`

## 1. Що згенерував AI-асистент

Для створення каркасу модуля `library_rental` використовувався GitHub Copilot у VS Code.

Приклад промпту для генерації:

> Create a minimal Odoo 19 Community module named `library_rental` inside `custom_addons`. Generate `__manifest__.py`, root `__init__.py`, `models/__init__.py`, and empty `views/` and `security/` directories. Use only `base` as a dependency. Do not create ORM models yet.

AI-асистент допоміг створити структуру модуля, файл маніфесту та файли ініціалізації Python.

## 2. Що перевірено та виправлено вручну

Після генерації проведено перевірку:

- `version = '19.0.1.0.0'` — відповідає Odoo 19.
- `depends = ['base']` — відсутні зайві залежності.
- `license = 'LGPL-3'` — коректна ліцензія.
- `installable = True` — модуль дозволено встановлювати.
- `application = True` — модуль відображається серед застосунків.
- Кореневий `__init__.py` імпортує `models`.
- `models/__init__.py` залишено порожнім, оскільки ORM-моделі ще не реалізовані.

Зайвих залежностей не виявлено. Ручних виправлень у маніфесті не знадобилося.

## Результат

Модуль `library_rental` створено та встановлено в локальній базі Odoo 19 Community. На наступних практичних заняттях планується додати моделі Book, Copy, Member і Loan.