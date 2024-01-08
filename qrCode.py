import cv2
import pyzbar.pyzbar as pyzbar
import json

cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_PLAIN

def run():
    try:
        while True:
            _, img = cap.read()
            decodedObjects = pyzbar.decode(img)
    
            # Check if any QR code is detected
            if decodedObjects:
                for obj in decodedObjects:
                    try:
                        decoded_data = str(obj.data, 'utf-8')
                        print(decoded_data)

                        # Replace single quotes with double quotes
                        decoded_data = decoded_data.replace("'", "\"")


                        data = json.loads(decoded_data)
                        format = data['format']
                        length = data['length']
                        inner = data['inner']
                        print('json data detected in QR code:\n' + format + '\n' + str(length) + '\n' + str(inner) + '\n')
                        cv2.putText(img, str(obj.data), (50, 50), font, 2, (255, 0, 0), 3)
                        cap.release()
                        cv2.destroyAllWindows()


                        return format, length, inner
                    

                    except json.JSONDecodeError as e:
                        print("Error decoding JSON:", e)
                        continue
                    except Exception as e:
                        print("Error processing QR code data:", e)
                        continue

            cv2.imshow("code detector", img)
    
            if cv2.waitKey(1) == ord("q"):
                break
    
        cap.release()
        cv2.destroyAllWindows()

    except KeyboardInterrupt:
        key = cv2.waitKey(1)
        if key == 27:
            cap.release()
            cv2.destroyAllWindows()
            return
