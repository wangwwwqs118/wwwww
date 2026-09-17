import os
from flask import Flask, render_template, request, jsonify
from supabase import create_client, Client

app = Flask(__name__)

# 請填入你的 Supabase 連線資訊
SUPABASE_URL = "https://hkgvyjluqhnvwhjgjlza.supabase.co"
SUPABASE_KEY = "sb_publishable_jTGKCg5Fd3rm1w9GYZ9USw_0N5EZNVe"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
def index():
    query = supabase.table('products').select('*')
    
    # 接收前台傳遞的分類與搜尋關鍵字
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