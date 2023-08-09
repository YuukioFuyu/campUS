from flask import Flask, render_template, request, redirect, url_for, session, flash, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
from cryptography.fernet import Fernet
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Database PostgreSQL
# 'postgresql://[DATABASE USER]:[PASSWORD]@[IP SERVER]/[DATABASE NAME]'
# Contoh:
# 'postgresql://postgres:Hw020&g@VzKz@127.0.0.1/messages'
#
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Hw020&g@VzKz@127.0.0.1/messages'
app.config['SESSION_COOKIE_SECURE'] = True
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Custom your own Secret Key for Encryption
app.secret_key = 'acuMalakaNguhahHaha'

# Generate Fernet key
fernet_key = Fernet.generate_key()
cipher_suite = Fernet(fernet_key)

# Class Section Pesan
class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    pengirim = db.Column(db.String(100), nullable=False)
    penerima = db.Column(db.String(100), nullable=False)
    encrypted_pesan = db.Column(db.LargeBinary, nullable=False)
    replies = db.relationship('Reply', backref='message', lazy=True)

    @property
    def pesan(self):
        decrypted_pesan = cipher_suite.decrypt(self.encrypted_pesan)
        return decrypted_pesan.decode()

    @pesan.setter
    def pesan(self, value):
        encrypted_pesan = cipher_suite.encrypt(value.encode())
        self.encrypted_pesan = encrypted_pesan

class Reply(db.Model):
    __tablename__ = 'replies'
    id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(db.Integer, db.ForeignKey('messages.id'), nullable=False)
    pengirim = db.Column(db.String(100), nullable=False)
    encrypted_pesan = db.Column(db.LargeBinary, nullable=False)

    @property
    def pesan(self):
        decrypted_pesan = cipher_suite.decrypt(self.encrypted_pesan)
        return decrypted_pesan.decode()

    @pesan.setter
    def pesan(self, value):
        encrypted_pesan = cipher_suite.encrypt(value.encode())
        self.encrypted_pesan = encrypted_pesan

# Class Section User
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    nama = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Route Section
@app.route('/')
@login_required
def index():
    username = session.get('username')
    if current_user.role == 'admin':
        messages = Message.query.all()
        return render_template('admin.html', messages=messages, username=username)
    else:
        messages = Message.query.filter(Message.username == username).all()
        return render_template('index.html', messages=messages, username=username)


# Menu Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        nama = request.form['nama']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        role = 'mahasiswa'

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username sudah digunakan. Silakan pilih username lain.', 'error')
            return redirect(url_for('register'))

        if password != confirm_password:
            flash('Konfirmasi password tidak sesuai.', 'error')
            return redirect(url_for('register'))

        _hashed_password = generate_password_hash(password)
        user = User(username=username, nama=nama, password=_hashed_password, role=role)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('register.html')


# Menu LogIn
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            session['username'] = user.username
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'error')
    return render_template('login.html')


# Menu LogOut
@app.route('/logout')
@login_required
def logout():
    logout_user()
    del session['username']
    return redirect(url_for('index'))


# Dashboard Profile
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    username = session.get('username')
    user = User.query.filter_by(username=username).first()

    if user is None:
        flash('Pengguna tidak ditemukan.', 'error')
        return redirect(url_for('index'))
    if request.method == 'POST':
        username_baru = request.form['username_baru']
        nama_baru = request.form['nama_baru']
        password_baru = request.form['password_baru']
        confirm_password = request.form['confirm_password']
        #role_baru = request.form['role_baru']
        # Perbarui username jika berbeda
        if username_baru and username_baru != username:
            existing_user = User.query.filter_by(username=username_baru).first()
            if existing_user:
                flash('Username sudah digunakan. Silakan pilih username lain.', 'error')
                return redirect(url_for('profile'))
            user.username = username_baru
        # Perbarui nama
        if nama_baru:
            user.nama = nama_baru
        # Perbarui password
        if password_baru:
            user.password = generate_password_hash(password_baru)
        # Konfirmasi password
        if password_baru != confirm_password:
            flash('Konfirmasi password tidak sesuai.', 'error')
            return redirect(url_for('profile'))
        # Perbarui role
        #if role_baru:
        #    user.role = role_baru
        db.session.commit()
        flash('Profil berhasil diperbarui.', 'success')
        return redirect(url_for('profile'))
    return render_template('profile.html', user=user)


# Dashboard Admin
@app.route('/admin')
@login_required
def admin():
    if current_user.role != 'admin':
        flash('Anda tidak memiliki akses sebagai Admin.', 'error')
        return redirect(url_for('index'))
    messages = Message.query.all()
    return render_template('admin.html', messages=messages)


# Tampilkan Semua User
@app.route('/users')
@login_required
def users():
    if current_user.role != 'admin':
        flash('Anda tidak memiliki akses sebagai Admin.', 'error')
        return redirect(url_for('index'))
    users = User.query.all()
    return render_template('users.html', users=users)


