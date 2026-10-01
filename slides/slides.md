---
theme: seriph
title: SOLID Principles
titleTemplate: '%s'
info: |
  ## SOLID Principles Kata
  A hands-on tour of the five SOLID principles, with Python before/after examples.
class: text-center
highlighter: shiki
lineNumbers: false
drawings:
  persist: false
transition: slide-left
fonts:
  sans: 'Inter'
  mono: 'Fira Code'
presenter: true
---

# SOLID

<div class="text-xl opacity-80 mt-2">Five principles for maintainable object-oriented design</div>

<div class="abs-br m-6 text-sm opacity-50">
  Use <kbd>space</kbd> / arrow keys to navigate
</div>

<!--
Formalisé par Robert C Martin AKA Oncle Bob dans les années 2000 pour répondre à un problème lié à la dégradation du code au fur et a mesure que les projets grossissent.
-->

---
layout: center
class: text-center
---

# What does SOLID stand for?

<div class="grid grid-cols-5 gap-4 mt-12 text-2xl font-bold">
  <div class="p-4 rounded-lg bg-blue-500/10 border border-blue-500/30">S</div>
  <div class="p-4 rounded-lg bg-green-500/10 border border-green-500/30">O</div>
  <div class="p-4 rounded-lg bg-yellow-500/10 border border-yellow-500/30">L</div>
  <div class="p-4 rounded-lg bg-purple-500/10 border border-purple-500/30">I</div>
  <div class="p-4 rounded-lg bg-red-500/10 border border-red-500/30">D</div>
</div>

<div class="mt-8 opacity-70">
  Let's reveal each letter as we go 👇
</div>


---
layout: center
class: text-center
---

# S — Single Responsibility

<div class="text-2xl mt-6">
A class should be responsible for a single part of the software functionality
</div>

---

# ❌ No Single Responsibility

```python
@dataclass
class User:
    """Represents information about a user"""
    name: str
    email: str

    # Function that handles the database when the scope
    # of this class is to represent a user
    def save_to_database(self):
        database = Database()
        database.save("user", self.name)
```

<v-click>

<div class="mt-4 text-red-400">
⚠️ <code>User</code> now knows how to persist itself — mixing "what a user is" with "how it's stored" <br />
⚠️ Database is initialized on the fly on User method.
</div>

</v-click>

---

# ✅ Enforcing Single Responsibility

```python
@dataclass
class User:
    """Represents information about a user"""
    name: str
    email: str


class UserRepository:
    """Dedicated class that maps a user object to the database"""
    def __init__(self, db: Database):
        self._db = db

    def save_user(self, user: User):
        self._db.save("user", user.name)
```

<div class="mt-4 text-green-400">
✅ <code>User</code> only represents data. <code>UserRepository</code> makes the relation between User and database
</div>

<!--
Une classe User q
-->

---
layout: center
class: text-center
---

# O — Open/Closed

<div class="text-2xl mt-6">
Open for extension, closed for modification
</div>

---

# ❌ No Open/Closed

```python
@dataclass
class User:
    name: str
    email: str

class BusinessLogic:

    def handle_mail(self, user: User) -> None:
        if user.email.endswith("@hotmail.fr"):
            print("something with hotmail happened")
        elif user.email.endswith("@google.fr"):
            print("something with google happened")
        # Tomorrow we have to handle @exterminator.com
        # ⚠️ what would happen?
```

---

# ✅ Enforcing Open/Closed

```python
# Common interface that glue all implementation
class MailHandler(Protocol):
    def supports(self, email: str) -> bool: ...
    def handle(self, user: User) -> None: ...


class HotmailHandler:
    def supports(self, email: str) -> bool:
        return email.endswith("@hotmail.fr")

    def handle(self, user: User) -> None:
        print("something with hotmail happened")

# sidenote: Missing Google Handler but slidedev doesn't allow large preview

class BusinessLogic:
    def __init__(self, mail_handlers: list[MailHandler]) -> None:
        self._mail_handlers = mail_handlers

    def handle_mail(self, user: User) -> None:
        for handler in self._mail_handlers:
            if handler.supports(user.email):
                handler.handle(user)
                return
```

---
layout: center
class: text-center
---

# L — Liskov Substitution

<div class="text-2xl mt-6">
A child class must implement and act like its parent
</div>

<div class="mt-8 italic opacity-70 max-w-lg mx-auto">
"If it looks like a duck and quacks like a duck but needs batteries,
you probably have the wrong abstraction"
</div>

---

# ❌ No Liskov Substitution

