# 🛕 Alayatales - Temple Management System

**Alayatales** is a comprehensive temple management system designed to preserve and share the rich heritage of sacred temples. Built with modern web technologies, it provides a user-friendly platform for documenting, managing, and exploring temples worldwide.

## ✨ Features

### 🏛️ Temple Management
- **Add New Temples**: Comprehensive form with image upload support
- **Edit Temple Information**: Update details, timings, and images
- **Delete Temples**: Secure deletion with confirmation
- **Image Gallery**: High-quality photos with automatic compression
- **Smart Search**: Find temples by name, location, or description
- **Advanced Filtering**: Sort by name, location, or date added

### 👥 User Management
- **Secure Authentication**: Email/password login with hashed passwords
- **Role-Based Access**: Admin and regular user roles
- **User Profiles**: Personal account management
- **Password Management**: Secure password updates

### 📊 Admin Dashboard
- **Statistics Overview**: Temple and user metrics
- **Visual Analytics**: Charts and graphs using Plotly
- **User Management**: Promote/demote users, view user details
- **Temple Management**: Bulk operations and quick actions
- **Data Export**: JSON export for temples and users
- **System Settings**: Application configuration and maintenance

### 🔍 Search & Discovery
- **Global Search**: Search across all temple data
- **Location Filtering**: Browse temples by location
- **Featured Temples**: Highlighted temples on homepage
- **Recent Additions**: Latest temples added to the system

### 📱 User Experience
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Intuitive Navigation**: Easy-to-use sidebar navigation
- **Real-time Updates**: Instant feedback and notifications
- **Image Optimization**: Automatic compression and resizing
- **Progress Indicators**: Visual feedback for operations

## 🚀 Technology Stack

### Backend
- **Python 3.8+**: Core programming language
- **MongoDB**: NoSQL database for flexible data storage
- **PyMongo**: MongoDB driver for Python

### Frontend
- **Streamlit**: Modern web framework for Python
- **Streamlit-Option-Menu**: Enhanced navigation components
- **HTML/CSS**: Custom styling and layouts

### Image Processing
- **Pillow (PIL)**: Image manipulation and compression
- **Base64 Encoding**: Efficient image storage

### Data Visualization
- **Plotly**: Interactive charts and graphs
- **Pandas**: Data manipulation and analysis

### Security
- **Hashlib**: Password hashing (SHA-256)
- **Secrets**: Secure token generation
- **Session Management**: User authentication state

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- MongoDB (local installation or MongoDB Atlas)
- Git (for cloning the repository)

### Step 1: Clone the Repository
```bash
git clone https://github.com/your-username/alayatales.git
cd alayatales
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Set Up Environment Variables
1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` file with your configuration:
```env
# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017/
DB_NAME=alayatales

# Demo Mode (set to 'true' to use mock data)
DEMO_MODE=false

# Application Settings
APP_SECRET_KEY=your-secret-key-here
ADMIN_EMAIL=admin@alayatales.com
ADMIN_PASSWORD=Admin@123

# File Upload Settings
MAX_UPLOAD_SIZE=5
MAX_IMAGES_PER_TEMPLE=5
ALLOWED_IMAGE_TYPES=png,jpg,jpeg,gif,webp
IMAGE_COMPRESSION_QUALITY=85
MAX_IMAGE_DIMENSION=800

# Feature Flags
ENABLE_REGISTRATION=true
ENABLE_PUBLIC_VIEW=true
ENABLE_IMAGE_UPLOAD=true
```

### Step 4: Set Up MongoDB

#### Option A: Local MongoDB
1. Install MongoDB Community Edition
2. Start MongoDB service:
```bash
# Windows
net start MongoDB

# macOS
brew services start mongodb-community

# Linux
sudo systemctl start mongod
```

