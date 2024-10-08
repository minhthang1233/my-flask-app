from flask import Flask, request, render_template
import urllib.parse
import requests

app = Flask(__name__)

# Hàm để mã hóa URL
def encode_link(link):
    base_url = link.split('?')[0]  # Lấy phần URL trước dấu hỏi
    return urllib.parse.quote(base_url, safe='')  # Mã hóa phần đó

# Hàm để giải mã liên kết rút gọn thành liên kết đầy đủ
def resolve_short_link(short_url):
    try:
        response = requests.head(short_url, allow_redirects=True)
        return response.url  # Trả về URL đầy đủ sau khi chuyển hướng
    except requests.RequestException:
        return None

@app.route('/')
def index():
    return render_template('index.html')

# Hàm xử lý kết quả khi người dùng nhập liên kết
@app.route('/generate_links', methods=['POST'])
def generate_links():
    original_link = request.form.get('link')

    if not original_link:
        return render_template('index.html', error="Vui lòng cung cấp liên kết.")

    full_link = resolve_short_link(original_link)

    if not full_link:
        return render_template('index.html', error="Không thể giải mã liên kết rút gọn.")

    encoded_link = encode_link(full_link)

    # Tạo 2 kết quả với các affiliate_id khác nhau
    result_1 = f"https://shope.ee/an_redir?origin_link={encoded_link}&affiliate_id=17385530062&sub_id=1review"
    result_2 = f"https://shope.ee/an_redir?origin_link={encoded_link}&affiliate_id=17305270177&sub_id=1review"

    # Đưa ra kết quả cho người dùng dưới dạng danh sách
    results = [result_1, result_2]

    return render_template('index.html', result=results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
