import serial
import time

# กำหนดการเชื่อมต่อ Serial
comport = 'COM16'  # พอร์ตที่ Arduino เชื่อมต่อ
baudrate = 9600

# เชื่อมต่อกับ Arduino
arduino = serial.Serial(comport, baudrate, timeout=1)
time.sleep(2)  # รอให้ Arduino พร้อม

def led(total):
    """ส่งคำสั่งไปยัง Arduino เพื่อควบคุม LED"""
    command = str(total)  # แปลงตัวเลขเป็นสตริง
    arduino.write(command.encode())  # ส่งคำสั่งไปยัง Arduino
    time.sleep(0.1)  # รอให้ Arduino ประมวลผลคำสั่ง

# ฟังก์ชันสำหรับปิดการเชื่อมต่อ
def close():
    arduino.close()
