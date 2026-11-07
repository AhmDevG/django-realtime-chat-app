# Django Real-Time Chat App

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Django-Framework-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django" />
  <img src="https://img.shields.io/badge/WebSockets-Realtime-010101?style=for-the-badge&logo=socketdotio&logoColor=white" alt="WebSockets" />
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="MIT License" />
</p>

<p align="center">
  A real-time chat application built with Django and Django Channels, featuring WebSocket-based communication.
</p>

---

## ✨ Features

- [] **Real-Time Messaging** — Instant communication using WebSockets. 
- [x] **Authentication** — User authentication and account management.
- [x] **Chat Rooms** — Real-time chat room creation and management. 
- [] **Message History** — Access previous conversations.
- [x] **Profile Management** — Edit and manage your profile.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming language |
| Django | Web framework |
| Django Channels | WebSocket support |
| Uvicorn | ASGI server |
| SQLite | Default development database |
| uv | Dependency and package management |

> **Note:** SQLite is configured as the default database. You can switch to another database through `settings.py`. For production deployments, consider PostgreSQL or MySQL.

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)

### 1. Clone the Repository

```bash
git clone https://github.com/AhmDevG/django-realtime-chat-app.git
cd django-realtime-chat-app
```

### 2. Install Dependencies

```bash
uv sync
```

### 3. Environment Configuration

Create a `.env` file in the project root directory and configure the following variables:

```env
EMAIL_BACKEND=
EMAIL_HOST=
EMAIL_PORT=
EMAIL_USE_TLS=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL=
```

> Keep your `.env` file private and never commit credentials or secrets to GitHub.

### 4. Apply Database Migrations

```bash
uv run python manage.py migrate
```

### 5. Start the Development Server

```bash
uv run uvicorn chat_project.asgi:application --reload
```

The application will be available at:

**http://127.0.0.1:8000/**

> The default address and port may vary depending on your Uvicorn configuration.

---

## 📸 Screenshots

<details>
<summary><strong>View Application Screenshots</strong></summary>

<br />

<table>
  <tr>
    <td width="50%">
      <img src="https://github.com/user-attachments/assets/9c07a0a2-279a-426a-b82b-d8ce88fff8ab" alt="Application Screenshot 1" width="100%" />
    </td>
    <td width="50%">
      <img src="https://github.com/user-attachments/assets/469e7019-9b2d-43b0-a07e-7f7f2c03e3dd" alt="Application Screenshot 2" width="100%" />
    </td>
  </tr>
  <tr>
    <td>
      <img src="https://github.com/user-attachments/assets/a0b34866-29f5-4254-b72b-59d65351c001" alt="Application Screenshot 3" width="100%" />
    </td>
    <td>
      <img src="https://github.com/user-attachments/assets/21caf2c4-3f09-412b-af8a-94a90722d784" alt="Application Screenshot 4" width="100%" />
    </td>
  </tr>
  <tr>
    <td>
      <img src="https://github.com/user-attachments/assets/cb1ca5bd-8325-4926-bce5-8c7225141bbe" alt="Application Screenshot 5" width="100%" />
    </td>
    <td>
      <img src="https://github.com/user-attachments/assets/2cb268ed-66d6-4522-85e1-817a4ab25ff0" alt="Application Screenshot 6" width="100%" />
    </td>
  </tr>
  <tr>
    <td>
      <img src="https://github.com/user-attachments/assets/9b5af0fe-49e4-469b-8af8-8ab4503b7b1d" alt="Application Screenshot 7" width="100%" />
    </td>
    <td>
      <img src="https://github.com/user-attachments/assets/8ade5d0a-82d5-4a45-a6c6-ce00e0920155" alt="Application Screenshot 8" width="100%" />
    </td>
  </tr>
  <tr>
    <td>
      <img src="https://github.com/user-attachments/assets/3e279dba-084e-4655-a590-f1820830f22c" alt="Application Screenshot 9" width="100%" />
    </td>
    <td>
      <img src="https://github.com/user-attachments/assets/810203f6-2f6e-4424-96a4-bce0efaf4563" alt="Application Screenshot 10" width="100%" />
    </td>
  </tr>
</table>

</details>

---

## 📄 License

This project is licensed under the **MIT License**.

See the [LICENSE](LICENSE) file for details.

> [!WARNING]
> **Work in Progress:** This project is still under active development and is not considered production-ready.
>
> It may contain bugs, incomplete features, and potential security vulnerabilities. Use it for development and testing purposes only. Do not deploy it in a production environment until it has been properly reviewed and secured.
