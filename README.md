InventoryFlow

Sistema moderno de gestión de inventarios full-stack diseñado para el seguimiento de stock y logística en tiempo real. Este proyecto se centra en una arquitectura desacoplada y profesional utilizando Python (FastAPI) y Angular.

🛠 Stack Tecnológico

Backend: Python 3.11 + FastAPI

Frontend: Angular 16+ (TypeScript)

Base de Datos: PostgreSQL 15

ORM: SQLAlchemy

DevOps: Docker & Docker Compose

🚀 Características Clave

Gestión en Tiempo Real: CRUD completo para productos y categorías.

Alertas de Stock: Indicadores visuales para productos con bajo inventario basados en umbrales personalizados.

Persistencia de Datos: Integración con base de datos relacional y esquemas optimizados.

API RESTful: Endpoints totalmente documentados con Swagger/OpenAPI.

Entorno Dockerizado: Infraestructura de datos aislada para facilitar el desarrollo y despliegue.

📦 Configuración del Proyecto

1. Base de Datos
Asegúrate de tener Docker instalado. Desde la raíz del proyecto, ejecuta:

Bash
docker-compose up -d
Esto iniciará PostgreSQL y pgAdmin (disponible en localhost:8080).

2. Backend (Python)
Accede a la carpeta /backend:

Crea un entorno virtual: python -m venv venv

Instala las dependencias: pip install -r requirements.txt

Inicia el servidor: uvicorn main:app --reload

3. Frontend (Angular)
Accede a la carpeta /frontend:

Instala las dependencias: npm install

Inicia la aplicación: ng serve

Accede a la interfaz en: http://localhost:4200

📁 Estructura del Proyecto
/backend: Lógica de FastAPI, modelos de SQLAlchemy y rutas de la API.

/frontend: Componentes de Angular, servicios y formularios reactivos.

docker-compose.yml: Orquestación de la infraestructura para desarrollo.

-----------------------------------------------------------------------------

InventoryFlow

A modern, full-stack inventory management system designed for real-time stock tracking and logistics. This project focuses on a clean, decoupled architecture using Python (FastAPI) and Angular.

🛠 Tech Stack

Backend: Python 3.11 + FastAPI

Frontend: Angular 16+

Database: PostgreSQL 15

ORM: SQLAlchemy

DevOps: Docker & Docker Compose

🚀 Key Features

Real-time Inventory Management: Complete CRUD for products and categories.

Stock Alerts: Visual indicators for low-stock items based on custom thresholds.

Data Persistence: Relational database integration with optimized schemas.

RESTful API: Fully documented endpoints using Swagger/OpenAPI.

Dockerized Environment: Isolated database and management tools for easy setup.

📦 Getting Started

1. Database Setup
Ensure you have Docker installed. From the root directory, run:

Bash
docker-compose up -d
This will start PostgreSQL and pgAdmin (available at localhost:8080).

2. Backend Setup
Navigate to the /backend folder:

Create a virtual environment: python -m venv venv

Install dependencies: pip install -r requirements.txt

Run the server: uvicorn main:app --reload

3. Frontend Setup
Navigate to the /frontend folder:

Install dependencies: npm install

Start the application: ng serve

Access the UI at: http://localhost:4200

📁 Project Structure
/backend: FastAPI logic, SQLAlchemy models, and API routes.

/frontend: Angular components, services, and reactive forms.

docker-compose.yml: Infrastructure orchestration for development.
