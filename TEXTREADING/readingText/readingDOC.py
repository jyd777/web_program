from flask import Flask, jsonify
from docx import Document

app = Flask(__name__)

def read_docx(file_path):
    document = Document(file_path)
    content = {
        "paragraphs": [],
        "phrases": [],
        "images": []
    }
    
    temp_phrase = {}
    
    for para in document.paragraphs:
        text = para.text
        if text.startswith("Phrase:"):
            if temp_phrase:
                content["phrases"].append(temp_phrase)
            temp_phrase = {"phrase": text[len("Phrase: "):]}
        elif text.startswith("Explanation:"):
            temp_phrase["explanation"] = text[len("Explanation: "):]
        elif text.startswith("Example:"):
            temp_phrase["example_en"] = text[len("Example: "):]
        elif text.startswith("示例:"):
            temp_phrase["example_cn"] = text[len("示例: "):]
        else:
            content["paragraphs"].append(text)
    
    if temp_phrase:
        content["phrases"].append(temp_phrase)

    for rel in document.part.rels:
        if "image" in document.part.rels[rel].target_ref:
            content["images"].append(document.part.rels[rel].target_ref)
    
    return content

@app.route('/api/article', methods=['GET'])
def get_article():
    data = read_docx('F:/vscode_files/web技术/githubwork/web_program/TEXTREADING/readingText/article.docx')
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
