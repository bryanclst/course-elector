def test_layout(test_client):
    response = test_client.get('/')
    data = response.data.decode()
    
    # elements from _layout.html
    assert '<nav class="sticky-top navbar navbar-expand-lg bg-success" data-bs-theme="dark">' in data
    assert '<footer class="fixed-bottom py-1 bg-success">' in data
    
    # blocks should be properly filled in
    assert '<title>{% block title %}{% endblock %}</title>' not in data
    assert '{% block styles %}{% endblock %}' not in data
    
    
    
    # same tests for a few other pages
    
    response = test_client.get('/submit_rating')
    data = response.data.decode()
    
    # elements from _layout.html
    assert '<nav class="sticky-top navbar navbar-expand-lg bg-success" data-bs-theme="dark">' in data
    assert '<footer class="fixed-bottom py-1 bg-success">' in data
    
    # blocks should be properly filled in
    assert '<title>{% block title %}{% endblock %}</title>' not in data
    assert '{% block styles %}{% endblock %}' not in data
    
    
    
    response = test_client.get('/search')
    data = response.data.decode()
    
    # elements from _layout.html
    assert '<nav class="sticky-top navbar navbar-expand-lg bg-success" data-bs-theme="dark">' in data
    assert '<footer class="fixed-bottom py-1 bg-success">' in data
    
    # blocks should be properly filled in
    assert '<title>{% block title %}{% endblock %}</title>' not in data
    assert '{% block styles %}{% endblock %}' not in data
    
    
    
    response = test_client.get('/view_forum_posts')
    data = response.data.decode()
    
    # elements from _layout.html
    assert '<nav class="sticky-top navbar navbar-expand-lg bg-success" data-bs-theme="dark">' in data
    assert '<footer class="fixed-bottom py-1 bg-success">' in data
    
    # blocks should be properly filled in
    assert '<title>{% block title %}{% endblock %}</title>' not in data
    assert '{% block styles %}{% endblock %}' not in data
    
    
    
    response = test_client.get('/about')
    data = response.data.decode()
    
    # elements from _layout.html
    assert '<nav class="sticky-top navbar navbar-expand-lg bg-success" data-bs-theme="dark">' in data
    assert '<footer class="fixed-bottom py-1 bg-success">' in data
    
    # blocks should be properly filled in
    assert '<title>{% block title %}{% endblock %}</title>' not in data
    assert '{% block styles %}{% endblock %}' not in data