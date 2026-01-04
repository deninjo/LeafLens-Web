# LeafLens Web - Smart Maize Doctor


LeafLens Web is a **Django REST Framework (DRF)** powered API system that serves as the core data processing and management layer for agricultural disease detection. This project is part of a comprehensive machine learning ecosystem that began with CNN model training for maize disease identification and has evolved into a full-scale backend system for storing, moving, and processing agricultural data.

### Project Evolution
This backend system represents the **data infrastructure and API layer**. The journey started with:
1. **CNN Model Training** - Deep learning models for maize disease detection completed [here](https://github.com/deninjo/Leaf-Lens)
2. **ML Backend Development** (current phase) - A robust data system for:
   - **Data Storage**: Secure storage of predictions, disease information, and user suggestions
   - **Data Movement**: API endpoints for seamless data transfer and retrieval
   - **Data Processing**: Real-time machine learning inference and analysis
   - **User Management**: Authentication and user-specific data handling

## 📋 Table of Contents

- [Features](#-features)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Installation & Setup](#-installation--setup)
- [Running the System](#-running-the-system)
- [API Documentation](#-api-documentation)
  - [Base URL](#base-url)
  - [Authentication](#authentication)
  - [Rate Limits](#rate-limits)
  - [Common Errors](#common-errors)
  - [Auth Endpoints](#1-authentication-endpoints)
  - [Disease Endpoints](#2-disease-endpoints)
  - [Prediction Endpoints](#3-prediction-endpoints)
  - [Suggestion Endpoints](#4-suggestion-endpoints)

## ✨ Features

- **JWT Authentication** - Secure user authentication with access and refresh tokens
- **AI-Powered Predictions** - Real-time disease detection using trained TensorFlow Lite models
- **Image Processing** - CLIP-based pre-filtering and XAI (Explainable AI) integration
- **Disease Management** - Comprehensive disease information with metadata
- **Community Suggestions** - User-contributed treatment and prevention suggestions
- **Advanced Filtering** - Search, filter, and order prediction results
- **API Documentation** - Auto-generated Swagger/OpenAPI docs
- **Rate Limiting** - Throttling for API endpoints to prevent abuse


## 📁 Project Structure

```
leaflens/
├── manage.py                 # Django management script
├── leaflens/                 # Main project configuration
│   ├── settings.py           # Django settings
│   ├── urls.py              # Main URL routing
│   └── wsgi.py              # WSGI configuration
├── accounts/                 # User authentication app
│   ├── models.py            # User models
│   ├── views.py             # Auth views (register, login, logout)
│   ├── serializers.py       # Auth serializers
│   └── urls.py              # Auth URL patterns
├── diseases/                 # Disease management app
│   ├── models.py            # Disease model
│   ├── views.py             # Disease CRUD views
│   └── urls.py              # Disease URL patterns
├── predictions/              # ML prediction app
│   ├── models.py            # Prediction model
│   ├── views.py             # Prediction and ML inference views
│   ├── throttles.py         # Rate limiting configuration
│   ├── filters.py           # Prediction filtering
│   └── urls.py              # Prediction URL patterns
├── suggestions/              # Community suggestions app
│   ├── models.py            # Suggestion model
│   ├── views.py             # Suggestion CRUD views
│   └── urls.py              # Suggestion URL patterns
├── ml/                       # Machine learning utilities
│   ├── models/              # Trained ML models (.tflite files)
│   └── utils.py             # ML inference functions
├── media/                    # Uploaded files storage
│   ├── predictions/         # User-uploaded images
│   └── xai/                 # Explainable AI generated images
└── static/                   # Static files (CSS, JS)
```

## 🔧 Prerequisites

- Python 3.8+ (tested with 3.9, 3.12)
- Git (for cloning the repository) 
- pip (Python package manager)
- Virtual environment (recommended)
- `requirements.txt` includes all dependencies
- Optional Tools: **Postman** or **cURL** for API testing



## 🚀 Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/deninjo/LeafLens-Web.git
   cd LeafLens-Web/leaflens
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv leaflensvenv
   
   # On Windows
   leaflensvenv\Scripts\activate
   
   # On macOS/Linux
   source leaflensvenv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Create a .env file in the project root
   cp .env.example .env
   
   # Edit .env with your configurations:
   DJANGO_SECRET_KEY=your_secret_key
   DJANGO_DEBUG=True
   DB_NAME=leaflens_db
   DB_USER=admin
   DB_HOST=localhost
   DB_PORT=3306
   MYSQL_ADMIN_PASS=yourpassword

   ```

5. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Load initial diseases (optional)**

## 🏃‍♂️ Running the System

### Development Server
```bash
python manage.py runserver
```

The API will be available at: `http://127.0.0.1:8000/`

### Access Points
- **API Base**: `http://127.0.0.1:8000/api/`
- **Admin Panel**: `http://127.0.0.1:8000/admin/`
- **API Documentation**: `http://127.0.0.1:8000/api/docs/`
- **API Schema**: `http://127.0.0.1:8000/api/schema/`

## 📚 API Documentation

### Base URL
`http://127.0.0.1:8000/api/`

### Authentication

Uses **JWT (JSON Web Token) Authentication**.

Include the token in the header for authenticated requests:
```
Authorization: Bearer <your_access_token_here>
```

### Auth Flow Explanation
1. **Register/Login** → Get access token + refresh token
2. **Use access token** → Make authenticated requests (expires in 5 minutes)
3. **Refresh token** → Get new access token when it expires (refresh expires in 1 day)
4. **Logout** → Blacklist refresh token

### Rate Limits
- **Anonymous users**: 10 predictions per min
- **Authenticated users**: 60 predictions per hour
- **Other endpoints**: For predict endpoint, anonymous users get 3/min, authenticated users get 20/min
### Common Errors

| Status Code | Error | Description |
|-------------|-------|-------------|
| 400 | Bad Request | Invalid input data or missing required fields |
| 401 | Unauthorized | Missing or invalid authentication token |
| 403 | Forbidden | Access denied (insufficient permissions) |
| 404 | Not Found | Resource doesn't exist |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server-side error |

---

## 1. Authentication Endpoints

### 1.1 Register User

**Endpoint:** `/api/auth/register/`  
**Method:** `POST`  
**Description:** Create a new user account.  
**Auth Required:** No

#### Request Body:
```json
{
  "username": "farmeruno",
  "email": "farmeruno@example.com",
  "password": "securepassword123"
}
```

#### cURL Example:
```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "farmeruno", "email": "farmeruno@example.com", "password": "securepassword123"}' \
  | jq
```
The -X specifies POST method, -H sets content type, -d sends data, | jq formats JSON response nicely

#### Response (201 Created):
```json
{
  "detail": "User registered successfully"
}
```

#### Error (400 Bad Request):
```json
{
  "username": ["A user with that username already exists."]
}
```

---

### 1.2 Login User

**Endpoint:** `/api/auth/login/`  
**Method:** `POST`  
**Description:** Authenticate user and get JWT tokens.  
**Auth Required:** No

#### Request Body:
```json
{
  "username": "farmeruno",
  "password": "securepassword123"
}
```

#### cURL Example:
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "farmer1", "password": "securepassword123"}' \
  | jq
```

#### Response (200 OK):
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### Error (401 Unauthorized):
```json
{
  "detail": "No active account found with the given credentials"
}
```

---

### 1.3 Refresh Token

**Endpoint:** `/api/auth/refresh/`  
**Method:** `POST`  
**Description:** Get new access token using refresh token.  
**Auth Required:** No (but requires valid refresh token)

#### Request Body:
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### cURL Example:
```bash
curl -X POST http://127.0.0.1:8000/api/auth/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "your_refresh_token_here"}' \
  | jq
```

#### Response (200 OK):
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

---

### 1.4 Logout User

**Endpoint:** `/api/auth/logout/`  
**Method:** `POST`  
**Description:** Blacklist refresh token (logout).  
**Auth Required:** Yes

#### Request Body:
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### cURL Example:
```bash
curl -X POST http://127.0.0.1:8000/api/auth/logout/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_access_token" \
  -d '{"refresh": "your_refresh_token_here"}' \
  | jq
```

#### Response (205 Reset Content):
```json
{
  "detail": "Successfully logged out"
}
```

---

## 2. Disease Endpoints

### 2.1 List Diseases

**Endpoint:** `/api/diseases/`  
**Method:** `GET`  
**Description:** Get list of all diseases with metadata.  
**Auth Required:** No

#### cURL Example:
```bash
curl -X GET http://127.0.0.1:8000/api/diseases/ | jq
```

#### Response (200 OK):
```json
[
  {
    "id": 1,
    "name": "Blight",
    "scientific_name": "Exserohilum turcicum",
    "description": "A fungal disease affecting corn leaves...",
    "metadata": {
      "causes": ["High humidity", "Poor air circulation"],
      "prevention": ["Crop rotation", "Resistant varieties"],
      "treatment": ["Fungicide application", "Remove infected leaves"]
    },
    "sample_image": "https://example.com/blight.jpg"
  }
]
```

---

### 2.2 Get Disease Details

**Endpoint:** `/api/diseases/<id>/`  
**Method:** `GET`  
**Description:** Get detailed information about a specific disease.  
**Auth Required:** No

#### cURL Example:
```bash
curl -X GET http://127.0.0.1:8000/api/diseases/3/ | jq
```

#### Response (200 OK):
```json
{
  "id": 3,
  "name": "Gray Leaf Spot",
  "scientific_name": "Cercospora zeae-maydis",
  "description": "Appears as: Rectangular gray or tan spots with dark edges giving them a 'blocky' appearance",
  "metadata": {
    "causes": [
      "Fungus Cercospora zeae-maydis.",
      "Prolonged leaf wetness (dew, rain).",
      "Warm temperatures (25–30°C).",
      "Continuous maize monoculture."
    ],
    "treatment": [
      "Apply fungicides (e.g., azoxystrobin, pyraclostrobin) preventively.",
      "Prune lower leaves to improve airflow.",
      "Reduce nitrogen fertilizer if over-applied."
    ],
    "prevention": [
      "Use resistant maize varieties.",
      "Rotate crops with soybeans or small grains.",
      "Plow under crop residue to reduce fungal spores.",
      "Avoid planting in low-lying, humid areas."
    ]
  },
  "sample_image": "https://cals.cornell.edu/sites/default/files/styles/three_card_callout/public/2021-02/gray-leaf-spot-on-corn-07282020-chemung-ny-5744-web.jpg?h=bc58accd&itok=Csddl9J0"
}
```

---

## 3. Prediction Endpoints

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/api/predict/` | POST | Upload image for disease prediction | No |
| `/api/predictions/` | GET | List user's predictions | Yes |
| `/api/predictions/<id>/` | GET | Get specific prediction | Yes |
| `/api/predictions/<id>/` | DELETE | Delete prediction | Yes |

### 3.1 Upload Image for Prediction

**Endpoint:** `/api/predict/`  
**Method:** `POST`  
**Description:** Upload an image and get AI-powered disease prediction.  
**Auth Required:** No (but user association if authenticated)  
**Rate Limit:** 10/hour (anonymous), 100/hour (authenticated)

#### Request (Multipart Form):
```
image: <image_file>
```

#### cURL Example:
```bash
curl -X POST http://127.0.0.1:8000/api/predict/ \
  -H "Authorization: Bearer your_access_token" \
  -F "image=@/path/to/your/maize_leaf.jpg" \
  | jq
```

#### Response (201 Created) - Successful Prediction:
```json
{
  "id": 1,
  "user": 1,
  "image_path": "/media/predictions/maize_leaf.jpg",
  "predicted_disease": {
    "id": 1,
    "name": "Northern Corn Leaf Blight",
    "scientific_name": "Exserohilum turcicum"
  },
  "prediction_scores": {
    "Northern Corn Leaf Blight": 0.85,
    "Common Rust": 0.12,
    "Healthy": 0.03
  },
  "explanation_image": null,
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### Response (201 Created) - Non-Maize Image:
```json
{
  "id": 2,
  "user": 1,
  "image_path": "/media/predictions/not_maize.jpg",
  "predicted_disease": null,
  "prediction_scores": {
    "is_maize": false
  },
  "explanation_image": null,
  "created_at": "2024-01-15T10:35:00Z"
}
```

#### Error (400 Bad Request):
```json
{
  "image": ["This field is required."]
}
```

#### Error (429 Too Many Requests):
```json
{
  "detail": "Request was throttled. Expected available in 3600 seconds."
}
```

---

### 3.2 List User Predictions

**Endpoint:** `/api/predictions/`  
**Method:** `GET`  
**Description:** Get list of authenticated user's predictions with filtering options.  
**Auth Required:** Yes

#### Query Parameters:
- `predicted_disease`: Filter by disease ID
- `search`: Search in disease names
- `ordering`: Order by `created_at`, `-created_at`, `id`, `-id`

#### cURL Example:
```bash
curl -X GET "http://127.0.0.1:8000/api/predictions/?ordering=-created_at" \
  -H "Authorization: Bearer your_access_token" \
  | jq
```

#### Response (200 OK):
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 2,
      "user": 1,
      "image_path": "/media/predictions/maize_sample2.jpg",
      "predicted_disease": {
        "id": 2,
        "name": "Common Rust",
        "scientific_name": "Puccinia sorghi"
      },
      "prediction_scores": {
        "Common Rust": 0.92,
        "Northern Corn Leaf Blight": 0.06,
        "Healthy": 0.02
      },
      "explanation_image": null,
      "created_at": "2024-01-15T11:00:00Z"
    }
  ]
}
```

---

### 3.3 Delete Prediction

**Endpoint:** `/api/predictions/<id>/`  
**Method:** `DELETE`  
**Description:** Delete a specific prediction (user can only delete their own).  
**Auth Required:** Yes

#### cURL Example:
```bash
curl -X DELETE http://127.0.0.1:8000/api/predictions/1/ \
  -H "Authorization: Bearer your_access_token"
```

#### Response (204 No Content):
```
(No response body)
```

---

## 4. Suggestion Endpoints

| Endpoint                        | Method | Description | Auth Required    |
|---------------------------------|-------|--|------------------|
| `/api/suggestions/`             | GET | Get list of suggestions (Admins see all, farmers see theirs) | Yes              |
| `/api/suggestions/`             | POST | Create new suggestion | Yes              |
| `/api/suggestions/<id>/`        | GET | Get specific suggestion | Yes              |
| `/api/suggestions/<id>/approve` | PATCH | Approve suggestion → auto-update disease metadata | Yes (Admin only) |
| `/api/suggestions/<id>/reject`  | PATCH | Reject user suggestion | Yes (Admin only) |
| `/api/suggestions/<id>/`        | DELETE | Delete suggestion | Yes (Author/Admin only) |

### 4.1 Create Suggestion

**Endpoint:** `/api/suggestions/`  
**Method:** `POST`  
**Description:** Submit a community suggestion for disease treatment/prevention.  
**Auth Required:** Yes

#### Request Body:
```json
{
  "user": 2,
  "disease": 1,
  "type": "treatment",
  "suggestion": "Apply copper-based fungicide every 14 days during humid conditions."
}
```

#### cURL Example:
```bash
curl -X POST http://127.0.0.1:8000/api/suggestions/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_access_token" \
  -d '{"user": 2, "disease": 1, "type": "treatment", "suggestion": "Apply copper-based fungicide every 14 days."}' \
  | jq
```

#### Response (201 Created):
```json
{
  "id": 1,
  "disease": {
    "id": 1,
    "name": "Northern Corn Leaf Blight"
  },
  "user": 1,
  "type": "treatment",
  "suggestion": "Apply copper-based fungicide every 14 days during humid conditions.",
  "status": "pending",
  "created_at": "2024-01-15T12:00:00Z"
}
```

---

### 4.2 List Suggestions

**Endpoint:** `/api/suggestions/`  
**Method:** `GET`  
**Description:** Get community suggestions.  
**Auth Required:** Yes (Admins see all, farmers see theirs)

#### Query Parameters:
- `status`: Filter by status (`pending`, `approved`, `rejected`)
- `type`: Filter by type (`cause`, `prevention`, `treatment`)
- `disease`: Filter by disease ID

#### cURL Example:
```bash
curl -X GET "http://127.0.0.1:8000/api/suggestions/?status=approved&type=treatment" | jq
```

#### Response (200 OK):
```json
[
  {
    "id": 1,
    "disease": {
      "id": 1,
      "name": "Northern Corn Leaf Blight"
    },
    "user": 1,
    "type": "treatment",
    "suggestion": "Apply copper-based fungicide every 14 days during humid conditions.",
    "status": "approved",
    "created_at": "2024-01-15T12:00:00Z"
  }
]
```

---

### 4.3 Approve Suggestion

**Endpoint:** `/api/suggestions/<id>/approve`  
**Method:** `PATCH`  
**Description:** Approve a pending suggestion. Updates the suggestion’s status to approved.
Applies the suggestion content to the related disease metadata (e.g. adds it to treatments or prevention guidance)  
**Auth Required:** Yes (Admins ONLY)



#### cURL Example:
```bash
curl -X PATCH http://127.0.0.1:8000/api/suggestions/1/approve/ \
  -H "Authorization: Bearer your_access_token" \
  | jq
```


#### Response (200 OK):
```json
{
    "detail": "Suggestion approved and merged into disease metadata"
}
```
---

### 4.4 Reject Suggestion

**Endpoint:** `/api/suggestions/<id>/reject`  
**Method:** `PATCH`  
**Description:** Reject a pending suggestion. Updates the suggestion’s status to rejected  
**Auth Required:** Yes (Admins ONLY)



#### cURL Example:
```bash
curl -X PATCH http://127.0.0.1:8000/api/suggestions/1/reject/ \
  -H "Authorization: Bearer your_access_token" \
  | jq

```


#### Response (200 OK):
```json
{
    "detail": "Suggestion rejected"
}
```
---


## 🔗 Related Resources

- **CNN Model Training Repository**: https://github.com/deninjo/Leaf-Lens
- **API Documentation**: http://127.0.0.1:8000/api/docs/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request





---

**Built with ❤️ for sustainable agriculture and AI-powered farming solutions.**