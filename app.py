from flask import Flask, request, jsonify, send_from_directory
from urllib.parse import urlparse, urljoin
import ipaddress, socket, requests

app = Flask(__name__, static_folder="static")

def is_public_host(host):
    try:
        infos = socket.getaddrinfo(host, None)
        ips = {info[4][0] for info in infos}
        return bool(ips) and all(ipaddress.ip_address(ip).is_global for ip in ips)
    except Exception:
        return False

@app.get("/")
def home():
    return send_from_directory("static", "index.html")

@app.post("/resolve")
def resolve():
    data = request.get_json(silent=True) or {}
    raw = (data.get("url") or "").strip()
    try:
        p = urlparse(raw)
        if p.scheme not in ("http", "https") or p.hostname != "gtraffic.io":
            return jsonify(error="Chỉ nhận link bắt đầu từ https://gtraffic.io/"), 400
        if not is_public_host(p.hostname):
            return jsonify(error="Không thể xác minh địa chỉ máy chủ an toàn."), 400

        # Only inspect the first ordinary HTTP redirect. Do not solve CAPTCHA,
        # submit verification codes, execute page scripts, or evade anti-bot checks.
        r = requests.get(
            raw, allow_redirects=False, timeout=12,
            headers={"User-Agent": "Mozilla/5.0 (compatible; LinkCheck/1.0)"},
            stream=True
        )
        status = r.status_code
        location = r.headers.get("Location")
        r.close()

        if status in (301, 302, 303, 307, 308) and location:
            dest = urljoin(raw, location)
            dp = urlparse(dest)
            if dp.scheme not in ("http", "https"):
                return jsonify(error="Máy chủ trả về kiểu chuyển hướng không được hỗ trợ.")
            return jsonify(status="redirect", destination=dest,
                           note="Đây là chuyển hướng HTTP thông thường; hãy mở link đích để tiếp tục.")
        return jsonify(status="manual",
                       note="GTraffic không trả về chuyển hướng HTTP trực tiếp. Trang có thể cần JavaScript, CAPTCHA hoặc thao tác xác nhận thủ công.",
                       http_status=status)
    except requests.RequestException:
        return jsonify(error="Không kết nối được GTraffic. Hãy thử lại sau."), 502
    except Exception:
        return jsonify(error="Không xử lý được link này."), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
