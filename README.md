# Restaurant Management API

A comprehensive FastAPI-based restaurant management system with JWT authentication, role-based access control, and complete CRUD operations for all restaurant entities.

## 🚀 Features

### 🔐 Authentication & Authorization
- **JWT Token Authentication** with access and refresh tokens
- **Role-based Access Control** (CLIENT, WAITER, CHEF, MANAGER, ADMIN)
- **Secure Password Hashing** using bcrypt
- **Automatic Admin Creation** on startup if none exists

### 🏪 Restaurant Management
- Complete restaurant CRUD operations
- Multi-location support
- Restaurant-specific staff management
- Operating hours and contact information

### 🍽️ Menu & Dishes Management
- Hierarchical menu structure (Restaurant → Menu → Categories → Dishes)
- Rich dish information (images, galleries, preparation time, popularity)
- Ingredient tracking with dietary information
- Allergen management and automatic compilation

### 🪑 Table Management
- QR code and NFC tag support for contactless ordering
- Table capacity and status tracking
- Restaurant-specific table management

### 📝 Order Management
- **Public QR Code Ordering** (dine-in, no authentication required)
- **Authenticated App Ordering** (delivery, pickup with user profiles)
- Automatic user profile integration for contact information
- Order status tracking and management
- Amount limits for public orders

### 📅 Reservation System
- **Public Availability Checking**
- **Staff-managed Public Reservations** (walk-ins)
- **Authenticated App Reservations** (security required)
- Table availability validation
- Reservation status management

### ⭐ Review & Rating System
- Customer review creation and management
- Review verification against completed orders
- Sentiment analysis and analytics
- Restaurant and dish-specific ratings
- Staff response capabilities

### 🎯 Promotions & Marketing
- Flexible promotion system with discount calculations
- Restaurant and dish-specific promotions
- Usage tracking and analytics
- Time-based promotional campaigns

### 🏆 Loyalty Program
- Simple points-based rewards system (1 point per $1 spent)
- Points redemption for discounts (100 points = $1)
- Transaction history and analytics
- Customer loyalty statistics

### 📦 Inventory Management
- Complete stock tracking with categories and suppliers
- Low stock alerts and expiry date monitoring
- Stock quantity updates with reason tracking
- Real-time inventory valuation
- Category and supplier analytics

### 🥬 Ingredients Management
- Comprehensive ingredient database
- Dietary information tracking (vegetarian, vegan, gluten-free, dairy-free)
- Allergen information management
- Dish-ingredient relationships with quantities
- Automatic dietary compilation for dishes

## 🛠️ Technology Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL with Prisma ORM
- **Authentication**: JWT with python-jose
- **Password Hashing**: bcrypt
- **Validation**: Pydantic models
- **Documentation**: Automatic OpenAPI/Swagger

## 📋 Prerequisites

- Python 3.8+
- PostgreSQL
- Node.js (for Prisma CLI)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd back-end2
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Environment Variables**
   ```env
   DATABASE_URL="postgresql://username:password@localhost:5432/restaurant_db"
   SECRET_KEY="your-super-secret-jwt-key"
   ALGORITHM="HS256"
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   REFRESH_TOKEN_EXPIRE_DAYS=7
   ```

6. **Database setup**
   ```bash
   # Generate Prisma client
   prisma generate
   
   # Run migrations
   prisma migrate dev
   ```

7. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

## 📚 API Documentation

Once running, access the interactive API documentation at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🔑 Authentication

### User Roles
- **CLIENT**: Regular customers (app users)
- **WAITER**: Restaurant staff (order management)
- **CHEF**: Kitchen staff (order preparation)
- **MANAGER**: Restaurant managers (full restaurant access)
- **ADMIN**: System administrators (global access)

### Authentication Flow
1. **Register**: `POST /auth/register`
2. **Login**: `POST /auth/login`
3. **Refresh Token**: `POST /auth/refresh`
4. **Logout**: `POST /auth/logout`

### Protected Endpoints
Include the JWT token in the Authorization header:
```
Authorization: Bearer <your-jwt-token>
```

## 📖 API Endpoints

### 🔐 Authentication (`/auth`)
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `POST /auth/refresh` - Refresh access token
- `POST /auth/logout` - User logout
- `GET /auth/me` - Get current user info

### 🏪 Restaurants (`/restaurants`)
- `GET /restaurants` - List restaurants (public)
- `POST /restaurants` - Create restaurant (Admin only)
- `GET /restaurants/{id}` - Get restaurant details
- `PUT /restaurants/{id}` - Update restaurant (Manager/Admin)
- `DELETE /restaurants/{id}` - Delete restaurant (Admin only)

### 🍽️ Menus (`/menus`)
- `GET /menus/restaurant/{restaurant_id}` - Get restaurant menu (public)
- `POST /menus` - Create menu (Manager/Admin)
- `PUT /menus/{menu_id}` - Update menu (Manager/Admin)
- `POST /menus/categories` - Create menu category (Manager/Admin)
- `POST /menus/dishes` - Create dish (Manager/Admin)

