import argparse
import time
import cv2
import os
from ultralytics import YOLO
import pywhatkit
from datetime import datetime
import socket

def check_time_limit(until_str):
    if not until_str:
        return False
    
    now = datetime.now()
    try:
        target_hour = int(until_str[:2])
        target_min = int(until_str[2:])
        
        target_time = now.replace(hour=target_hour, minute=target_min, second=0, microsecond=0)
        
        if now > target_time:
            return True
    except ValueError:
        return True
        
    return False

def is_connected():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--number", required=True)
    parser.add_argument("--mode", choices=['single', 'continuous'], default='single')
    parser.add_argument("--delay", type=int, default=0)
    parser.add_argument("--out", default="detections")
    parser.add_argument("--interval", type=int, default=3)
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--until", type=str, default=None)
    
    args = parser.parse_args()

    if not os.path.exists(args.out):
        os.makedirs(args.out)

    time.sleep(args.delay)

    model = YOLO("yolov8n.pt")
    cap = cv2.VideoCapture(0)
    
    alerts_sent = 0

    try:
        while True:
            if args.until and check_time_limit(args.until):
                break

            if args.mode == 'continuous' and alerts_sent >= args.limit:
                break

            detected = False
            frame = None

            ret, frame = cap.read()
            if not ret:
                break

            results = model(frame, verbose=False)
            
            for result in results:
                for box in result.boxes:
                    cls = int(box.cls[0])
                    if cls == 0:
                        detected = True
                        break
                if detected:
                    break
            
            if detected:
                timestamp = int(time.time())
                file_path = os.path.abspath(os.path.join(args.out, f"alert_{timestamp}.png"))
                
                cv2.imwrite(file_path, frame)
                
                try:
                    if is_connected():
                        pywhatkit.sendwhats_image(args.number, file_path, f"Alert! Person Spotted at {datetime.now().strftime('%H:%M:%S')}", 7, True)
                        alerts_sent += 1
                except Exception:
                    pass

                if args.mode == 'single':
                    break
                
                elif args.mode == 'continuous':
                    time.sleep(args.interval)
                    for _ in range(5):
                        cap.read()
            
            if not detected:
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()