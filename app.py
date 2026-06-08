import sqlite3
import re
import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
# Secret key for secure admin sessions
app.secret_key = 'ecommdots_million_dollar_vault_key_2026' 
DB_FILE = 'ecommdots.db'

def get_db_connection():
    """Establishes a connection to your data layer."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def ensure_master_admin():
    """Silently generates your master credentials if they don't exist."""
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE username = 'admin'").fetchone()
    if not user:
        hashed_pw = generate_password_hash('EliteCMS2026!')
        conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('admin', hashed_pw))
        conn.commit()
    conn.close()

def generate_slug(title):
    """Converts a new blog title into a clean, SEO-optimized URL."""
    slug = title.lower().strip()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[\s_-]+', '-', slug)
    return slug

# ==========================================
# 1. PUBLIC SEO ROUTES (THE FRONTEND)
# ==========================================

# ==========================================
# MAIN AGENCY ROUTES
# ==========================================
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/testimonials')
def testimonials():
    return render_template('testimonials.html')

@app.route('/blog')
def blog_grid():
    """Initial load: Pulls articles and mathematically generates the Category Nav."""
    conn = get_db_connection()
    
    # 1. Fetch the first 10 articles
    articles = conn.execute('SELECT * FROM articles ORDER BY created_at DESC LIMIT 10 OFFSET 0').fetchall()
    total_articles = conn.execute('SELECT COUNT(*) FROM articles').fetchone()[0]
    
    # 2. Dynamically calculate exact counts for every category in your database
    cat_counts_raw = conn.execute('SELECT category, COUNT(*) as count FROM articles GROUP BY category').fetchall()
    # Convert to a dictionary so Jinja2 can easily loop through it
    cat_counts = {row['category']: row['count'] for row in cat_counts_raw}
    
    conn.close()
    
    return render_template('blog_grid.html', articles=articles, total_articles=total_articles, cat_counts=cat_counts)

@app.route('/api/load_more')
def load_more():
    """Asynchronous API that handles BOTH Pagination and Category Filtering."""
    offset = int(request.args.get('offset', 0))
    category = request.args.get('category', 'all')
    limit = 10
    
    conn = get_db_connection()
    
    if category == 'all':
        articles = conn.execute('SELECT * FROM articles ORDER BY created_at DESC LIMIT ? OFFSET ?', (limit, offset)).fetchall()
        total_in_cat = conn.execute('SELECT COUNT(*) FROM articles').fetchone()[0]
    else:
        # Securely filter by the exact category requested by the frontend
        articles = conn.execute('SELECT * FROM articles WHERE category = ? ORDER BY created_at DESC LIMIT ? OFFSET ?', (category, limit, offset)).fetchall()
        total_in_cat = conn.execute('SELECT COUNT(*) FROM articles WHERE category = ?', (category,)).fetchone()[0]
        
    conn.close()
    
    # We return the HTML fragment AND the new total so the JS knows when to hide the "Load More" button
    html_fragment = render_template('_blog_loop.html', articles=articles)
    
    # We package the response with custom headers so the frontend JS gets the metadata without breaking the HTML
    from flask import make_response
    response = make_response(html_fragment)
    response.headers['X-Total-Count'] = total_in_cat
    response.headers['X-Returned-Count'] = len(articles)
    return response
    
    # Render ONLY the fragment HTML, not the whole page
    return render_template('_blog_loop.html', articles=articles)
@app.route('/blog/<string:slug>')
def article_view(slug):
    """Generates a dedicated page for a single article based on its URL slug."""
    conn = get_db_connection()
    article = conn.execute('SELECT * FROM articles WHERE slug = ?', (slug,)).fetchone()
    conn.close()
    
    if article is None:
        return render_template('404_vault.html'), 404
        
    return render_template('article.html', article=article)

