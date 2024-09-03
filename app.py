from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a random secret key for production

# Initialize the SQLite database
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        if name:
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute('INSERT INTO items (name, description) VALUES (?, ?)', (name, description))
            conn.commit()
            conn.close()
            flash('Item added successfully!', 'success')
            return redirect(url_for('items'))
        else:
            flash('Please fill out the name field!', 'danger')
    return render_template('add_item.html')

@app.route('/items')
def items():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM items')
    items = c.fetchall()
    conn.close()
    return render_template('items.html', items=items)

@app.route('/edit_item/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM items WHERE id = ?', (item_id,))
    item = c.fetchone()
    conn.close()

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        if name:
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute('UPDATE items SET name = ?, description = ? WHERE id = ?', (name, description, item_id))
            conn.commit()
            conn.close()
            flash('Item updated successfully!', 'success')
            return redirect(url_for('items'))
        else:
            flash('Please fill out the name field!', 'danger')
    return render_template('edit_item.html', item=item)

@app.route('/delete_item/<int:item_id>')
def delete_item(item_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('DELETE FROM items WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()
    flash('Item deleted successfully!', 'success')
    return redirect(url_for('items'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
