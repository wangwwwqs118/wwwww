import os
from flask import Flask, render_template, request, jsonify
from supabase import create_client, Client

app = Flask(__name__)

# 優先讀取 Render 環境變數；若沒有讀到，則使用引號內的備用值
SUPABASE_URL = os.environ.get("SUPABASE_URL") or "https://hkgvyjluqhnvwhjgjlza.supabase.co"
SUPABASE_KEY = os.environ.get("SUPABASE_KEY") or "sb_publishable_jTGKCg5Fd3rm1w9GYZ9USw_0N5EZNVe"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
def index():
    query = supabase.table('products').select('*')
    category = request.args.get('category')
    search = request.args.get('search')
    
    if category and category != 'all':
        query = query.eq('category', category)
    if search:
        query = query.ilike('name', f'%{search}%')
        
    response = query.order('id').execute()
    return render_template('index.html', products=response.data, current_cat=category or 'all')

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    response = supabase.table('products').select('*').eq('id', product_id).single().execute()
    return render_template('detail.html', product=response.data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)