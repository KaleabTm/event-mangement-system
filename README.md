# Event Management System

A full-stack Event Management platform powered by:

* 🐍 **Django** (Backend)
* ⚛️ **Next.js** (Frontend)
* 🐘 **PostgreSQL** (Database)
* 🌐 **Nginx** (Reverse proxy)
* 🐳 **Docker** (for containerization)

---

## 📁 Project Structure

```plaintext
ems/
├── event-management-backend/       # Django backend
│   └── docker/
│       └── development/Dockerfile
├── event-management-frontend/      # Next.js frontend
│   └── docker/
│       └── Dockerfile
├── nginx/
│   └── default.conf
├── docker-compose.yml
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

* [Docker](https://www.docker.com/products/docker-desktop)
* [Docker Compose](https://docs.docker.com/compose/)

---

## 🔧 Setup & Usage

### 1. Clone the Repository

```bash
git clone https://github.com/KaleabTm/event-mangement-system.git
cd ems
```

### 2. Build & Run Containers

```bash
docker compose up --build
```

* **Frontend**: [http://localhost:3000](http://localhost:3000)
* **Backend**: [http://localhost:8000/api/](http://localhost:8000/api/)
* **Nginx Proxy (prod ready entrypoint)**: [http://localhost](http://localhost)

---

## 💾 PostgreSQL Data Persistence

All database data is stored in a named volume (`postgres_data`) and will **persist** even if the containers are destroyed.
To clear everything (including DB):

```bash
docker compose down -v
```

---

## ✅ Health & Readiness

* `postgres` includes a healthcheck to ensure DB is ready before Django starts.
* `depends_on` is used to manage service startup order.

---

## 🔪 Testing Endpoints

You can test backend APIs using tools like:

* [Postman](https://www.postman.com/)
* `curl http://localhost:8000/api/`
* Or frontend pages at `http://localhost:3000`

---

## 📜 License

MIT — feel free to use and adapt this project.

---
