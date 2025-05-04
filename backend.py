from flask import Flask, request, jsonify
import requests
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

def process_url(url):
    try:
        # Contoh parsing sederhana (sesuaikan dengan struktur PoopHD)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        video_tag = soup.find('source', {'type': 'video/mp4'})
        return {
            "url_input": url,
            "title": soup.title.string,
            "video_url": video_tag['src'] if video_tag else "No video found"
        }
    except Exception as e:
        return {"url_input": url, "error": str(e)}

@app.route('/mass_download', methods=['POST'])
def mass_download():
    data = request.json
    urls = data.get("urls", [])
    
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(process_url, urls))
    
    return jsonify({"results": results})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