# ==========================================
# 2. THE SECURE COMMAND CENTER (ADMIN CMS)
# ==========================================

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    """High-contrast, secure login gateway."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Access Denied. Invalid credentials.')
            
    return '''
        <body style="background:#0a0a0a; color:#fff; font-family:sans-serif; display:flex; justify-content:center; align-items:center; height:100vh; margin:0;">
            <div style="background:#111; padding:40px; border-radius:8px; border:1px solid rgba(255,255,255,0.1); width:100%; max-width:350px; box-shadow:0 20px 40px rgba(0,0,0,0.5), 0 0 40px rgba(217,35,45,0.1);">
                <h2 style="margin-top:0; font-weight:800; letter-spacing:2px;">CMS <span style="color:#d9232d;">ECOMMDOTS</span></h2>
                <form method="post" style="display:flex; flex-direction:column; gap:15px;">
                    <input type="text" name="username" placeholder="Username" required style="background:#050505; border:1px solid #333; color:#fff; padding:12px; outline:none;">
                    <input type="password" name="password" placeholder="Password" required style="background:#050505; border:1px solid #333; color:#fff; padding:12px; outline:none;">
                    <button type="submit" style="background:#d9232d; color:#fff; border:none; padding:14px; font-weight:bold; letter-spacing:1px; cursor:pointer; margin-top:10px;">LOGIN</button>
                </form>
            </div>
        </body>
    '''

@app.route('/admin', methods=['GET', 'POST'])
def admin_dashboard():
    """The Command Center: View and Publish Articles."""
    if not session.get('logged_in'):
        return redirect(url_for('admin_login'))
        
    conn = get_db_connection()
    
    # If the user submits a new article via the dashboard
    if request.method == 'POST':
        title = request.form['title']
        category = request.form['category']
        subcategory = request.form['subcategory']
        read_time = request.form['read_time']
        excerpt = request.form['excerpt']
        content = request.form['content']
        author_name = request.form['author_name']
        author_image = request.form['author_image']
        thumbnail_url = request.form['thumbnail_url']
        
        # Checkboxes for layout modifiers
        is_wide = 1 if 'is_wide' in request.form else 0
        is_featured = 1 if 'is_featured' in request.form else 0
        
        slug = generate_slug(title)
        publish_date = datetime.datetime.now().strftime("%B %Y")
        
        try:
            conn.execute('''
                INSERT INTO articles (title, slug, category, subcategory, read_time, publish_date, excerpt, content, author_name, author_image, thumbnail_url, is_wide, is_featured)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (title, slug, category, subcategory, read_time, publish_date, excerpt, content, author_name, author_image, thumbnail_url, is_wide, is_featured))
            conn.commit()
            flash('Masterpiece successfully deployed to the live grid.')
        except sqlite3.IntegrityError:
            flash('Deploy Failed: An article with a similar title or slug already exists.')
            
    # Pull all active articles to display in the management table
    articles = conn.execute('SELECT id, title, category, publish_date, slug FROM articles ORDER BY created_at DESC').fetchall()
    conn.close()
    
    return render_template('admin.html', articles=articles)

@app.route('/admin/delete/<int:id>', methods=['POST'])
def delete_article(id):
    """Permanently purges an article from the database."""
    if not session.get('logged_in'):
        return redirect(url_for('admin_login'))
        
    conn = get_db_connection()
    conn.execute('DELETE FROM articles WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Digital asset permanently destroyed.')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/logout')
def logout():
    session.clear()
    return redirect(url_for('admin_login'))

# ==========================================
# CONTEXTUAL 404 ROUTING
# ==========================================
@app.errorhandler(404)
def page_not_found(e):
    # 1. If the invalid URL was inside the Intelligence Vault
    if request.path.startswith('/article/') or request.path.startswith('/blog'):
        return render_template('404_vault.html'), 404
        
    # 2. For all other invalid agency URLs (services, about, random typos)
    return render_template('404_agency.html'), 404

if __name__ == '__main__':
    ensure_master_admin()
    # Debug is strictly False for production
    app.run(debug=False)