# Edit User
@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if current_user.role != 'admin':
        flash('Anda tidak memiliki akses sebagai Admin.', 'error')
        return redirect(url_for('index'))

    user = User.query.get(user_id)
    if user is None:
        flash('Pengguna tidak ditemukan.', 'error')
        return redirect(url_for('admin'))

    if request.method == 'POST':
        username_baru = request.form.get('username')
        nama_baru = request.form.get('nama')
        password_baru = request.form.get('password')
        confirm_password = request.form['confirm_password']
        role_baru = request.form.get('role')

        if username_baru and username_baru != user.username:
            existing_user = User.query.filter_by(username=username_baru).first()
            if existing_user:
                flash('Username sudah digunakan. Silakan pilih username lain.', 'error')
                return redirect(url_for('edit_user', user_id=user.id))
            user.username = username_baru

        if nama_baru:
            user.nama = nama_baru

        if password_baru:
            user.password = generate_password_hash(password_baru)

        if password_baru != confirm_password:
            flash('Konfirmasi password tidak sesuai.', 'error')
            return redirect(url_for('edit_user', user_id=user.id))

        if role_baru:
            user.role = role_baru

        db.session.commit()
        flash('Data pengguna berhasil diperbarui.', 'success')
        return redirect(url_for('index'))

    return render_template('edit_user.html', user=user)


# Hapus User
@app.route('/delete_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def delete_user(user_id):
    if current_user.role != 'admin':
        flash('Anda tidak memiliki akses sebagai Admin.', 'error')
        return redirect(url_for('index'))

    user = User.query.get(user_id)
    if not user:
        flash('Pengguna tidak ditemukan.', 'error')
        return redirect(url_for('users'))

    if request.method == 'POST':
        db.session.delete(user)
        db.session.commit()
        flash('Pengguna berhasil dihapus.', 'success')
        return redirect(url_for('users'))

    return render_template('users.html', user=user)


# Buat Pesan
@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    username = session.get('username')
    if request.method == 'POST':
        username = username
        pengirim = request.form['pengirim']
        penerima = request.form['penerima']
        pesan = request.form['pesan']
        message = Message(username=username, pengirim=pengirim, penerima=penerima, pesan=pesan)
        db.session.add(message)
        db.session.commit()
        return redirect(url_for('index'))
    # Ambil data pengguna dengan peran "admin" dari tabel "users"
    users = User.query.filter_by(role='admin').all()
    return render_template('create.html', username=username, users=users)


# Balas Pesan
@app.route('/reply/<int:id>', methods=['GET', 'POST'])
def reply(id):
    if current_user.role != 'admin':
        flash('Anda tidak memiliki akses sebagai Admin.', 'error')
        return redirect(url_for('index'))
    message = Message.query.get(id)
    if request.method == 'POST':
        pengirim = request.form['pengirim']
        pesan = request.form['pesan']
        reply = Reply(message_id=message.id, pengirim=pengirim, pesan=pesan)
        db.session.add(reply)
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('reply.html', message=message)


# Edit Balas Pesan
@app.route('/edit_reply/<int:id>', methods=['GET', 'POST'])
def edit_reply(id):
    if current_user.role != 'admin':
        flash('Anda tidak memiliki akses sebagai Admin.', 'error')
        return redirect(url_for('index'))
    reply = Reply.query.get(id)
    if not reply:
        return redirect(url_for('admin'))  # Redirect jika reply tidak ditemukan

    message = reply.message
    if not message:
        return redirect(url_for('admin'))  # Redirect jika message tidak ditemukan

    if request.method == 'POST':
        new_pesan = request.form['pesan']
        reply.pesan = new_pesan
        db.session.commit()
        return redirect(url_for('admin'))

    return render_template('edit_reply.html', message=message, reply=reply)


# Edit Pesan
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    message = Message.query.get(id)
    if not message:
        return redirect(url_for('index'))  # Redirect jika pesan tidak ditemukan

    # Cek apakah pengguna yang sedang login adalah pengirim pesan
    if current_user.username != message.username:
        flash('Anda tidak memiliki akses untuk mengedit pesan ini.', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        message.pengirim = request.form['pengirim']
        message.penerima = request.form['penerima']
        message.pesan = request.form['pesan']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', message=message)


# Delete Pesan
@app.route('/delete/<int:id>')
def delete(id):
    message = Message.query.get(id)
    if not message:
        return redirect(url_for('index'))  # Redirect jika pesan tidak ditemukan

    # Cek apakah pengguna yang sedang login adalah pengirim pesan atau admin
    if current_user.role != 'admin' and current_user.username != message.username:
        flash('Anda tidak memiliki akses untuk menghapus pesan ini.', 'error')
        return redirect(url_for('index'))

    if message:
        # Hapus entitas replies yang terkait dengan pesan
        for reply in message.replies:
            db.session.delete(reply)
        db.session.delete(message)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
