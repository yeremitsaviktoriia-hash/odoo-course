# Odoo ERP-CRM — Library Rental

Навчальний проєкт із курсу «ERP-CRM системи».

**Версія:** Odoo 19 Community  
**Модуль:** `library_rental`  
**База даних:** `library_db`

## AI-generated

Для створення каркасу та моделі Book модуля `library_rental` використовувався GitHub Copilot у VS Code.

Приклад промпту для генерації:

> Create a minimal Odoo 19 Community module named `library_rental` inside `custom_addons`. Generate `__manifest__.py`, root `__init__.py`, `models/__init__.py`, and empty `views/` and `security/` directories. Use only `base` as a dependency. Do not create ORM models yet.

Copilot згенерував каркас модуля, початковий маніфест та файли ініціалізації Python. Початкові параметри маніфесту (`version`, `depends`, `license`, `installable` і `application`) залишилися як згенеровані. Модель Book і базові подання додано окремим кроком.

## Вручну виправлено та перевірено

Каркас доповнено реєстрацією моделей Book, Copy, Member і Loan у `models/__init__.py` та підключенням прав доступу, подань і демо-даних у маніфесті. Точний розподіл цих правок між Copilot і автором у початковій історії проєкту не зафіксовано.

Під час рев’ю звірено всі три `Many2one`. У поточному коді кожен уже мав явні `required=True` та `ondelete='restrict'`, тому ці параметри збережено. Також перевірено обов’язковість назви книги, інвентарного номера примірника, імені та номера читацького квитка. Дати завершення і повернення можна заповнити пізніше.

## Структура зв’язків

Book описує видання, Copy — його фізичний примірник, Member — читача, а Loan — видачу конкретного примірника конкретному читачеві. Це дає змогу вести окрему історію кожного примірника одного видання.

| Прямий зв’язок (`Many2one`) | Зворотний зв’язок (`One2many`) | Чому поле обов’язкове і діє `ondelete='restrict'` |
| --- | --- | --- |
| `Copy.book_id → Book` | `Book.copy_ids` показує всі примірники видання | Кожен примірник належить виданню. Odoo блокує видалення книги, поки на неї посилаються примірники. |
| `Loan.copy_id → Copy` | `Copy.loan_ids` показує історію видач примірника | Кожна видача стосується конкретного примірника. Odoo блокує видалення примірника, поки на нього посилаються видачі, зокрема повернені. |
| `Loan.member_id → Member` | `Member.loan_ids` показує історію видач читача | Кожна видача має читача. Odoo блокує видалення читача, поки на нього посилаються видачі. |

`One2many` використовує відповідне зворотне поле `Many2one`. Назву книги й автора у формі видачі Odoo бере через `copy_id.book_id`, а номер читацького квитка — через `member_id`.

### Відхилення від рекомендованої структури

За доступними вимогами кроків 4–6 відхилень у зв’язках не виявлено. Додаткові поля у видачі лише відображають дані пов’язаних записів.

### Перевірка

Модуль успішно оновлено в `library_db`. Під час перевірки кроку 4 Odoo завантажив список і форму Loans для внутрішнього користувача. Пробний імпорт дав 4 книги, 8 примірників, 3 читачів і 4 видачі. Для видачі *Dune* перевірено автора Frank Herbert. Тестову транзакцію відкочено, оскільки в робочій базі демо-режим вимкнений.

## Крок 5. Практика з ORM в Odoo shell

Вправи виконано 18.11.2026 у базі `library_db`. Вивід консолі збережено у файлі [odoo-shell-step-5.txt](odoo-shell-step-5.txt). Команда запуску в PowerShell наведена нижче.

```powershell
& D:\Odoo19\odoo\.venv\Scripts\python.exe D:\Odoo19\odoo\odoo-bin shell -c D:\Odoo19\odoo\odoo.conf -d library_db --no-http
```

### 1. Пошук книг за автором

```python
books = env['library.book'].search([('author', '=', 'Frank Herbert')])
books.read(['name', 'author'])
```

Знайдено одну книгу — **Dune** (ID 6).

### 2. Підрахунок вільних примірників

```python
book = books.filtered(lambda record: record.name == 'Dune')[:1]
copies = env['library.copy'].search([('book_id', '=', book.id)])
free_copies = copies.filtered(
    lambda copy: not copy.loan_ids.filtered_domain([('state', '=', 'active')])
)
len(free_copies)
```

Отримано **1** вільний примірник — `ORM-DUNE-001` (ID 9). Для вправи його додано до наявної книги.

### 3. Пошук прострочених видач

```python
from odoo import fields

loans = env['library.loan']
today = fields.Date.context_today(loans.with_context(tz='Europe/Kyiv'))
overdue = loans.search([('state', '=', 'active'), ('due_date', '<', today)])
overdue.ids
```

Станом на 18.11.2026 результат — `[]`.

### 4. Створення та закриття видачі

Для вправи додано читача **ORM Practice Reader** (ID 4). Наступний блок створює нову видачу при кожному виконанні.

```python
member = env['library.member'].browse(4)
loan = loans.create({
    'copy_id': free_copies[0].id,
    'member_id': member.id,
    'loan_date': today,
    'due_date': today,
})
assert loan.state == 'active'
loan.write({'state': 'returned', 'return_date': today})
assert loan.state == 'returned' and loan.return_date == today
env.cr.commit()
```

Видачу **ID 5** створено в стані `active`, переведено в `returned` і збережено в базі. Дата повернення — 18.11.2026.
