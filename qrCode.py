#most importantly for this code to run is to import OpenCV
import cv2
import pyzbar.pyzbar as pyzbar
import json

# set up camera object called Cap which we will use to find OpenCV
try:
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise Exception("Could not open video device.")
    
    # Rest of your code here
except Exception as e:
    print(e)

font = cv2.FONT_HERSHEY_PLAIN

def run():
    
    try:   
        #This creates an Infinite loop to keep your camera searching for data at all times
        while True:
    
            # Below is the method to get a image of the QR code
            _, img = cap.read()
    
            # Below is the method to read the QR code by detetecting the bounding box coords and decoding the hidden QR data 
            decodedObjects = pyzbar.decode(img)
    
            # This is how we get that Blue Box around our Data. This will draw one, and then Write the Data along with the top
            for obj in decodedObjects:
                
                print(str(obj.data, 'utf-8'))
                json_data = json.loads(json.dumps(eval(str(obj.data, 'utf-8'))))
                cv2.putText(img, str(obj.data), (50, 50),font, 2, (255, 0, 0), 3)
        
                format = json_data['format']
                length = json_data['length']
                inner = json_data['inner']
                print('json data detect in qrcode:\n'+format+'\n'+str(length)+'\n'+str(inner)+'\n')
                if json_data:
                    print("data found: ", json_data)
            
                    cap.release()
                    cv2.destroyAllWindows() 
                    return format, length, inner

            
            # Below will display the live camera feed to the Desktop on Raspberry Pi OS preview
            cv2.imshow("code detector", img)
    
            #At any point if you want to stop the Code all you need to do is press 'q' on your keyboard
            if(cv2.waitKey(1) == ord("q")):
                break
    
        # When the code is stopped the below closes all the applications/windows that the above has created
        cap.release()
        cv2.destroyAllWindows()

    except KeyboardInterrupt:
        key = cv2.waitKey(1)
        if key == 27:
            # When the code is stopped the below closes all the applications/windows that the above has created
            cap.release()
            cv2.destroyAllWindows()
            return
