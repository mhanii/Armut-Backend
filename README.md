# Armut Backend API

This is the Django backend API for the Armut e-commerce platform, deployed on Vercel.

## Features

- Product management
- Store management
- User authentication
- Shopping cart functionality
- Image serving
- Search functionality
- Category management

## API Endpoints

- `GET /api/health/` - Health check endpoint
- `GET /api/products/` - List all products
- `GET /api/products/<id>/` - Get product details
- `GET /api/banners` - Get banner images
- `GET /api/discount` - Get discount information
- `GET /api/search/` - Search products
- `GET /api/category/<slug>/` - Get products by category
- `GET /api/stores/` - List all stores
- `GET /api/categories/` - List all categories

## Deployment on Vercel

### Prerequisites

1. Vercel account
2. Git repository with your code
3. PostgreSQL database (recommended for production)

### Environment Variables

Set these environment variables in your Vercel project:

- `DEBUG`: Set to "False" for production
- `DATABASE_URL`: Your PostgreSQL connection string (if using external database)
- `SECRET_KEY`: Django secret key (generate a new one for production)

### Deployment Steps

1. **Connect your repository to Vercel:**
   - Go to Vercel dashboard
   - Click "New Project"
   - Import your Git repository

2. **Configure build settings:**
   - Framework Preset: Other
   - Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - Output Directory: `staticfiles`
   - Install Command: `pip install -r requirements.txt`

3. **Set environment variables:**
   - Add all required environment variables in Vercel dashboard

4. **Deploy:**
   - Click "Deploy" and wait for the build to complete

### Local Development

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Run migrations: `python manage.py migrate`
6. Start the development server: `python manage.py runserver`

### Database

The project is configured to use SQLite for local development and PostgreSQL for production. To use PostgreSQL locally, update the DATABASES setting in `main/settings.py`.

### Static Files

Static files are served using WhiteNoise middleware. Make sure to run `python manage.py collectstatic` before deployment.

## Frontend Integration

The frontend is deployed separately at: `https://armut-frontend.vercel.app`

CORS is configured to allow requests from the frontend domain.

## Security Notes

This is a development deployment. For production, consider:

- Using environment variables for sensitive data
- Implementing proper authentication
- Setting up HTTPS
- Configuring proper CORS settings
- Using a production database
- Setting up proper logging and monitoring 