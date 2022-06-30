import random
import string
from flask import Flask, session, render_template, url_for, request, redirect
from passlib.hash import pbkdf2_sha256

app = Flask(__name__)
alphanum=''.join(ch for ch in string.printable if ch.isalnum())
skey=''.join(random.choice(alphanum) for i in range(16))
app.secret_key = skey

def pass_from_text(p):
  return pbkdf2_sha256.encrypt(p, rounds=20000, salt_size=16)
def ver(p1,pw):
  return pbkdf2_sha256.verify(p1, pw)

def sessionCnt():
  try: 
   session['counter'] += 1
  except:
    session['counter'] = 1

ppw=pass_from_text("qazxsw21")
print ppw
@app.route('/')
def index():
    sessionCnt()
    return render_template('index.html')

@app.route('/form')
def form():
  sessionCnt()
  if request.args.get('username') and request.args.get('password'):
	   #check username and password with db...
  	if request.args.get('username')=="mail@gmail.com" and ver(request.args.get('password'),ppw):
  		session['name'] = "TestUser"
  		session['email'] = request.args.get('username')
  		session['passwd'] = request.args.get('password')
  		return redirect(url_for('index'))
  	else:
  		return render_template('form.html', session=session)	
  else:
	return render_template('form.html', session=session)

@app.route('/page1')
def page1():
  session['counter'] = session['counter'] + 1
  return render_template('page1.html')

@app.route('/page2')
def page2():
  session['counter'] = session['counter'] + 1
  return render_template('page2.html')

@app.route('/clear')
def clearsession():
    session.clear()
    return redirect(url_for('index'))



if __name__ == '__main__':
  app.run(debug=True)
