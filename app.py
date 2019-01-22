from flask import Flask, request, render_template, redirect, flash, jsonify, url_for
import sqlite3
import random

app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = 'my-secret-key'
app.config['SESSION_TYPE'] = 'filesystem'

conn = sqlite3.connect('collection.db')

cursor = conn.execute('SELECT * FROM words')

words = {}

for c in cursor:
    words[c[1]] = (c[2], c[3])

conn.close()

orig_len = len(words)

@app.route('/', methods=['GET', 'POST'])
def index():

    if "practice" in request.form:
        if(len(words) == 0):
            flash("All words practiced!")
            return render_template('index.html')

        return redirect(url_for('practice'))

    if "add" in request.form:
        return redirect(url_for('add'))

    if "populate" in request.form:
        conn = sqlite3.connect('collection.db')

        cursor = conn.execute('SELECT * FROM words')

        for c in cursor:
            words[c[1]] = (c[2], c[3])

        conn.close()

        flash("Repopulated, go back to practice!")

    return render_template('index.html')

@app.route('/practice', methods=['GET', 'POST'])
def practice():

    if request.method == "POST":

        choice = request.form['choice']
        word = request.form['word']

        if choice == "1":
            return jsonify({"meaning": words[word][0], "mnemonic": words[word][1]})

        elif choice == "2":
            del words[word]

            if(len(words) == 0):
                return jsonify({'word': "-1"})

            else:
                word = random.choice(list(words.keys()))
                done = str(orig_len - len(words)) + "/" + str(orig_len)
                return jsonify({'word': word, 'done': done})

        elif choice == "3":
            words_new = {key:value for key, value in words.items() if key != word}
            word = random.choice(list(words_new.keys()))
            done = str(orig_len - len(words)) + "/" + str(orig_len)
            return jsonify({'word': word, 'done': done})

    word = random.choice(list(words.keys()))
    done = str(orig_len - len(words)) + "/" + str(orig_len)

    return render_template('practice.html', word=word, done=done)

@app.route('/add', methods=['GET', 'POST'])
def add():

    if "addWord" in request.form:
        word = request.form['word']
        meaning = request.form['meaning']
        mnemonic = request.form['mnemonic']

        if(len(word) == 0 or len(meaning) == 0 or len(mnemonic) == 0):
            flash("Complete the form!")
            return render_template('add.html')

        conn = sqlite3.connect('collection.db')

        conn.execute('INSERT INTO words(word, meaning, mnemonic) VALUES(?, ?, ?)', (word, meaning, mnemonic))

        conn.commit()

        conn.close()

        flash("Word put into db successfully!")

    return render_template('add.html')
