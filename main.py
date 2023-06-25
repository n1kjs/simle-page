import http.server
import socketserver
import urllib.parse

PORT = 80
user_data = {}

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            with open('index.html', 'rb') as file:
                content = file.read().decode('utf-8')
                self.wfile.write(content.encode('utf-8'))
        elif self.path == '/styles.css':
            self.send_response(200)
            self.send_header("Content-type", "text/css; charset=utf-8")
            self.end_headers()
            with open('styles.css', 'rb') as file:
                self.wfile.write(file.read())
        elif self.path == '/greeting':
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            with open('greeting.html', 'rb') as file:
                content = file.read().decode('utf-8')
                content = content.replace("{name}", user_data.get('name', ''))
                content = content.replace("{surname}", user_data.get('surname', ''))
                self.wfile.write(content.encode('utf-8'))
        else:
            self.send_response(404)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        params = urllib.parse.parse_qs(post_data)
        user_data['name'] = params['name'][0]
        user_data['surname'] = params['surname'][0]

        self.send_response(302)
        self.send_header('Location', '/greeting')
        self.end_headers()

with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print("Сервер запущен на порту", PORT)
    httpd.serve_forever()
