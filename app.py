# ======================================================
# first version that worked"""
# try creating tha path to your download  folder

from flask import Flask, render_template, request, send_file
from docx import Document
import random

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', number_of_questions=5)  # Change 5 to whatever default value you want


@app.route('/generate', methods=['POST'])
def generate():
    number_of_questions = int(request.form['number_of_questions'])

    questions = []
    options = {}

    for i in range(1, number_of_questions + 1):
        question = request.form[f'question_{i}'].capitalize()
        questions.append(question)

        options_for_question = {}
        for label in ['a', 'b', 'c', 'd']:
            option = request.form[f'option_{i}_{label}'].capitalize()
            options_for_question[label] = option

        options[question] = options_for_question

    versions = []
    for _ in range(4):  # Generate two versions
        shuffled_questions, shuffled_options = shuffle_questions(questions.copy(), options.copy())
        versions.append((shuffled_questions, shuffled_options))

    documents = []
    for i, (questions, options) in enumerate(versions, start=1):
        doc = Document()
        for j, question in enumerate(questions, start=1):
            doc.add_paragraph(f"{j}. {question}")
            labels = ['a.', 'b.', 'c.', 'd.']
            for k, key in enumerate(options[question]):
                doc.add_paragraph(f"   {labels[k]} {options[question][key]}")
            doc.add_paragraph()
        file_name = f'TYPE {i}.docx'
        # file_path = r'C:Users/user/Download/'
        
        doc.save(file_name)
        # doc.save(file_path + file_name)
        documents.append(file_name)

    return render_template('download.html', documents=documents)

def shuffle_questions(questions, options):
    random.shuffle(questions)
    for question in questions:
        shuffled_options = options[question]
        shuffled_keys = list(shuffled_options.keys())
        random.shuffle(shuffled_keys)
        options[question] = {key: shuffled_options[key] for key in shuffled_keys}
    return questions, options

if __name__ == "__main__":
    app.run(debug=True)