#### Option B: MongoDB Atlas (Cloud)
1. Create a free account at [MongoDB Atlas](https://www.mongodb.com/atlas)
2. Create a new cluster
3. Get your connection string
4. Update `MONGODB_URI` in `.env` file

### Step 5: Run the Application
```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## 🎯 Usage

### First Time Setup
1. **Access the Application**: Open your browser and go to `http://localhost:8501`
2. **Register an Admin Account**: Click "Register" and create an admin account
3. **Login**: Use your credentials to log in
4. **Add Your First Temple**: Go to "Add Temple" and create your first entry

### For Regular Users
- **Browse Temples**: Use "All Temples" to explore the collection
- **Search**: Use the search bar to find specific temples
- **View Details**: Click "View Details" on any temple card
- **Create Account**: Register to access additional features

### For Administrators
- **Admin Dashboard**: Access comprehensive statistics and management tools
- **Add Temples**: Create new temple entries with images
- **Manage Users**: View, promote, or manage user accounts
- **Export Data**: Download temple and user data
- **System Settings**: Configure application settings

## 🛠️ Configuration

### Environment Variables
The application uses environment variables for configuration. Key settings include:

- `MONGODB_URI`: Database connection string
- `DB_NAME`: Database name
- `DEMO_MODE`: Enable demo mode with mock data
- `MAX_UPLOAD_SIZE`: Maximum file size for images (MB)
- `MAX_IMAGES_PER_TEMPLE`: Maximum number of images per temple
- `IMAGE_COMPRESSION_QUALITY`: JPEG compression quality (1-100)

### Feature Flags
Enable or disable features using environment variables:
- `ENABLE_REGISTRATION`: Allow new user registration
- `ENABLE_PUBLIC_VIEW`: Allow viewing without login
- `ENABLE_IMAGE_UPLOAD`: Enable image upload functionality

## 📊 Database Schema

### Temples Collection
```json
{
  "_id": "ObjectId",
  "name": "Temple Name",
  "location": "City, State/Country",
  "description": "Detailed description",
  "images": ["base64_encoded_image_1", "base64_encoded_image_2"],
  "timings": {
    "morningOpening": "06:00",
    "morningClosing": "12:00",
    "eveningOpening": "16:00",
    "eveningClosing": "21:00"
  },
  "created_at": "ISODate",
  "updated_at": "ISODate"
}
```

### Users Collection
```json
{
  "_id": "ObjectId",
  "name": "User Name",
  "email": "user@example.com",
  "password": "hashed_password",
  "role": "admin|user",
  "created_at": "ISODate",
  "updated_at": "ISODate"
}
```

## 🔒 Security Features

- **Password Hashing**: SHA-256 hashing for secure password storage
- **Session Management**: Secure session-based authentication
- **Role-Based Access Control**: Different permissions for admin and regular users
- **Input Validation**: Comprehensive validation for all user inputs
- **File Upload Security**: Restricted file types and size limits
- **CSRF Protection**: Built-in protection against cross-site request forgery

## 🚀 Deployment

### Streamlit Cloud
1. Push your code to GitHub
2. Connect your repository to [Streamlit Cloud](https://streamlit.io/cloud)
3. Set up environment variables in Streamlit Cloud dashboard
4. Deploy with one click

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Heroku Deployment
1. Create `Procfile`:
```
web: sh setup.sh && streamlit run app.py
```

2. Create `setup.sh`:
```bash
mkdir -p ~/.streamlit/
echo "[server]" > ~/.streamlit/config.toml
echo "port = $PORT" >> ~/.streamlit/config.toml
echo "enableCORS = false" >> ~/.streamlit/config.toml
echo "headless = true" >> ~/.streamlit/config.toml
```

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### Ways to Contribute
- 📝 **Add Temple Information**: Help document temples in your area
- 🐛 **Report Bugs**: Found an issue? Let us know!
- 💡 **Suggest Features**: Have ideas for improvements?
- 🔧 **Code Contributions**: Submit pull requests for bug fixes or features
- 📚 **Documentation**: Help improve our documentation
- 🌍 **Translations**: Help translate the app to other languages

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Add tests if applicable
5. Commit your changes: `git commit -m "Add feature"`
6. Push to your fork: `git push origin feature-name`
7. Create a pull request

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions small and focused
- Write tests for new features

## 🙏 Acknowledgments

This project was made possible thanks to the amazing open-source community and the following technologies:

### Core Technologies
- **[Streamlit](https://streamlit.io/)** - For the incredible web framework that makes Python web apps simple
- **[MongoDB](https://www.mongodb.com/)** - For reliable and scalable NoSQL database
- **[Python](https://www.python.org/)** - For the powerful and versatile programming language

### Libraries and Frameworks
- **[Pillow (PIL)](https://pillow.readthedocs.io/)** - For advanced image processing capabilities
- **[Plotly](https://plotly.com/)** - For beautiful and interactive data visualizations
- **[PyMongo](https://pymongo.readthedocs.io/)** - For seamless MongoDB integration
- **[Pandas](https://pandas.pydata.org/)** - For powerful data manipulation and analysis
- **[Streamlit-Option-Menu](https://github.com/victoryhb/streamlit-option-menu)** - For enhanced navigation components

### Special Thanks
- **🌟 Open Source Community** - For countless libraries, tools, and inspiration
- **🏛️ Temple Authorities** - For preserving our cultural and spiritual heritage
- **👨‍💻 Developers** - Who contribute code, report bugs, and suggest improvements
- **🙏 Users** - Who help document temples and share their knowledge
- **📚 Documentation Writers** - For creating guides and tutorials
- **🌍 Cultural Preservationists** - For their dedication to heritage conservation

### Inspiration
This project is inspired by the need to preserve and share the rich cultural heritage of temples worldwide. We believe that technology can play a crucial role in documenting and celebrating our spiritual and architectural treasures.

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### MIT License Summary
- ✅ Commercial use
- ✅ Modification
- ✅ Distribution
- ✅ Private use
- ❌ Liability
- ❌ Warranty

## 📞 Support

### Getting Help
- 📖 **Documentation**: Check this README and inline code comments
- ❓ **FAQ**: Visit the Help page in the application
- 🐛 **Issues**: Report bugs on GitHub Issues
- 💬 **Discussions**: Join community discussions on GitHub

### Contact Information
- **Project Maintainer**: Temple Heritage Team
- **Email**: support@alayatales.com
- **GitHub**: [https://github.com/your-username/alayatales](https://github.com/your-username/alayatales)

## 🗺️ Roadmap

### Version 1.1 (Upcoming)
- [ ] Multi-language support
- [ ] Advanced search filters
- [ ] Temple categories and tags
- [ ] User favorites and bookmarks
- [ ] Email notifications
- [ ] API endpoints for external integrations

### Version 1.2 (Future)
- [ ] Mobile app (React Native)
- [ ] Offline mode support
- [ ] Advanced analytics dashboard
- [ ] Social features (comments, ratings)
- [ ] Integration with mapping services
- [ ] Bulk import/export tools

### Long-term Vision
- [ ] AI-powered temple recognition
- [ ] Virtual temple tours
- [ ] Community-driven content moderation
- [ ] Integration with cultural heritage organizations
- [ ] Educational resources and guides
- [ ] Multi-tenant support for organizations

## 📈 Statistics

- **Version**: 1.0.0
- **Language**: Python
- **Framework**: Streamlit
- **Database**: MongoDB
- **License**: MIT
- **Status**: Active Development

---

**Made with ❤️ for preserving temple heritage**

*© 2024 Temple Heritage Team. All rights reserved.*

---

### Quick Links
- [Installation Guide](#-installation)
- [User Guide](#-usage)
- [API Documentation](docs/api.md)
- [Contributing Guidelines](#-contributing)
- [License](LICENSE)
- [Changelog](CHANGELOG.md)