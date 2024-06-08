from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)

file_path = 'gerenciamento_loja.xlsx'
data = pd.read_excel(file_path)

@app.route('/')
def index():
    return render_template('templates\index.html', data=data.to_dict(orient='records'))

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        new_data = {
            'Nome': request.form['nome'],
            'Produto': request.form['produto'],
            'Quantidade': request.form['quantidade'],
            'Preço': request.form['preco']
        }
        global data
        data = data.append(new_data, ignore_index=True)
        data.to_excel(file_path, index=False)
        return redirect(url_for('templates\index.html'))
    return render_template('templates\add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'POST':
        data.at[id, 'Nome'] = request.form['nome']
        data.at[id, 'Produto'] = request.form['produto']
        data.at[id, 'Quantidade'] = request.form['quantidade']
        data.at[id, 'Preço'] = request.form['preco']
        data.to_excel(file_path, index=False)
        return redirect(url_for('templates\index.html'))
    row = data.loc[id]
    return render_template('templates\edit.html', row=row, id=id)

if __name__ == '__main__':
    app.run(debug=True)
