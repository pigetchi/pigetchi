from flask import Flask, render_template_string, request, redirect, url_for
import random
from time import time

app = Flask(__name__)

# Начальные настройки
app.config['state'] = {
    'pressed_verify': False,
    'pressed_cost': False,
    'pressed_deposit': False,
    'show_error': False,
    'show_success': False,
    'random_cost': 0,
    'error_message': "",
    'success_message': "",
    'cat_state': 'idle'  # idle, checking, money, happy
}

@app.route('/')
def index():
    state = app.config['state']
    
    # HTML шаблон с CSS и JavaScript
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Pigetchi</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Comic+Neue:wght@700&display=swap');
            
            body {
                font-family: 'Comic Neue', cursive;
                text-align: center;
                margin: 0;
                padding: 20px;
                background-color: #FFF5E6;
                background-image: radial-gradient(#FFD700 10%, transparent 10%);
                background-size: 20px 20px;
            }
            
            .container {
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                background-color: white;
                border-radius: 20px;
                box-shadow: 0 10px 20px rgba(0,0,0,0.1);
                border: 3px solid #FFA500;
            }
            
            .header {
                font-size: 42px;
                margin-bottom: 20px;
                cursor: pointer;
                color: #FF6B6B;
                text-shadow: 3px 3px 0 #FFD700;
                transition: all 0.3s;
            }
            
            .header:hover {
                transform: scale(1.05);
                text-shadow: 5px 5px 0 #FFD700;
            }
            
            .cat-container {
                margin: 20px 0;
                height: 200px;
                position: relative;
            }
            
            .cat {
                width: 150px;
                height: 150px;
                margin: 0 auto;
                background-size: contain;
                background-repeat: no-repeat;
                background-position: center;
                transition: all 0.5s;
                position: relative;
            }
            
            .cat-idle {
                background-image: url('https://i.imgur.com/RQ8Z0Qp.png');
                animation: bounce 2s infinite;
            }
            
            .cat-checking {
                background-image: url('https://i.imgur.com/JQ6pLlD.png');
                animation: shake 0.5s infinite;
            }
            
            .cat-money {
                background-image: url('https://i.imgur.com/4Q2Zfzq.png');
                animation: float 3s infinite;
            }
            
            .cat-happy {
                background-image: url('https://i.imgur.com/9pZzKjU.png');
                animation: dance 1s infinite;
            }
            
            .button-container {
                display: flex;
                justify-content: center;
                gap: 15px;
                margin-bottom: 20px;
                flex-wrap: wrap;
            }
            
            .button {
                padding: 12px 25px;
                font-size: 18px;
                border: none;
                border-radius: 50px;
                cursor: pointer;
                transition: all 0.3s;
                font-weight: bold;
                box-shadow: 0 5px 0 rgba(0,0,0,0.2);
                position: relative;
                overflow: hidden;
            }
            
            .button:active {
                transform: translateY(5px);
                box-shadow: none;
            }
            
            .button:hover {
                filter: brightness(1.1);
            }
            
            .button::after {
                content: '';
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: rgba(255,255,255,0.1);
                transform: rotate(45deg);
                transition: all 0.5s;
            }
            
            .button:hover::after {
                left: 100%;
            }
            
            #verify {
                background: linear-gradient(135deg, #4CAF50, #8BC34A);
                color: white;
                text-shadow: 1px 1px 1px rgba(0,0,0,0.3);
            }
            
            #cost {
                background: linear-gradient(135deg, #2196F3, #03A9F4);
                color: white;
                text-shadow: 1px 1px 1px rgba(0,0,0,0.3);
            }
            
            #deposit {
                background: linear-gradient(135deg, #FF9800, #FFC107);
                color: white;
                text-shadow: 1px 1px 1px rgba(0,0,0,0.3);
            }
            
            .display-area {
                margin-top: 20px;
                min-height: 60px;
                position: relative;
            }
            
            .message {
                padding: 10px 20px;
                border-radius: 50px;
                font-size: 18px;
                margin: 10px auto;
                max-width: 80%;
                box-shadow: 0 3px 10px rgba(0,0,0,0.1);
            }
            
            .error {
                background: #FFEBEE;
                color: #F44336;
                border: 2px solid #F44336;
                animation: shake 0.5s;
            }
            
            .success {
                background: #E8F5E9;
                color: #4CAF50;
                border: 2px solid #4CAF50;
                animation: pop 0.5s;
            }
            
            .cost-display {
                font-size: 28px;
                font-weight: bold;
                color: #FF9800;
                text-shadow: 2px 2px 0 #FFF9C4;
                animation: pulse 1s infinite alternate;
            }
            
            @keyframes bounce {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-20px); }
            }
            
            @keyframes shake {
                0%, 100% { transform: translateX(0); }
                25% { transform: translateX(-5px); }
                75% { transform: translateX(5px); }
            }
            
            @keyframes float {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-15px); }
            }
            
            @keyframes dance {
                0%, 100% { transform: rotate(0); }
                25% { transform: rotate(5deg); }
                75% { transform: rotate(-5deg); }
            }
            
            @keyframes pulse {
                from { transform: scale(1); }
                to { transform: scale(1.1); }
            }
            
            @keyframes pop {
                0% { transform: scale(0.5); opacity: 0; }
                80% { transform: scale(1.1); }
                100% { transform: scale(1); opacity: 1; }
            }
            
            .confetti {
                position: absolute;
                width: 10px;
                height: 10px;
                background-color: #f00;
                opacity: 0;
            }
        </style>
        <script>
            function reloadPage() {
                window.location.href = '/reload';
            }
            
            function createConfetti() {
                const colors = ['#FF5252', '#FFD740', '#64FFDA', '#448AFF', '#B388FF'];
                const container = document.querySelector('.display-area');
                
                for (let i = 0; i < 50; i++) {
                    const confetti = document.createElement('div');
                    confetti.className = 'confetti';
                    confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
                    confetti.style.left = Math.random() * 100 + '%';
                    confetti.style.top = -10 + 'px';
                    confetti.style.opacity = 1;
                    confetti.style.transform = 'rotate(' + Math.random() * 360 + 'deg)';
                    
                    const animation = confetti.animate([
                        { top: '-10px', opacity: 1, transform: 'rotate(0deg)' },
                        { top: '100%', opacity: 0, transform: 'rotate(' + (Math.random() * 360) + 'deg)' }
                    ], {
                        duration: 1000 + Math.random() * 2000,
                        easing: 'cubic-bezier(0.1, 0.8, 0.3, 1)'
                    });
                    
                    container.appendChild(confetti);
                    animation.onfinish = () => confetti.remove();
                }
            }
            
            {% if state['show_success'] %}
                window.onload = function() {
                    createConfetti();
                };
            {% endif %}
        </script>
    </head>
    <body>
        <div class="container">
            <div class="header" onclick="reloadPage()">pigetchi</div>
            
            <div class="cat-container">
                <div class="cat 
                    {% if state['cat_state'] == 'checking' %}cat-checking
                    {% elif state['cat_state'] == 'money' %}cat-money
                    {% elif state['cat_state'] == 'happy' %}cat-happy
                    {% else %}cat-idle{% endif %}">
                </div>
            </div>
            
            <div class="button-container">
                <button id="verify" class="button" onclick="window.location.href='/verify'">Праверить</button>
                <button id="cost" class="button" onclick="window.location.href='/cost'">Стоимость</button>
                <button id="deposit" class="button" onclick="window.location.href='/deposit'">Задепать</button>
            </div>
            
            <div class="display-area">
                {% if state['show_error'] %}
                    <div class="message error">{{ state['error_message'] }}</div>
                {% endif %}
                
                {% if state['pressed_cost'] and state['pressed_verify'] %}
                    <div class="cost-display">{{ state['random_cost'] }}$</div>
                {% endif %}
                
                {% if state['show_success'] %}
                    <div class="message success">{{ state['success_message'] }}</div>
                {% endif %}
            </div>
        </div>
    </body>
    </html>
    """
    
    return render_template_string(html, state=state)

@app.route('/verify')
def verify():
    state = app.config['state']
    state['pressed_verify'] = True
    state['show_error'] = False
    state['error_message'] = ""
    state['cat_state'] = 'checking'
    return redirect(url_for('index'))

@app.route('/cost')
def cost():
    state = app.config['state']
    state['pressed_cost'] = True
    state['random_cost'] = random.randint(1, 100)
    
    if not state['pressed_verify']:
        state['show_error'] = True
        state['error_message'] = "Сначала проверьте!"
        state['show_success'] = False
        state['cat_state'] = 'idle'
    else:
        state['cat_state'] = 'money'
    
    return redirect(url_for('index'))

@app.route('/deposit')
def deposit():
    state = app.config['state']
    
    if state['pressed_verify'] and state['pressed_cost']:
        state['show_success'] = True
        state['success_message'] = "Успешно! 🎉"
        state['pressed_deposit'] = True
        state['show_error'] = False
        state['cat_state'] = 'happy'
    else:
        state['show_error'] = True
        state['error_message'] = "Сначала проверьте и укажите стоимость!"
        state['cat_state'] = 'idle'
    
    return redirect(url_for('index'))

@app.route('/reload')
def reload():
    # Сброс всех состояний
    app.config['state'] = {
        'pressed_verify': False,
        'pressed_cost': False,
        'pressed_deposit': False,
        'show_error': False,
        'show_success': False,
        'random_cost': 0,
        'error_message': "",
        'success_message': "",
        'cat_state': 'idle'
    }
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)