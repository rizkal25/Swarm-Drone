import socket
import threading
import time
# NB: socket berfungsi sebagai tautan komunikasi antara dua entitas

# MAC Address:
# A : 60-60-1F-5F-6A-1D
# B : 60-60-1F-62-77-B5

# IP & port dari Tello
tello1_address = ('192.168.0.100', 8889) #A
tello2_address = ('192.168.0.101', 8889) #B

# IP & port dari local computer
local1_address = ('', 9013) #A
local2_address = ('', 9011) #B

# Buat koneksi UDP yang akan dikirimi perintah
sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# NB: Argumen AF_INET menunjukkan bahwa kita meminta socket Internet Protocol (IP), khususnya IPv4

# Hubungkan alamat (nama host, nomor port) ke socket
sock1.bind(local1_address)
sock2.bind(local2_address)

# Kirim pesan/perintah ke Tello
def sendA(message, delay):
  try:
    sock1.sendto(message.encode(), tello1_address)
    print("Sending message: " + message)
  except Exception as e:
    print("Error sending: " + str(e))

  time.sleep(delay)

def sendAll(message, delay):
  try:
    sock1.sendto(message.encode(), tello1_address)
    sock2.sendto(message.encode(), tello2_address)
    print("Sending message: " + message)
  except Exception as e:
    print("Error sending: " + str(e))

  time.sleep(delay)

# Menerima pesan/perintah dari Tello
def receive():
  while True:
    # Mencoba untuk menerima pesan. Jika tidak, cetak pengecualian
    try:
      response1, ip_address = sock1.recvfrom(128)
      response2, ip_address = sock2.recvfrom(128)
      print("Received message: from Tello EDU #1: " + response1.decode(encoding='utf-8'))
      print("Received message: from Tello EDU #2: " + response2.decode(encoding='utf-8'))
    except Exception as e:
      # Jika ada kesalahan tutup soket dan keluar dari loop
      sock1.close()
      sock2.close()
      print("Error receiving: " + str(e))
      break

# Buat dan mulai membaca thread yang berjalan di latar belakang
receiveThread = threading.Thread(target=receive)
receiveThread.daemon = True
receiveThread.start()
# NB: Menggunakan fungsi penerimaan dan akan terus memantau pesan masuk

sendAll("command", 3)
sendAll("takeoff", 4)

# Tello A UP
sendA("up 75", 3)

# Gerak Kotak Horizontal
for i in range(4):
  sendAll("forward 50", 3)
  sendAll("cw 90", 4)

# Gerak Kotak Vertikal
sendAll("down 30", 3)
sendAll("right 50", 3)
sendAll("up 30", 3)
sendAll("left 50", 3)

sendAll("land", 3)
print("Mission completed successfully!")
sock1.close()
sock2.close()