### 🪑 Tables (`/tables`)
- `GET /tables/restaurant/{restaurant_id}` - List tables (Staff)
- `POST /tables` - Create table (Manager/Admin)
- `PUT /tables/{table_id}` - Update table (Manager/Admin)
- `GET /tables/{table_id}/qr` - Generate QR code (Staff)

### 📝 Orders (`/orders`)
- `POST /orders/public` - Create public order (QR code ordering)
- `POST /orders` - Create authenticated order
- `GET /orders/my-orders` - Get user's orders
- `GET /orders/restaurant/{restaurant_id}` - Get restaurant orders (Staff)
- `PUT /orders/{order_id}/status` - Update order status (Staff)

### 📅 Reservations (`/reservations`)
- `GET /reservations/availability` - Check table availability (public)
- `POST /reservations/public` - Create public reservation (Staff only)
- `POST /reservations` - Create authenticated reservation
- `GET /reservations/my-reservations` - Get user's reservations
- `GET /reservations/restaurant/{restaurant_id}` - Get restaurant reservations (Staff)

### ⭐ Reviews (`/reviews`)
- `GET /reviews/restaurant/{restaurant_id}` - Get restaurant reviews (public)
- `POST /reviews` - Create review (authenticated users)
- `GET /reviews/my-reviews` - Get user's reviews
- `PUT /reviews/{review_id}/response` - Staff response to review

### 🎯 Promotions (`/promotions`)
- `GET /promotions/active` - Get active promotions (public)
- `POST /promotions/calculate-discount` - Calculate promotion discount
- `POST /promotions` - Create promotion (Manager/Admin)
- `GET /promotions/restaurant/{restaurant_id}/stats` - Promotion analytics

### 🏆 Loyalty (`/loyalty`)
- `GET /loyalty/program-info` - Get loyalty program info (public)
- `GET /loyalty/my-card` - Get user's loyalty card
- `POST /loyalty/redeem-points` - Redeem loyalty points
- `POST /loyalty/award-points` - Award points for order (Staff)
- `GET /loyalty/restaurant/{restaurant_id}/stats` - Loyalty analytics

### 📦 Inventory (`/inventory`)
- `GET /inventory/items` - List inventory items (Staff)
- `POST /inventory/items` - Create inventory item (Manager/Admin)
- `PUT /inventory/items/{item_id}` - Update inventory item (Manager/Admin)
- `POST /inventory/stock/update` - Update stock quantity (Staff)
- `GET /inventory/low-stock-alerts/{restaurant_id}` - Low stock alerts
- `GET /inventory/stats/{restaurant_id}` - Inventory analytics

### 🥬 Ingredients (`/ingredients`)
- `GET /ingredients` - List ingredients (Staff)
- `POST /ingredients` - Create ingredient (Manager/Admin)
- `POST /ingredients/dish-ingredients` - Add ingredient to dish
- `GET /ingredients/dish/{dish_id}/ingredients` - Get dish ingredients
- `GET /ingredients/stats` - Ingredient analytics

## 🔒 Security Features

### Public Endpoints (No Authentication Required)
- Restaurant browsing and menu viewing
- Table availability checking
- QR code ordering (with limitations)
- Promotion browsing
- Review reading

### Authenticated Endpoints
- User profile management
- App-based ordering and reservations
- Review creation
- Loyalty program participation

### Staff-Only Endpoints
- Order and reservation management
- Inventory viewing
- Basic restaurant operations

### Manager/Admin-Only Endpoints
- Restaurant and menu management
- Staff management
- Inventory and ingredient management
- Analytics and reporting

## 🛡️ Security Considerations

1. **QR Code Orders**: Limited to dine-in only with amount restrictions
2. **App Reservations**: Require authentication for security
3. **Staff Isolation**: Staff can only access their assigned restaurant
4. **Admin Override**: Admins have global access across all restaurants
5. **Token Security**: Automatic token refresh and logout functionality

## 📊 Business Logic

### Order Types
- **DINE_IN**: Customer orders at table (public or authenticated)
- **DELIVERY**: Customer orders for delivery (authenticated only)
- **PICKUP**: Customer orders for pickup (authenticated only)

### User Experience
- **Automatic Profile Usage**: Authenticated orders automatically use user's saved contact information
- **Loyalty Integration**: Points automatically awarded on completed orders
- **Review Verification**: Reviews can only be created for completed orders

### Restaurant Operations
- **Multi-location Support**: Staff management per restaurant
- **Hierarchical Access**: Manager access includes all staff permissions
- **Real-time Analytics**: Live inventory, sales, and customer analytics

## 🚦 Error Handling

The API uses standard HTTP status codes:
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `422` - Validation Error
- `500` - Internal Server Error

All error responses include descriptive messages:
```json
{
  "detail": "Descriptive error message"
}
```

## 🧪 Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app tests/
```

## 📝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support, email support@restaurant-api.com or create an issue in the repository.

## 🔄 Version History

- **v1.0.0** - Initial release with complete restaurant management features
- Authentication system with JWT and role-based access
- Complete CRUD operations for all entities
- Public and authenticated endpoints
- Comprehensive analytics and reporting

---

**Built with ❤️ using FastAPI and modern Python practices**
