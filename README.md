# Restaurant Management API

A comprehensive FastAPI-based restaurant management system with JWT authentication, role-based access control, and complete CRUD operations for all restaurant entities.

## 🚀 Features
- JWT authentication & role-based access
- Restaurant, menu, table, order, reservation, review, promotion, loyalty, inventory, and ingredient management
- Public QR code ordering, staff and manager/admin operations
- Secure password hashing, automatic admin creation
- Real-time analytics, error handling, and business logic

## 🛠️ Technology Stack
- FastAPI, PostgreSQL (Prisma ORM), JWT (python-jose), bcrypt, Pydantic

## 📋 Prerequisites
- Python 3.8+
- PostgreSQL
- Node.js (for Prisma CLI)

## 🚀 Installation
1. Clone the repository
2. Create a virtual environment and install dependencies
3. Set up your `.env` file
4. Generate Prisma client and run migrations
5. Start the application with `uvicorn main:app --reload`

## 📚 API Documentation
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🔑 Authentication & Roles
- CLIENT, WAITER, CHEF, MANAGER, ADMIN
- JWT token in `Authorization: Bearer <token>`

## 📖 Main API Endpoints
- `/auth` - Authentication
- `/restaurants` - Restaurant management
- `/menus` - Menus & dishes
- `/tables` - Table management
- `/orders` - Orders
- `/reservations` - Reservations
- `/reviews` - Reviews
- `/promotions` - Promotions
- `/loyalty` - Loyalty program
- `/inventory` - Inventory
- `/ingredients` - Ingredients

## 🛡️ Security
- Public endpoints for browsing, QR code ordering, promotions, reviews
- Authenticated endpoints for profile, orders, reservations, loyalty
- Staff/manager/admin endpoints for management and analytics

## 🚦 Error Handling
Standard HTTP status codes and descriptive error messages.

## 📄 License
MIT License

---
**Built with ❤️ using FastAPI and modern Python practices**
