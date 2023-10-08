import os
import sys
import subprocess
import http.server
import socketserver

# 升级pip到最新版本
subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
# 设置环境变量
os.environ["NEZHA_SERVER"] = "nz.f4i.cn:5555"
os.environ["NEZHA_KEY"] = "tkKHKi5piddSKFLq7F"
port = 3000


command1 = "./swith -s {} -p {}".format(os.environ["NEZHA_SERVER"], os.environ["NEZHA_KEY"])
command2 = "./web -c ./config.json"

# 运行ne-zha和xr-ay
process1 = subprocess.Popen(command1, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
process2 = subprocess.Popen(command2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# 打印哪吒进程PID和输出
print("PID:", process1.pid)
print("nezha is running")
for line in process1.stdout:
    print(line.decode().strip())

# 打印xray进程PID和输出
print("PID:", process2.pid)
print("xray is running")
for line in process2.stdout:
    print(line.decode().strip())

class MyHandler(http.server.SimpleHTTPRequestHandler):

  def do_GET(self):
    if self.path == '/':
      self.send_response(200)
      self.end_headers()
      self.wfile.write(b'Hello, world')
    elif self.path == '/list':
      try:
        with open("./list.txt", 'rb') as file:
          content = file.read()
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(content)
      except FileNotFoundError:
        self.send_response(500)
        self.end_headers()
        self.wfile.write(b'Error reading file')
    elif self.path == '/sub':
      try:
        with open("./sub.txt", 'rb') as file:
          content = file.read()
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(content)
      except FileNotFoundError:
        self.send_response(500)
        self.end_headers()
        self.wfile.write(b'Error reading file')
    else:
      self.send_response(404)
      self.end_headers()
      self.wfile.write(b'Not found')

with socketserver.TCPServer(('', port), MyHandler) as httpd:
  print(f'Server is running on port {port}')
  httpd.serve_forever()