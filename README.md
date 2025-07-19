# 🏭 Cement Corporation of India Limited - Official Website
This project is the official website for Cement Corporation of India Limited (CCI), a Government of India Enterprise. It's built using Flask and designed with modern web technologies to provide a comprehensive and engaging experience for all stakeholders, including customers, partners, and employees.

The website features company information, news updates, tender listings, details about manufacturing plants, a contact form, and a secure user authentication system with separate dashboards for regular users and administrators.

-----

## ✨ Features

### Public Access:

  * **Home Page**: Engaging hero section, key statistics (Years of Excellence, Capacity, Plants, Employees), "About CCI" overview, latest news & updates, manufacturing plant highlights, and current tenders snapshot.
  * **About Us**: Detailed company history, key milestones, vision, mission, core values, achievements, and quality certifications.
  * **Board of Directors**: Information on the leadership team, including their qualifications and experience.
  * **Our Plants**: Interactive map highlighting plant locations across India, detailed information about each manufacturing unit (capacity, established year, status), and production statistics.
  * **Tenders**: Comprehensive listing of current tenders, categorized Browse (open, archive, terms), search and filter functionalities, and an e-Tender Helpdesk.
  * **Contact Us**: Head office and regional office contact details, a dynamic contact form for inquiries, important links, emergency contact, and a FAQ section.

### User & Admin Features:

  * **User Registration**: Secure new user account creation.
  * **User Login**: Authenticated access for registered users and administrators.
  * **User Dashboard**: Personalized dashboard for logged-in users, displaying recent tenders, latest news, account status, and quick action links.
  * **Admin Dashboard**: Dedicated dashboard for administrators with statistics on total tenders, messages, users, and news.
  * **Admin News Management**: CRUD (Create, Read, Update, Delete) operations for news updates by administrators.
  * **Admin User Management**: Admin can view, promote, and delete user accounts.
  * **Admin Tender Management**: Admin can view and manage tender listings.
  * **Admin Message Management**: Admin can view and mark contact messages as read.
  * **Responsive Design**: Built with Tailwind CSS for a modern, mobile-first, and responsive user interface.
  * **Animations**: Utilizes AOS (Animate On Scroll) for engaging scroll animations and custom CSS animations.
  * **Flash Messages**: Provides informative feedback to users for various actions (success, error, info).

-----

## 🛠️ Installation & Setup

### Prerequisites

  * **Python 3.7+**
  * **`pip`** (Python package installer)

### Steps

1.  **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd CCI_website
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Initialize the Database and Create Sample Data:**
    The `app.py` script automatically initializes an SQLite database (`cci_website.db`) and populates it with sample data (including an admin user and a regular user) if no admin user exists.

    ```bash
    python app.py
    ```

    You will see messages in your terminal indicating that sample data has been created.

      * **Admin Credentials**: `username='admin'`, `password='admin123'`
      * **User Credentials**: `username='testuser'`, `password='user123'`
      * You can also quickly log in as admin by visiting `/demo-admin` in your browser.

5.  **Run the Application:**

    ```bash
    python app.py
    ```

    The application will run on `http://127.0.0.1:5000` (or `http://0.0.0.0:5000` if `host='0.0.0.0'` is specified).

-----

## 💡 Usage

### Public Access:

Navigate to `http://127.0.0.1:5000` in your web browser. Explore the Home, About Us, Board of Directors, Plants, Tenders, and Contact Us pages using the navigation bar.

### User Access:

1.  **Register**: Go to `/register` to create a new user account.
2.  **Login**: Use your registered credentials (or `testuser`/`user123`) at `/login` to log in.
3.  **User Dashboard**: After logging in, you'll be redirected to `/user-dashboard` to see your personalized overview.

### Admin Access:

