# Django CTF Blog & Writeup Platform

A Django-based blog application designed for hosting CTF (Capture The Flag) writeups and personal blog posts. This platform allows you to write content in Markdown format and display it beautifully on the web.

## Features

- 📝 **Markdown Support** - Write posts in Markdown with full syntax support
- 🚩 **CTF Writeups** - Perfect for documenting security challenges and solutions
- 📚 **Category Organization** - Organize posts by categories (CTF Writeup, Tutorial, Blog Post, etc.)
- 🎨 **Clean UI** - Modern, responsive design that works on all devices
- 🔍 **Code Highlighting** - Syntax highlighting for code blocks
- 📊 **Admin Interface** - Easy content management through Django admin
- 🔖 **SEO Friendly** - Clean URLs and proper meta information

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Scirtor/django-project.git
   cd django-project
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables (optional)**
   ```bash
   cp .env.example .env
   # Edit .env and set your SECRET_KEY for production
   ```
   For production, generate a new secret key:
   ```bash
   python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to create your admin account.

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Website: http://localhost:8000
   - Admin panel: http://localhost:8000/admin

## Usage

### Creating Posts

1. Navigate to the admin panel at http://localhost:8000/admin
2. Log in with your superuser credentials
3. Click on "Posts" → "Add Post"
4. Fill in the details:
   - **Title**: Your post title
   - **Slug**: Auto-generated from title (can be customized)
   - **Content**: Write your content in Markdown
   - **Excerpt**: Short description for the post list
   - **Category**: Choose or create a category
   - **Published**: Check to make the post visible

### Markdown Features

The platform supports full Markdown syntax including:

- **Headers** (# H1, ## H2, etc.)
- **Code blocks** with syntax highlighting
- **Tables**
- **Lists** (ordered and unordered)
- **Links** and images
- **Blockquotes**
- **Inline code**

Example Markdown post:

```markdown
# My CTF Writeup

## Challenge Description

This was a web exploitation challenge...

### Solution

The vulnerability was in the login form:

\`\`\`python
payload = "admin' OR '1'='1' --"
\`\`\`

## Flag

CTF{example_flag_here}
```

### Categories

Organize your content with categories like:
- CTF Writeup
- Tutorial
- Blog Post
- Security Research
- Tool Review

### Viewing Posts

- **All posts**: http://localhost:8000
- **By category**: http://localhost:8000/category/CTF%20Writeup/
- **Individual post**: http://localhost:8000/post/your-post-slug/

## Project Structure

```
django-project/
├── blog/                      # Main blog application
│   ├── migrations/           # Database migrations
│   ├── templates/            # HTML templates
│   │   └── blog/
│   │       ├── base.html     # Base template
│   │       ├── post_list.html    # List view
│   │       └── post_detail.html  # Detail view
│   ├── models.py             # Post model
│   ├── views.py              # View logic
│   ├── admin.py              # Admin configuration
│   └── urls.py               # URL routing
├── ctf_blog/                 # Project settings
│   ├── settings.py           # Django settings
│   └── urls.py               # Main URL configuration
├── static/                   # Static files (CSS, JS, images)
├── manage.py                 # Django management script
└── requirements.txt          # Python dependencies
```

## Customization

### Changing the Theme

Edit the CSS in `blog/templates/blog/base.html` to customize colors, fonts, and layout.

### Adding New Features

The modular structure makes it easy to extend:
- Add new models in `blog/models.py`
- Create new views in `blog/views.py`
- Add templates in `blog/templates/blog/`

## Deployment

For production deployment:

1. **Configure environment variables**
   
   Set these environment variables in your production environment:
   ```bash
   export DJANGO_SECRET_KEY='your-secure-secret-key'
   export DJANGO_DEBUG='False'
   export DJANGO_ALLOWED_HOSTS='yourdomain.com,www.yourdomain.com'
   ```
   
   Or use a `.env` file (not recommended for production, use your platform's secret management):
   ```bash
   cp .env.example .env
   # Edit .env with production values
   ```

2. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

3. **Use a production server** (gunicorn, uWSGI, etc.)
   ```bash
   pip install gunicorn
   gunicorn ctf_blog.wsgi:application
   ```

4. **Set up a reverse proxy** (nginx, Apache)

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## License

This project is open source and available for personal and educational use.

## Support

For questions or issues:
- Open an issue on GitHub
- Contact the maintainer

---

Built with ❤️ and Django for the CTF community

