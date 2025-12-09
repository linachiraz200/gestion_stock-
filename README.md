# 📦 Django Stock Management System

A comprehensive **enterprise-grade inventory management system** built with Django 5.1.3, featuring advanced product management, client tracking, supplier management, invoice generation with PDF export, automated stock alerts, and global search functionality.

## 🚀 What This Project Does

This system helps businesses manage their entire inventory workflow:

- **📊 Real-time Stock Monitoring** - Track product quantities with automated low-stock alerts
- **🏷️ Product Categorization** - Organize products with categories and advanced filtering
- **👥 Customer & Supplier Management** - Complete CRM for clients and suppliers
- **📄 Professional Invoice Generation** - Create and export invoices as PDF documents
- **🔍 Global Search** - Find anything across products, clients, suppliers, and invoices
- **📧 Automated Notifications** - Email alerts for low stock and critical inventory levels
- **📈 Business Analytics** - Dashboard with key metrics and stock insights
- **🔐 Enterprise Security** - Role-based access, secure authentication, and data protection

## ✨ Key Features

### Core Functionality
✅ **Advanced Product Management** - Categories, filtering, stock tracking, and bulk operations  
✅ **Client & Supplier CRM** - Complete contact management with relationship tracking  
✅ **Professional Invoice System** - Generate, print, and export invoices as PDF  
✅ **Stock Alert System** - Automated email notifications for low stock levels  
✅ **Global Search Engine** - Search across all data with intelligent filtering  
✅ **Real-time Dashboard** - Key metrics, alerts, and business insights  

### Technical Features
✅ **Dual Database Support** - SQLite for development, MongoDB Atlas for production  
✅ **PDF Generation** - Professional invoice PDFs with ReportLab  
✅ **Email Notifications** - SMTP integration for automated alerts  
✅ **Responsive Design** - Mobile-friendly interface with dark mode  
✅ **Enterprise Security** - CSRF protection, secure sessions, environment-based config  
✅ **CI/CD Pipeline** - Automated testing, security scanning, and deployment  
✅ **Docker Ready** - Complete containerization for easy deployment

## 📁 Project Structure

```
gestion_stock-/
├── gestion_stock/          # Main Django project
├── core/                   # Core utilities (search, alerts, notifications)
├── produits/               # Product management app
├── clients/                # Client management app
├── fournisseurs/           # Supplier management app
├── factures/               # Invoice management app
├── templates/              # HTML templates with responsive design
├── static/                 # CSS, JavaScript, images
├── .github/workflows/      # CI/CD pipeline configuration
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose setup
├── Makefile              # Development automation
└── pyproject.toml        # Code quality configuration
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+ (Docker uses Python 3.11 for compatibility)
- Docker & Docker Compose (Recommended)
- Git

### 1. Clone & Setup
```bash
git clone https://github.com/linachiraz200/gestion_stock-.git
cd gestion_stock-

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration
```bash
cp .env.example .env
# Edit .env with your settings (see Configuration section)
```

### 3. Database Setup
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 4. Run Development Server

**Option A: Docker (Recommended)**
```bash
docker-compose up --build
```
Visit: `http://localhost:8080`

**Option B: Local Development**
```bash
python manage.py runserver
```
Visit: `http://localhost:8000`

## ⚙️ Configuration

### Database Options

**Option 1: SQLite (Recommended for Development)**
```env
USE_MONGODB=False
```

**Option 2: MongoDB Atlas (Production)**
```env
USE_MONGODB=True
MONGO_CONNECTION_STRING=mongodb+srv://username:password@cluster.mongodb.net/dbname
MONGO_DB_NAME=gestion_stock
```

### Essential Environment Variables
```env
# Security
SECRET_KEY=your-secure-secret-key-here
DEBUG=True  # Set to False in production
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com

# Stock Management
LOW_STOCK_THRESHOLD=5
PAGINATION_SIZE=10

# Email Notifications
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=gestionstock@yourdomain.com
```

## 🛠️ Essential Commands

### Development Commands
```bash
# Run development server
python manage.py runserver

# Create database migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Run tests
python manage.py test

# Check for low stock and send alerts
python manage.py check_stock --send-email
```

### Using Makefile (Recommended)
```bash
# Set up development environment
make setup-dev

# Run all quality checks
make quality

# Run tests with coverage
make test-coverage

# Format code
make format

# Run security checks
make security

# Build Docker image
make docker-build

# Run full CI pipeline locally
make ci
```

### Docker Commands
```bash
# Build and run with Docker Compose
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop containers
docker-compose down
```

## 🌐 Application URLs

### Docker (Port 8080)
- **Admin Panel**: http://localhost:8080/admin/
- **Dashboard**: http://localhost:8080/dashboard/
- **Products**: http://localhost:8080/produits/
- **Clients**: http://localhost:8080/clients/
- **Suppliers**: http://localhost:8080/fournisseur/
- **Invoices**: http://localhost:8080/factures/
- **Global Search**: http://localhost:8080/core/search/
- **Stock Alerts**: http://localhost:8080/core/alerts/

### Local Development (Port 8000)
- **Admin Panel**: http://localhost:8000/admin/
- **Dashboard**: http://localhost:8000/dashboard/
- **Products**: http://localhost:8000/produits/
- **Clients**: http://localhost:8000/clients/
- **Suppliers**: http://localhost:8000/fournisseur/
- **Invoices**: http://localhost:8000/factures/

