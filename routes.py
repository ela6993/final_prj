from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from flask_socketio import SocketIO, emit, join_room, leave_room

from models import User
from models import Message

def register_routes(app, bcrypt, db, socketio):

    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/signup', methods = ['POST', 'GET'])
    def signup():
        if request.method == 'GET':
            return render_template('signup.html')
        elif request.method == 'POST':
            username = request.form.get('username')
            name = request.form.get('name')
            password = request.form.get('password')

            hashed_password = bcrypt.generate_password_hash(password)

            user = User(username = username, name = name, password = hashed_password)

            db.session.add(user)
            db.session.commit()

            return render_template('signup.html')
        
    @app.route('/login', methods = ['GET', 'POST'])
    def login():
        if request.method == 'GET':
            return render_template('login.html')
        elif request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            user = User.query.filter(User.username == username).first()

            if user and bcrypt.check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('userpage'))
            else:
                return redirect('index.html')
            
    @app.route('/userpage', methods = ['GET'])
    def userpage():
        if request.method == "GET":
            return render_template('userpage.html')
            
    @app.route('/logout')
    def logout():
        logout_user()
        return render_template('index.html')
    
    @app.route('/others')
    @login_required
    def others():
        users = User.query.filter(User.user_id != current_user.user_id).all()
        return render_template('users.html', users = users)
    
    @app.route('/user/<id>')
    def user(id):
        user = User.query.filter(User.user_id == id).first()
        room_id = f'{min(int(id), int(current_user.user_id))}_{max(int(id), int(current_user.user_id))}'

        return render_template('user.html', user = user, room_id = room_id)
    
    @app.route('/chat/<user>/<id>')
    def chat(id, user):
        username = user

        return render_template('chat.html', user = username, id = id)
    
    @socketio.on('join')
    def on_join(data):
        chat_id = data['chat_id']
        join_room(chat_id)

        history_messages = Message.query.filter(Message.chat_id == chat_id).order_by(Message.message_id).all()

        for i in history_messages:
            socketio.emit('message', {'username': i.username, 'msg': i.message_content}, to = request.sid)
  
    @socketio.on('send_message')
    def handle_message(data):
        username = data['username']
        chatid = data['chatid']
        message = data['message']

        sent_message = Message(message_content = message, chat_id = chatid, username = username)

        db.session.add(sent_message)
        db.session.commit()

        socketio.emit('message', {'username': username, 'msg': message}, to = chatid)        