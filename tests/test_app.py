import pytest
from flask import url_for

from blog.app import app, posts


@pytest.fixture
def client():
    app.config['SERVER_NAME'] = 'localhost:5000'
    with app.app_context():
        with app.test_client() as client:
            yield client


def test_home_page(client):
    response = client.get(url_for('generic_renderer', page='home'))
    assert response.status_code == 200
    assert b'Welcome to Blog Maryoma' in response.data


def test_about_page(client):
    response = client.get(url_for('generic_renderer', page='about'))
    assert response.status_code == 200


def test_blog_page_no_posts(client):
    response = client.get(url_for('generic_renderer', page='blog'))
    assert response.status_code == 200
    assert (
        b'No blog posts yet' in response.data or b'Blog Posts' in response.data
    )


def test_get_new_post(client):
    response = client.get(url_for('new_post'))
    assert response.status_code == 200
    assert b'New Post' in response.data


def test_new_post_without_redirect(client):
    response = client.post(
        url_for('new_post'),
        data={'title': 'Test Title', 'content': 'Test Content'},
    )
    assert response.status_code == 302
    assert response.location.endswith('/blog')


def test_new_post(client):
    response = client.post(
        url_for('new_post'),
        data={'title': 'New Post', 'content': 'This is a new post'},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b'New Post' in response.data
    assert b'This is a new post' in response.data


def test_new_post_no_content(client):
    response = client.post(
        url_for('new_post'),
        data={'title': '', 'content': ''},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b'Untitled' in response.data
    assert b'Empty Post' in response.data


def test_blog_page_with_posts(client):
    posts.append({'title': 'Test Post', 'content': 'This is a test post'})
    response = client.get(url_for('generic_renderer', page='blog'))
    assert response.status_code == 200
    assert b'Test Post' in response.data
    assert b'This is a test post' in response.data


def test_non_existing_page(client):
    response = client.get('/non-existing-route')
    assert response.status_code == 404