### API Endpoints
- **Export Products CSV**: `/produits/export/csv/`
- **Generate Invoice PDF**: `/factures/{id}/pdf/`

## 📊 Usage Examples

### Stock Management Workflow
1. **Add Products** with categories and initial stock
2. **Set Stock Thresholds** for automated alerts
3. **Create Invoices** for sales transactions
4. **Monitor Dashboard** for real-time insights
5. **Receive Email Alerts** when stock runs low

### Search & Filter
- **Global Search**: Search across all entities
- **Product Filtering**: By category, stock level, price range
- **Invoice Search**: By number, client, date range

### Automated Alerts
```bash
# Manual stock check
python manage.py check_stock

# Send email notifications
python manage.py check_stock --send-email

# Set up daily automated checks (cron)
0 9 * * * cd /path/to/project && python manage.py check_stock --send-email
```

## 🔧 Development

### Code Quality
```bash
# Run linting
flake8 .

# Format code
black .
isort .

# Security scan
bandit -r .
safety check
```

### Testing
```bash
# Run all tests
python manage.py test

# Run with coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

## 🚀 Deployment

### Production Checklist
- [ ] Set `DEBUG=False`
- [ ] Configure secure `SECRET_KEY`
- [ ] Set up production database (MongoDB Atlas)
- [ ] Configure email settings
- [ ] Set up SSL certificates
- [ ] Configure static file serving
- [ ] Set up automated backups
- [ ] Configure monitoring and logging

### Docker Deployment
```bash
# Production build
docker build -t gestion-stock .

# Run with environment variables
docker run -p 8000:8000 \
  -e DEBUG=False \
  -e SECRET_KEY=your-production-key \
  -e USE_MONGODB=True \
  gestion-stock
```

## 📈 Monitoring & Maintenance

### Stock Alerts Setup
```bash
# Add to crontab for daily alerts at 9 AM
crontab -e
0 9 * * * cd /path/to/project && python manage.py check_stock --send-email
```

### Database Maintenance
```bash
# Backup SQLite database
cp db.sqlite3 backup_$(date +%Y%m%d).sqlite3

# MongoDB backup (if using Atlas)
# Use MongoDB Atlas backup features
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Run quality checks (`make quality`)
4. Commit changes (`git commit -m 'Add amazing feature'`)
5. Push to branch (`git push origin feature/amazing-feature`)
6. Open Pull Request

## 📋 Requirements & Dependencies

### System Requirements
- **Python**: 3.11+ (3.14 has compatibility issues with Django admin)
- **Docker**: Latest version (recommended for deployment)
- **Git**: For version control
- **Memory**: Minimum 512MB RAM
- **Storage**: 100MB+ free space

### Python Dependencies (requirements.txt)

#### Core Framework
```
django==5.1.3          # Main web framework for building the application
asgiref==3.8.1         # ASGI server reference implementation for Django
sqlparse==0.5.2        # SQL parser for Django ORM query processing
tzdata==2025.2         # Timezone database for handling date/time operations
pytz==2024.2           # Python timezone library for accurate time handling
```

#### Database Support
```
mongoengine==0.27.0    # Object Document Mapper (ODM) for MongoDB integration
pymongo==4.6.1        # Official MongoDB driver for Python connections
dnspython==2.4.2       # DNS toolkit required for MongoDB Atlas connections
```

#### PDF Generation
```
reportlab==4.0.7       # Professional PDF generation library for invoices
weasyprint==61.2       # HTML/CSS to PDF converter for advanced layouts
```

#### Production & Utilities
```
gunicorn==21.2.0       # Production-ready WSGI HTTP server for deployment
python-dotenv==1.0.1   # Environment variable management from .env files
```

### Installation
```bash
# Install all dependencies
pip install -r requirements.txt

# Or install core packages individually
pip install django==5.1.3 mongoengine==0.27.0 reportlab==4.0.7
```

## 🔒 Security

- CSRF protection enabled
- Secure session configuration
- Environment-based secrets
- SQL injection prevention
- XSS protection headers
- Secure password validation

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Troubleshooting

### Common Issues

**Python 3.14 Compatibility**
- Use Docker (Python 3.11) for best compatibility
- Local development may have admin panel issues with Python 3.14

**Port Conflicts**
- Docker uses port 8080 to avoid conflicts
- Stop other services using ports 8000/8080 if needed

**Database Issues**
- Delete `db_new.sqlite3` and run `python manage.py migrate` to reset
- Check Docker logs: `docker-compose logs -f`

**Missing Dependencies**
- Run `pip install -r requirements.txt` to install all dependencies
- For WeasyPrint issues on Windows, install GTK+ libraries

### Getting Help

1. Check the [Issues](https://github.com/linachiraz200/gestion_stock-/issues) page
2. Review Docker logs for error details
3. Ensure all prerequisites are installed
4. Try the Docker approach if local development fails

---

**Built with ❤️ using Django 5.1.3 and modern web technologies**cense

This project is licensed under the MIT License - see LICENSE file for details.

## 👨‍💻 Author

**Lina Chiraz** - [GitHub Profile](https://github.com/linachiraz200)

## 🙏 Acknowledgments

- Django community for the excellent framework
- MongoDB team for Atlas cloud database
- ReportLab for PDF generation capabilities
- All contributors and users

---

**Last Updated**: December 1, 2025  
**Version**: 2.0.0 - Enterprise Edition
