# Data Nexa

A SaaS data profiling tool that analyzes CSV/Excel files and provides AI-powered insights. Built with FastAPI backend and React frontend.

## 🚀 Features

- 📊 **File Analysis**: Upload and analyze CSV/Excel files
- 🔍 **Data Profiling**: Automated data quality assessment
- 🤖 **AI Insights**: Groq-powered intelligent recommendations
- 🔐 **Authentication**: JWT-based secure access
- 🏢 **Multi-tenant**: Workspace-based organization
- ⚡ **High Performance**: Async FastAPI + React with Vite

## 🛠 Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL with SQLAlchemy 2.0 (async)
- **AI**: Groq API (Llama 3.1 70B)
- **Authentication**: JWT tokens with bcrypt
- **Data Processing**: Pandas, OpenPyXL
- **Code Quality**: Black, isort, mypy, pytest

### Frontend
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **State Management**: Zustand
- **HTTP Client**: Axios
- **Charts**: Chart.js / Recharts

## 📋 Prerequisites

- **Python 3.11+**
- **Node.js 18+**
- **PostgreSQL 14+** (optional - SQLite works for development)
- **Groq API Key** (get from [console.groq.com](https://console.groq.com))

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone <repository-url>
cd Data-Nexa
```

### 2. Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your Groq API key and other settings
```

**Required Environment Variables:**
```env
# Get from console.groq.com
GROQ_API_KEY=gsk_your_groq_api_key_here

# Generate with: openssl rand -hex 32
SECRET_KEY=your_secret_key_here

# Database (SQLite by default, PostgreSQL optional)
# POSTGRES_SERVER=localhost
# POSTGRES_USER=postgres
# POSTGRES_PASSWORD=your_password
# POSTGRES_DB=datanexa
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env
# Edit .env with your backend URL
```

### 4. Run Development Servers

**Backend** (Terminal 1):
```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend** (Terminal 2):
```bash
cd frontend
npm run dev
```

### 5. Access Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 📁 Project Structure

```
Data-Nexa/
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── api/v1/            # API endpoints
│   │   ├── core/              # Security, config, exceptions
│   │   │   └── ai_engine/     # Groq AI integration
│   │   ├── models/            # SQLAlchemy models
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── services/          # Business logic
│   │   ├── utils/             # Utilities
│   │   └── db/                # Database config
│   ├── tests/                 # Backend tests
│   ├── requirements.txt       # Python dependencies
│   └── .env                   # Backend environment
│
├── frontend/                   # React Frontend
│   ├── src/
│   │   ├── components/        # UI components
│   │   ├── pages/             # Route components
│   │   ├── store/             # Zustand stores
│   │   ├── services/          # API calls
│   │   ├── hooks/             # Custom hooks
│   │   └── utils/             # Utilities
│   ├── package.json           # Node dependencies
│   └── .env                   # Frontend environment
│
├── .postman.json              # Postman collection config
├── .kiro/                     # Kiro configuration
└── README.md                  # This file
```

## 🔧 Development

### Backend Commands

```bash
cd backend

# Code formatting
black app/ tests/
isort app/ tests/

# Type checking
mypy app/

# Run tests
pytest tests/ -v

# Database migrations (when available)
alembic upgrade head
```

### Frontend Commands

```bash
cd frontend

# Development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Linting
npm run lint
```

## 🌐 API Endpoints

### AI Insights
- `GET /api/v1/insights/{analysis_id}` - Get insights for analysis
- `GET /api/v1/insights/{analysis_id}/summary` - Get insights summary
- `POST /api/v1/insights/{analysis_id}/generate` - Generate new insights
- `GET /api/v1/insights/stats/tokens` - Get Groq API token usage
- `GET /api/v1/insights/stats/cache` - Get Redis cache statistics

### Health
- `GET /health` - Health check endpoint

## 🤖 AI Integration

Data Nexa uses **Groq** for AI-powered insights:

- **Model**: Llama 3.1 70B Versatile
- **Features**: Data quality analysis, recommendations, code generation
- **Cost**: Very low cost compared to other AI providers
- **Speed**: Ultra-fast inference times

### Getting Groq API Key

1. Visit [console.groq.com](https://console.groq.com)
2. Sign up/login
3. Create an API key
4. Add to your `.env` file: `GROQ_API_KEY=gsk_your_key_here`

## 🐳 Docker Deployment

### Backend
```bash
cd backend
docker build -t datanexa-backend .
docker run -p 8000:8000 --env-file .env datanexa-backend
```

### Frontend
```bash
cd frontend
docker build -t datanexa-frontend .
docker run -p 3000:3000 datanexa-frontend
```

## 🧪 Testing

### Backend Testing
```bash
cd backend
pytest tests/ -v --cov=app
```

### Frontend Testing
```bash
cd frontend
npm run test
```

## 📚 Documentation

- **API Documentation**: http://localhost:8000/docs (Swagger UI)
- **Architecture**: See `backend/docs/` for detailed architecture docs
- **AI Engine**: See `backend/docs/AI_INSIGHTS.md` for AI integration details

## 🤝 Contributing

1. **Code Style**: Follow Black formatting (max line length: 100)
2. **Type Hints**: Add type hints to all Python functions
3. **Documentation**: Write docstrings in Google format
4. **Testing**: Write tests for new features
5. **Architecture**: Use repository pattern for data access

## 📄 License

Proprietary

## 🆘 Troubleshooting

### Common Issues

**Backend won't start:**
- Check if virtual environment is activated
- Verify all environment variables are set
- Ensure Groq API key is valid

**Frontend won't start:**
- Run `npm install` to install dependencies
- Check Node.js version (18+ required)
- Verify backend is running on port 8000

**Database issues:**
- Default uses SQLite (no setup required)
- For PostgreSQL, ensure database exists and credentials are correct

**AI insights not working:**
- Verify Groq API key is set correctly
- Check API key has sufficient credits
- Review backend logs for detailed error messages

### Getting Help

1. Check the logs in both backend and frontend terminals
2. Visit API docs at http://localhost:8000/docs
3. Review environment variable configuration
4. Ensure all dependencies are installed correctly