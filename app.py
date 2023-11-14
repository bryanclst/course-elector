from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

#structures to hold posts and comments
class_list = [
    {"code": "ITCS 3155"},
    {"code": "JAPN 3202"}
]
posts = []
comments = {}

@app.get('/view_forum_posts')
def view_forum_posts():
    return render_template('view_forum_posts.html', posts=posts, forum_active = True)

@app.route('/create_forum_post', methods=['GET', 'POST'])
def create_forum_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        selected_code = request.form['code']
        posts.append({'title': title, 'content': content, 'code': selected_code})
        return redirect(url_for('view_forum_posts'))
    return render_template('create_forum_post.html', class_list=class_list, forum_active = True)


@app.route('/view_single_forum_post/<int:post_id>', methods=['GET', 'POST'])
def view_single_forum_post(post_id):
    if request.method == 'POST':
        comment = request.form['comment']
        if post_id not in comments:
            comments[post_id] = []
        comments[post_id].append(comment)
    post_data = posts[post_id] if post_id < len(posts) else None
    return render_template('view_single_forum_post.html', post=post_data, comments=comments.get(post_id, []), post_id=post_id, forum_active = True)



@app.route('/delete_post/<int:post_id>')
def delete_post(post_id):
    if post_id < len(posts):
        del posts[post_id]
    return redirect(url_for('view_forum_posts'), forum_active = True)

@app.route('/delete_comment/<int:post_id>/<int:comment_id>', methods=['POST'])
def delete_comment(post_id, comment_id):
    if post_id in comments and comment_id < len(comments[post_id]):
        del comments[post_id][comment_id]
    return redirect(url_for('view_single_forum_post', post_id=post_id), forum_active = True)

@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_forum_post(post_id):
    if request.method == 'POST':
        new_title = request.form['title']
        new_content = request.form['content']
        if post_id < len(posts):
            posts[post_id]['title'] = new_title
            posts[post_id]['content'] = new_content
            return redirect(url_for('view_single_forum_post', post_id=post_id))
    post_data = posts[post_id] if post_id < len(posts) else None
    return render_template('edit_forum_post.html', post=post_data, post_id=post_id, forum_active = True)

@app.route('/edit_comment/<int:post_id>/<int:comment_id>', methods=['GET', 'POST'])
def edit_forum_comment(post_id, comment_id):
    if request.method == 'POST':
        new_comment = request.form['comment']
        if post_id in comments and comment_id < len(comments[post_id]):
            comments[post_id][comment_id] = new_comment
            return redirect(url_for('view_single_forum_post', post_id=post_id))
    post_data = posts[post_id] if post_id < len(posts) else None
    return render_template('edit_forum_comment.html', comment=comments[post_id][comment_id], post=post_data, post_id=post_id, comment_id=comment_id, forum_active = True)