```python
@dataclass
class User:
    name: str
    email: str

class UserMailService:
    def send_welcome_mail(user: User) -> None:
        print(f"Sending welcome email to {user.email.lower()}")

@dataclass
class GuestUser(User):
    # ❌ User promises email is a string, but this allows None
    email: str | None = None


user_mail_service = UserMailService()
guest = GuestUser(name="Guest")
user_mail_service.send_welcome_mail(guest)  # 💥 None has no lower() method
```

---

# ✅ Enforcing Liskov Substitution

```python {10-11|15-16}
@dataclass
class User:
    name: str
    email: str

class UserMailService:
    def send_welcome_mail(user: User) -> None:
        print(f"Sending welcome email to {user.email.lower()}")

@dataclass
class GuestUser(User):
    # ✅ still honors the User contract: email stays a plain string
    email: str = "guest@exterminator.com"

user_mail_service = UserMailService()
guest = GuestUser(name="Guest")
user_mail_service.send_welcome_mail(guest)  # ✅ works everywhere User works
```

---
layout: center
class: text-center
---

# I — Interface Segregation

<div class="text-2xl mt-6">
A class should not be forced to depend on methods it does not use
</div>

<v-click>

<div class="mt-4 text-blue-400">
    Interfaces shouldn't have multiple scope.
</div>

</v-click>

---

# ❌ No Interface Segregation

```python
class NotificationService(Protocol):
    def send_email(self, address: str, message: str) -> None: ...
    def send_sms(self, phone_number: str, message: str) -> None: ...


class EmailNotificationService:
    def send_email(self, address: str, message: str) -> None:
        print(f"Sending email to {address}: {message}")

    # ❌ This service only sends email, but the interface also requires SMS
    def send_sms(self, phone_number: str, message: str) -> None:
        raise NotImplementedError
```

---

# ✅ Enforcing Interface Segregation

```python
class EmailSender(Protocol):
    def send_email(self, address: str, message: str) -> None: ...


class SmsSender(Protocol):
    def send_sms(self, phone_number: str, message: str) -> None: ...


class EmailNotificationService:
    def send_email(self, address: str, message: str) -> None:
        print(f"Sending email to {address}: {message}")


class WelcomeService:
    def __init__(self, email_sender: EmailSender) -> None:
        self._email_sender = email_sender

    def welcome(self, email: str) -> None:
        self._email_sender.send_email(email, "Welcome!")
```

---
layout: center
class: text-center
---

# D — Dependency Inversion

<div class="text-2xl mt-6">
High-level policy should depend on abstractions, not low-level details
</div>

---

# ❌ No Dependency Inversion

```python {8-9}
class Database:
    def save(self, table: str, value: str) -> None:
        print(f"Saving {value} to {table}")


class UserService:
    def __init__(self) -> None:
        # ❌ High-level logic constructs and depends on a concrete database
        self._database = Database()

    def save_user(self, name: str) -> None:
        self._database.save("user", name)
```

---

# ✅ Enforcing Dependency Inversion

```python {1-3|13-14|17-18}
class UserRepository(Protocol):
    def save_user(self, name: str) -> None: ...


class DatabaseUserRepository:
    def __init__(self, database: Database) -> None:
        self._database = database

    def save_user(self, name: str) -> None:
        self._database.save("user", name)


class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self._user_repository = user_repository

    def save_user(self, name: str) -> None:
        self._user_repository.save_user(name)


# ✅ The concrete implementation is supplied from outside the business logic
user_service = UserService(DatabaseUserRepository(Database()))
user_service.save_user("José")
```

---
layout: center
class: text-center
---

# Recap

<div class="grid grid-cols-1 gap-3 mt-8 text-left max-w-xl mx-auto">
  <div class="p-3 rounded-lg bg-blue-500/10 border border-blue-500/30"><b>S</b>ingle Responsibility — one reason to change</div>
  <div class="p-3 rounded-lg bg-green-500/10 border border-green-500/30"><b>O</b>pen/Closed — extend without modifying</div>
  <div class="p-3 rounded-lg bg-yellow-500/10 border border-yellow-500/30"><b>L</b>iskov Substitution — subtypes must honor contracts</div>
  <div class="p-3 rounded-lg bg-purple-500/10 border border-purple-500/30"><b>I</b>nterface Segregation — small, focused interfaces</div>
  <div class="p-3 rounded-lg bg-red-500/10 border border-red-500/30"><b>D</b>ependency Inversion — depend on abstractions</div>
</div>

---
layout: center
class: text-center
---

# Questions ?

<div class="text-xl opacity-70 mt-4">
    <p>Questions?</p>
    <img src="./img/image.png" />
</div>
