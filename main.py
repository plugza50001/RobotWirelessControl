import cv2
import mediapipe as mp
import time
import controller as cnt

time.sleep(2.0)

mp_draw = mp.solutions.drawing_utils
mp_hand = mp.solutions.hands

# ปลายนิ้วทั้ง 5
tipIds = [4, 8, 12, 16, 20]

# เปิดกล้อง
video = cv2.VideoCapture(0)

# ตั้งค่า MediaPipe
with mp_hand.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
    try:
        while True:
            ret, image = video.read()
            if not ret:
                break

            # แปลงสีจาก BGR เป็น RGB
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            # ประมวลผลภาพด้วย MediaPipe
            results = hands.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # กำหนดค่าเริ่มต้น
            closest_hand = None
            min_distance = float('inf')
            lmList = []

            # หากตรวจจับมือได้
            if results.multi_hand_landmarks:
                h, w, c = image.shape
                center_x, center_y = w // 2, h // 2  # จุดศูนย์กลางของเฟรม

                # หามือที่ใกล้ศูนย์กลางของเฟรมมากที่สุด
                for hand_landmark in results.multi_hand_landmarks:
                    # คำนวณตำแหน่งเฉลี่ยของมือ
                    avg_x = sum([lm.x for lm in hand_landmark.landmark]) / len(hand_landmark.landmark) * w
                    avg_y = sum([lm.y for lm in hand_landmark.landmark]) / len(hand_landmark.landmark) * h
                    
                    # คำนวณระยะห่างจากจุดศูนย์กลาง
                    distance = ((avg_x - center_x) ** 2 + (avg_y - center_y) ** 2) ** 0.5
                    if distance < min_distance:
                        min_distance = distance
                        closest_hand = hand_landmark
                
                # ประมวลผลมือที่ใกล้ที่สุด
                if closest_hand:
                    for id, lm in enumerate(closest_hand.landmark):
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        lmList.append([id, cx, cy])

                    # วาดเส้นเชื่อม Landmark ของมือ
                    mp_draw.draw_landmarks(image, closest_hand, mp_hand.HAND_CONNECTIONS)

            # ตรวจจับนิ้วที่ยกขึ้น
            fingers = []
            if len(lmList) != 0:
                
                if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)

                
                for id in range(1, 5):
                    if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                total = fingers.count(1)

                # ควบคุม LED ตามจำนวน
                cnt.led(total)

                # แสดงจำนวนและข้อความบนหน้าจอ
                cv2.rectangle(image, (20, 300), (270, 425), (0, 255, 0), cv2.FILLED)
                cv2.putText(image, str(total), (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
                cv2.putText(image, "LED", (100, 375), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)

            # แสดงผลภาพ
            cv2.imshow("VisionDrive:Hand Gesture Control System", image)

            # ตรวจสอบการกดปุ่ม 'q' หรือ ESC เพื่อออก
            k = cv2.waitKey(1)
            if k == ord('q') or k == 27:
                break

    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")
    finally:
        # ปิดการใช้งานกล้อง
        video.release()
        cv2.destroyAllWindows()