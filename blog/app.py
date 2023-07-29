from typing import Any, Dict, List

from flask import Flask, abort, redirect, render_template, request, url_for
from jinja2.exceptions import TemplateNotFound

app: Flask = Flask(__name__, template_folder='templates')

posts: List[Dict[str, str]] = []


@app.route('/')
@app.route('/<page>')
def generic_renderer(page: str = 'home') -> Any:
    try:
        return render_template(f'{page}.html', posts=posts)
    except TemplateNotFound:
        abort(404)


@app.route('/new-post', methods=['GET', 'POST'])
def new_post() -> Any:
    if request.method == 'POST':
        posts.append(
            {
                'title': request.form.get('title').strip() or 'Untitled',
                'content': request.form.get('content').strip() or 'Empty Post',
            }
        )
        return redirect(url_for('generic_renderer', page='blog'))
    return render_template('new_post.html')
