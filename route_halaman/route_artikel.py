from flask import Blueprint, jsonify, render_template, request, redirect, url_for
import controller.controller_artikel as artikel_controller

artikel_bp = Blueprint('artikel_bp', __name__, template_folder='../templates')

# API
@artikel_bp.route('/artikel', methods=['GET'])
def get_articles():
    try:
        articles = artikel_controller.get_all_articles()
        return jsonify({
            "status": "success",
            "data": articles
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Web Admin
# @artikel_bp.route('/admin/artikel', methods=['GET'])
# def index():
#     articles = artikel_controller.get_all_articles()
#     return render_template('artikel/index.html', articles=articles)
@artikel_bp.route('/admin/artikel', methods=['GET'])
def index():
    page = int(request.args.get('page', 1))
    per_page = 10
    search_query = request.args.get('search', '')

    # Ambil semua artikel dengan filter search
    all_articles = artikel_controller.get_all_articles(search_query)

    # Hitung total dan slice data untuk halaman saat ini
    total = len(all_articles)
    start = (page - 1) * per_page
    end = start + per_page
    articles = all_articles[start:end]

    # Cek apakah ada next page
    has_next = end < total

    return render_template('artikel/index.html', articles=articles, page=page, has_next=has_next, search_query=search_query)

@artikel_bp.route('/admin/artikel/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        artikel_controller.create_article(
            request.form['title'],
            request.form['content'],
            request.files.get('image')
        )
        return redirect(url_for('artikel_bp.index'))
    return render_template('artikel/create.html')

@artikel_bp.route('/admin/artikel/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    article = artikel_controller.get_article_by_id(id)
    if request.method == 'POST':
        artikel_controller.update_article(
            id,
            request.form['title'],
            request.form['content'],
            request.files.get('image')
        )
        return redirect(url_for('artikel_bp.index'))
    return render_template('artikel/edit.html', article=article)

@artikel_bp.route('/admin/artikel/delete/<id>', methods=['GET'])
def delete(id):
    artikel_controller.delete_article(id)
    return redirect(url_for('artikel_bp.index'))

@artikel_bp.route('/artikel/<id>', methods=['GET'])
def get_article(id):
    try:
        article = artikel_controller.get_article_by_id(id)
        if not article:
            return jsonify({"status": "error", "message": "Article not found"}), 404
        return jsonify({"status": "success", "data": article}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