1.  **Login as Admin**: Use the pre-created admin credentials (`admin`/`admin123`) or visit `/demo-admin` to log in quickly.
2.  **Admin Dashboard**: After logging in as admin, you'll be redirected to `/admin`.
3.  **Admin Management**: From the admin dashboard, you can navigate to manage:
      * `/admin/news`: Add, edit, and delete news updates.
      * `/admin/tenders`: View and manage tenders.
      * `/admin/messages`: View contact messages.
      * `/admin/users`: View, promote, or delete user accounts.
      * `/admin/create-admin`: (Only accessible if no admin exists initially) Create a custom admin account.

-----

## 📁 Project Structure

```
.
├── app.py                  # Main Flask application file, handles routes, database, forms.
├── instance/               # Flask instance folder (contains sqlite database 'cci_website.db')
│   └── cci_website.db
├── static/                 # Static files (CSS, JS, images)
│   ├── css/                # Potentially for custom CSS, though Tailwind is CDN-linked
│   ├── js/                 # Potentially for custom JS
│   └── images/
│       └── image.png       # Company logo used in header
│       └── ...             # Other images if added later
├── templates/              # Jinja2 HTML templates for the website pages
│   ├── admin/              # Templates specific to admin functionalities
│   │   ├── dashboard.html
│   │   ├── news.html
│   │   ├── add_news.html
│   │   ├── edit_news.html
│   │   ├── messages.html
│   │   └── users.html
│   ├── about.html          # About Us page
│   ├── base.html           # Base template for common layout (header, footer, scripts, styles)
│   ├── board_of_directors.html # Board of Directors page
│   ├── contact.html        # Contact Us page with form
│   ├── create_admin.html   # Initial admin creation page
│   ├── index.html          # Home page
│   ├── login.html          # User login page
│   ├── plants.html         # Our Manufacturing Plants page
│   ├── register.html       # User registration page
│   └── tenders.html        # Tenders section
└── README.md               # This file
```

-----

## 📝 Forms & Models

The application uses `Flask-WTF` for form handling and `Flask-SQLAlchemy` for database management.

### Database Models (`app.py`)

  * `User`: Stores user credentials, email, and admin status.
  * `NewsUpdate`: Stores news articles (title, content, author, date).
  * `Tender`: Stores tender details (title, description, tender number, dates, cost, location, status).
  * `ContactMessage`: Stores messages submitted via the contact form.
  * `Plant`: Stores details about manufacturing plants.
  * `BoardMember`: Stores information about the board members.

### Forms (`app.py`)

  * `ContactForm`: For the contact us page.
  * `LoginForm`: For user login.
  * `RegisterForm`: For new user registration.
  * `TenderForm`: For admin to add/edit tenders.
  * `NewsForm`: For admin to add/edit news updates.

-----

## 🔗 External Libraries & Frameworks

  * **Flask**: Python web framework.
  * **Flask-SQLAlchemy**: ORM for database interactions.
  * **Flask-WTF**: Integration for WTForms to handle web forms.
  * **Werkzeug**: Utilities for password hashing.
  * **Tailwind CSS**: Utility-first CSS framework (linked via CDN in `base.html`).
  * **AOS (Animate On Scroll)**: JavaScript library for scroll animations (linked via CDN in `base.html`).
  * **Font Awesome**: Icon library (linked via CDN in `base.html`).
  * **Google Fonts (Inter)**: For typography.

-----

## 🤝 Contributing

We welcome contributions to improve the CCI website\!

1.  **Fork** the repository.
2.  **Create** a new branch (`git checkout -b feature/your-feature-name`).
3.  **Implement** your changes.
4.  **Write** tests for new features (if applicable, though not explicitly in provided files, it's good practice).
5.  **Ensure** the code adheres to style guidelines.
6.  **Commit** your changes (`git commit -m 'feat: Add new feature X'`).
7.  **Push** to the branch (`git push origin feature/your-feature-name`).
8.  **Open** a Pull Request.

-----

## 📄 License

This project is open-source and available under the [MIT License](https://www.google.com/search?q=LICENSE).

-----

## 📞 Contact

For any questions or inquiries, please open an issue on the GitHub repository, or use the contact form on the website.

-----
