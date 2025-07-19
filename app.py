from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, FileField, PasswordField, IntegerField, FloatField, BooleanField
from wtforms.validators import DataRequired, Email, Length, NumberRange, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cci_website.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)

# Add moment filter to Jinja2
@app.template_filter('moment')
def moment_filter(datetime_obj):
    """Format datetime object for display"""
    if datetime_obj is None:
        return ''
    return datetime_obj.strftime('%d %B %Y at %I:%M %p')

@app.template_filter('date')
def date_filter(datetime_obj):
    """Format datetime object as date only"""
    if datetime_obj is None:
        return ''
    return datetime_obj.strftime('%d %B %Y')

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class NewsUpdate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    author = db.Column(db.String(100), nullable=False)

class Tender(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    tender_no = db.Column(db.String(50), unique=True, nullable=False)
    opening_date = db.Column(db.DateTime, nullable=False)
    closing_date = db.Column(db.DateTime, nullable=False)
    estimated_cost = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='Open')
    
    def to_dict(self):
        """Convert Tender object to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'tender_no': self.tender_no,
            'opening_date': self.opening_date.isoformat() if self.opening_date else None,
            'closing_date': self.closing_date.isoformat() if self.closing_date else None,
            'estimated_cost': self.estimated_cost,
            'location': self.location,
            'status': self.status
        }

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date_sent = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)

class Plant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    capacity = db.Column(db.Float, nullable=False)
    established_year = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='Operational')

class BoardMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    designation = db.Column(db.String(100), nullable=False)
    qualification = db.Column(db.String(200))
    experience = db.Column(db.Text)
    photo_filename = db.Column(db.String(100))

# Forms
class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired(), Length(min=5, max=200)])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10, max=1000)])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', 
                                   validators=[DataRequired(), EqualTo('password')])

class TenderForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description', validators=[DataRequired()])
    tender_no = StringField('Tender Number', validators=[DataRequired(), Length(max=50)])
    estimated_cost = FloatField('Estimated Cost', validators=[DataRequired(), NumberRange(min=0)])
    location = StringField('Location', validators=[DataRequired(), Length(max=100)])

class NewsForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    content = TextAreaField('Content', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired(), Length(max=100)])

# Routes
@app.route('/')
def index():
    try:
        news_updates = NewsUpdate.query.order_by(NewsUpdate.date_posted.desc()).limit(3).all()
        return render_template('index.html', news_updates=news_updates)
    except Exception as e:
        print(f"Error in index route: {e}")
        return render_template('index.html', news_updates=[])

@app.route('/about')
def about():
    try:
        return render_template('about.html')
    except Exception as e:
        print(f"Error in about route: {e}")
        return f"<h1>About Page</h1><p>Error loading template: {e}</p>"

@app.route('/board-of-directors')
def board_of_directors():
    try:
        board_members = BoardMember.query.all()
        return render_template('board_of_directors.html', board_members=board_members)
    except Exception as e:
        print(f"Error in board_of_directors route: {e}")
        return f"<h1>Board of Directors</h1><p>Error loading template: {e}</p>"

@app.route('/plants')
def plants():
    try:
        plants = Plant.query.all()
        return render_template('plants.html', plants=plants)
    except Exception as e:
        print(f"Error in plants route: {e}")
        return f"<h1>Plants</h1><p>Error loading template: {e}</p>"

@app.route('/tenders')
def tenders():
    try:
        tender_objects = Tender.query.filter_by(status='Open').order_by(Tender.closing_date.asc()).all()
        tenders_dict = [tender.to_dict() for tender in tender_objects]
        return render_template('tenders.html', tenders=tender_objects, tenders_json=tenders_dict)
    except Exception as e:
        print(f"Error in tenders route: {e}")
        return f"<h1>Tenders</h1><p>Error loading template: {e}</p>"

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        try:
            message = ContactMessage(
                name=form.name.data,
                email=form.email.data,
                subject=form.subject.data,
                message=form.message.data
            )
            db.session.add(message)
            db.session.commit()
            flash('Your message has been sent successfully!', 'success')
            return redirect(url_for('contact'))
        except Exception as e:
            print(f"Error saving contact message: {e}")
            flash('Error sending message. Please try again.', 'error')
    try:
        return render_template('contact.html', form=form)
    except Exception as e:
        print(f"Error in contact route: {e}")
        return f"<h1>Contact</h1><p>Error loading template: {e}</p>"

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(username=form.username.data).first()
            if user and check_password_hash(user.password_hash, form.password.data):
                session['user_id'] = user.id
                session['username'] = user.username
                session['is_admin'] = user.is_admin
                flash(f'Welcome back, {user.username}!', 'success')
                
                # Redirect based on user type
                if user.is_admin:
                    return redirect(url_for('admin_dashboard'))
                else:
                    return redirect(url_for('user_dashboard'))
            else:
                flash('Invalid username or password', 'error')
        except Exception as e:
            print(f"Error in login: {e}")
            flash('Login error. Please try again.', 'error')
    try:
        return render_template('login.html', form=form)
    except Exception as e:
        print(f"Error in login route: {e}")
        return f"<h1>Login</h1><p>Error loading template: {e}</p>"

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            # Check if username already exists
            existing_user = User.query.filter_by(username=form.username.data).first()
            if existing_user:
                flash('Username already exists. Please choose a different one.', 'error')
                return render_template('register.html', form=form)
            
            # Check if email already exists
            existing_email = User.query.filter_by(email=form.email.data).first()
            if existing_email:
                flash('Email already registered. Please use a different email.', 'error')
                return render_template('register.html', form=form)
            
            # Create new user
            user = User(
                username=form.username.data,
                email=form.email.data,
                password_hash=generate_password_hash(form.password.data),
                is_admin=False  # Regular users are not admin by default
            )
            
            db.session.add(user)
            db.session.commit()
            
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            print(f"Error in registration: {e}")
            flash('Registration error. Please try again.', 'error')
    
    try:
        return render_template('register.html', form=form)
    except Exception as e:
        print(f"Error in register route: {e}")
        return f"<h1>Register</h1><p>Error loading template: {e}</p>"

@app.route('/user-dashboard')
def user_dashboard():
    if not session.get('user_id'):
        flash('Please log in to access your dashboard.', 'error')
        return redirect(url_for('login'))
    
    try:
        user = User.query.get(session['user_id'])
        recent_tenders = Tender.query.filter_by(status='Open').order_by(Tender.closing_date.asc()).limit(5).all()
        recent_news = NewsUpdate.query.order_by(NewsUpdate.date_posted.desc()).limit(3).all()
        
        return render_template('user_dashboard.html', user=user, recent_tenders=recent_tenders, recent_news=recent_news)
    except Exception as e:
        print(f"Error in user_dashboard route: {e}")
        return f"<h1>Dashboard</h1><p>Error loading template: {e}</p>"

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))

@app.route('/admin')
def admin_dashboard():
    if not session.get('is_admin'):
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('login'))
    
    try:
        total_tenders = Tender.query.count()
        total_messages = ContactMessage.query.count()
        unread_messages = ContactMessage.query.filter_by(is_read=False).count()
        total_users = User.query.count()
        total_news = NewsUpdate.query.count()
        current_time = datetime.now()
        
        return render_template('admin/dashboard.html', 
                             total_tenders=total_tenders,
                             total_messages=total_messages,
                             unread_messages=unread_messages,
                             total_users=total_users,
                             total_news=total_news,
                             current_time=current_time)
    except Exception as e:
        print(f"Error in admin_dashboard route: {e}")
        return f"<h1>Admin Dashboard</h1><p>Error loading template: {e}</p>"

# NEWS MANAGEMENT ROUTES
@app.route('/admin/news')
def admin_news():
    if not session.get('is_admin'):
        flash('Access denied.', 'error')
        return redirect(url_for('login'))
    
    try:
        news_updates = NewsUpdate.query.order_by(NewsUpdate.date_posted.desc()).all()
        
        # Calculate date statistics
        from datetime import datetime, timedelta
        
        now = datetime.utcnow()
        thirty_days_ago = now - timedelta(days=30)
        seven_days_ago = now - timedelta(days=7)
        
        # Count news from different time periods
        total_news = len(news_updates)
        news_this_month = len([n for n in news_updates if n.date_posted >= thirty_days_ago])
        news_this_week = len([n for n in news_updates if n.date_posted >= seven_days_ago])
        
        return render_template('admin/news.html', 
                             news_updates=news_updates,
                             total_news=total_news,
                             news_this_month=news_this_month,
                             news_this_week=news_this_week)
    except Exception as e:
        print(f"Error in admin_news route: {e}")
        return f"<h1>Admin News</h1><p>Error loading template: {e}</p>"

@app.route('/admin/news/add', methods=['GET', 'POST'])
def add_news():
    if not session.get('is_admin'):
        flash('Access denied.', 'error')
        return redirect(url_for('login'))
    
    form = NewsForm()
    if form.validate_on_submit():
        try:
            news = NewsUpdate(
                title=form.title.data,
                content=form.content.data,
                author=form.author.data
            )
            db.session.add(news)
            db.session.commit()
            flash('News update added successfully!', 'success')
            return redirect(url_for('admin_news'))
        except Exception as e:
            print(f"Error adding news: {e}")
            flash('Error adding news. Please try again.', 'error')
    
    return render_template('admin/add_news.html', form=form)

@app.route('/admin/news/edit/<int:news_id>', methods=['GET', 'POST'])
def edit_news(news_id):
    if not session.get('is_admin'):
        flash('Access denied.', 'error')
        return redirect(url_for('login'))
    
    news = NewsUpdate.query.get_or_404(news_id)
    form = NewsForm(obj=news)
    
    if form.validate_on_submit():
        try:
            news.title = form.title.data
            news.content = form.content.data
            news.author = form.author.data
            db.session.commit()
            flash('News update updated successfully!', 'success')
            return redirect(url_for('admin_news'))
        except Exception as e:
            print(f"Error updating news: {e}")
            flash('Error updating news. Please try again.', 'error')
    
    return render_template('admin/edit_news.html', form=form, news=news)

@app.route('/admin/news/delete/<int:news_id>', methods=['POST'])
def delete_news(news_id):
    if not session.get('is_admin'):
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    try:
        news = NewsUpdate.query.get_or_404(news_id)
        db.session.delete(news)
        db.session.commit()
        return jsonify({'success': True, 'message': 'News deleted successfully'})
    except Exception as e:
        print(f"Error deleting news: {e}")
        return jsonify({'success': False, 'message': 'Error deleting news'}), 500

# Add these routes to your app.py file

@app.route('/admin/users/<int:user_id>/make-admin', methods=['POST'])
def make_admin(user_id):
    if not session.get('is_admin'):
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    try:
        user = User.query.get_or_404(user_id)
        user.is_admin = True
        db.session.commit()
        return jsonify({'success': True, 'message': 'User promoted to admin successfully'})
    except Exception as e:
        print(f"Error making user admin: {e}")
        return jsonify({'success': False, 'message': 'Error promoting user'}), 500

@app.route('/admin/users/<int:user_id>/delete', methods=['DELETE'])
def delete_user(user_id):
    if not session.get('is_admin'):
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    try:
        user = User.query.get_or_404(user_id)
        
        # Don't allow deleting yourself
        if user.id == session.get('user_id'):
            return jsonify({'success': False, 'message': 'Cannot delete your own account'}), 400
        
        db.session.delete(user)
        db.session.commit()
        return jsonify({'success': True, 'message': 'User deleted successfully'})
    except Exception as e:
        print(f"Error deleting user: {e}")
        return jsonify({'success': False, 'message': 'Error deleting user'}), 500

@app.route('/admin/create-admin', methods=['GET', 'POST'])
def create_admin():
    """Route to create the first admin user"""
    # Check if any admin already exists
    existing_admin = User.query.filter_by(is_admin=True).first()
    if existing_admin:
        flash('An admin user already exists. Please login with existing credentials.', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Basic validation
        if not username or not email or not password:
            flash('All fields are required.', 'error')
            return render_template('create_admin.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
            return render_template('create_admin.html')
        
        # Check if username or email already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'error')
            return render_template('create_admin.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists.', 'error')
            return render_template('create_admin.html')
        
        try:
            # Create admin user
            admin_user = User(
                username=username,
                email=email,
                password_hash=generate_password_hash(password),
                is_admin=True
            )
            
            db.session.add(admin_user)
            db.session.commit()
            
            flash('Admin user created successfully! You can now login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            print(f"Error creating admin user: {e}")
            flash('Error creating admin user. Please try again.', 'error')
            return render_template('create_admin.html')
    
    return render_template('create_admin.html')

@app.route('/setup-admin')
def setup_admin():
    """Quick setup route - creates admin user if none exists"""
    try:
        # Check if any admin already exists
        existing_admin = User.query.filter_by(is_admin=True).first()
        if existing_admin:
            flash('Admin user already exists. Please login.', 'info')
            return redirect(url_for('login'))
        
        # Create default admin user
        admin_user = User(
            username='admin',
            email='admin@cciltd.in',
            password_hash=generate_password_hash('admin123'),
            is_admin=True
        )
        
        db.session.add(admin_user)
        db.session.commit()
        
        flash('Admin user created! Username: admin, Password: admin123', 'success')
        return redirect(url_for('login'))
    except Exception as e:
        print(f"Error setting up admin: {e}")
        flash('Error setting up admin user.', 'error')
        return redirect(url_for('index'))

@app.route('/admin/tenders')
def admin_tenders():
    if not session.get('is_admin'):
        flash('Access denied.', 'error')
        return redirect(url_for('login'))
    
    try:
        tenders = Tender.query.order_by(Tender.closing_date.desc()).all()
        return render_template('admin/tenders.html', tenders=tenders)
    except Exception as e:
        print(f"Error in admin_tenders route: {e}")
        return f"<h1>Admin Tenders</h1><p>Error loading template: {e}</p>"

@app.route('/admin/messages')
def admin_messages():
    if not session.get('is_admin'):
        flash('Access denied.', 'error')
        return redirect(url_for('login'))
    
    try:
        messages = ContactMessage.query.order_by(ContactMessage.date_sent.desc()).all()
        return render_template('admin/messages.html', messages=messages)
    except Exception as e:
        print(f"Error in admin_messages route: {e}")
        return f"<h1>Admin Messages</h1><p>Error loading template: {e}</p>"

@app.route('/admin/users')
def admin_users():
    if not session.get('is_admin'):
        flash('Access denied.', 'error')
        return redirect(url_for('login'))
    
    try:
        users = User.query.order_by(User.created_at.desc()).all()
        return render_template('admin/users.html', users=users)
    except Exception as e:
        print(f"Error in admin_users route: {e}")
        return f"<h1>Admin Users</h1><p>Error loading template: {e}</p>"

# API Routes
@app.route('/api/news')
def api_news():
    try:
        news = NewsUpdate.query.order_by(NewsUpdate.date_posted.desc()).limit(5).all()
        return jsonify([{
            'id': n.id,
            'title': n.title,
            'content': n.content[:200] + '...' if len(n.content) > 200 else n.content,
            'date_posted': n.date_posted.strftime('%Y-%m-%d'),
            'author': n.author
        } for n in news])
    except Exception as e:
        print(f"Error in api_news: {e}")
        return jsonify([])

@app.route('/api/tenders')
def api_tenders():
    try:
        tenders = Tender.query.filter_by(status='Open').order_by(Tender.closing_date.asc()).all()
        return jsonify([tender.to_dict() for tender in tenders])
    except Exception as e:
        print(f"Error in api_tenders: {e}")
        return jsonify([])

# Demo route for quick admin access
@app.route('/demo-admin')
def demo_admin():
    """Quick demo admin login - remove in production"""
    try:
        admin_user = User.query.filter_by(username='admin').first()
        if admin_user:
            session['user_id'] = admin_user.id
            session['username'] = admin_user.username
            session['is_admin'] = admin_user.is_admin
            flash('Demo admin login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Admin user not found. Please run the application to create sample data.', 'error')
            return redirect(url_for('login'))
    except Exception as e:
        print(f"Error in demo_admin: {e}")
        flash('Demo admin login failed.', 'error')
        return redirect(url_for('login'))

def create_sample_data():
    """Create sample data for demonstration"""
    try:
        # Create admin user
        admin = User(
            username='admin',
            email='admin@cciltd.in',
            password_hash=generate_password_hash('admin123'),
            is_admin=True
        )
        
        # Create a regular user for testing
        user = User(
            username='testuser',
            email='user@cciltd.in',
            password_hash=generate_password_hash('user123'),
            is_admin=False
        )
        
        # Sample news updates
        news1 = NewsUpdate(
            title='CCI Reports Strong Q4 Performance',
            content='Cement Corporation of India Limited has reported strong financial performance for Q4 2024, with increased production and improved operational efficiency across all plants.',
            author='CCI Communications'
        )
        
        news2 = NewsUpdate(
            title='New Sustainability Initiative Launched',
            content='CCI has launched a comprehensive sustainability initiative focusing on reducing carbon emissions and promoting green cement production technologies.',
            author='CCI Environmental Team'
        )
        
        # Sample plants
        plant1 = Plant(
            name='Rajban Plant',
            location='Rajban',
            state='Himachal Pradesh',
            capacity=6.75,
            established_year=1979,
            status='Operational'
        )
        
        plant2 = Plant(
            name='Tandur Plant',
            location='Tandur',
            state='Telangana',
            capacity=10.90,
            established_year=1980,
            status='Operational'
        )
        
        # Sample board members
        board1 = BoardMember(
            name='Smt. Sanjay Sinha',
            designation='CMD',
            qualification='B.Tech, MBA',
            experience='Over 25 years in cement industry'
        )
        
        # Sample tenders
        tender1 = Tender(
            title='Supply of Raw Materials for Cement Production',
            description='Tender for supply of limestone and other raw materials for cement production at Rajban Plant.',
            tender_no='CCI/2024/001',
            opening_date=datetime(2024, 8, 1),
            closing_date=datetime(2024, 8, 30),
            estimated_cost=5000000,
            location='Rajban, Himachal Pradesh'
        )
        
        tender2 = Tender(
            title='Electrical Equipment Maintenance Contract',
            description='Annual maintenance contract for electrical equipment at Tandur Plant including transformers, motors, and control panels.',
            tender_no='CCI/2024/002',
            opening_date=datetime(2024, 9, 1),
            closing_date=datetime(2024, 9, 25),
            estimated_cost=2500000,
            location='Tandur, Telangana'
        )
        
        db.session.add_all([admin, user, news1, news2, plant1, plant2, board1, tender1, tender2])
        db.session.commit()
        print("Sample data created successfully!")
        print("Admin credentials: username='admin', password='admin123'")
        print("User credentials: username='testuser', password='user123'")
        print("You can also visit /demo-admin for quick admin access")
    except Exception as e:
        print(f"Error creating sample data: {e}")
        db.session.rollback()

def init_db():
    """Initialize database and create sample data if needed"""
    try:
        db.create_all()
        
        # Check if admin user exists, if not create sample data
        admin_exists = User.query.filter_by(username='admin').first()
        if not admin_exists:
            create_sample_data()
    except Exception as e:
        print(f"Error initializing database: {e}")

if __name__ == '__main__':
    with app.app_context():
        init_db()
    
    app.run(debug=True, host='0.0.0.0', port=5000)