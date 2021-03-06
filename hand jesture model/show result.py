import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import ImageFont, ImageDraw, Image
 
#%%
model = load_model('./hand jesture model/model.h5')
model.summary()
 
# open webcam (웹캠 열기)
webcam = cv2.VideoCapture(0)
 
if not webcam.isOpened():
    print("Could not open webcam")
    exit()
      
# loop through frames
while webcam.isOpened():
    
    # read frame from webcam 
    status, frame = webcam.read()
    
    if not status:
        break
    
    img = cv2.resize(frame, (224, 224), interpolation = cv2.INTER_AREA)
    x = img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
 
    prediction = model.predict(x)
    predicted_class = np.argmax(prediction[0]) # 예측된 클래스 0, 1, 2
    print(prediction[0])
    print(predicted_class)
 
    
    if predicted_class == 0:
        me = "한 손- 1"
    elif predicted_class == 1:
        me = "한 손- 2"        
    elif predicted_class == 2:
        me = "한 손- 손바닥 아래"
    elif predicted_class == 3:
        me = "한 손- 손날"        
    elif predicted_class == 4:
        me = "한 손- 주먹"
    elif predicted_class == 5:
        me = "두 손- 왼 주먹"        
    elif predicted_class == 6:
        me = "두 손- 오른 주먹"
    elif predicted_class == 7:
        me = "두 손- 왼 손바닥 위"        
    elif predicted_class == 8:
        me = "두 손- 오른 손바닥 위"
    elif predicted_class == 9:
        me = "두 손- 손목 비틀기"        
                
    # display
    fontpath = "font/gulim.ttc"
    font1 = ImageFont.truetype(fontpath, 100)
    frame_pil = Image.fromarray(frame)
    draw = ImageDraw.Draw(frame_pil)
    draw.text((50, 50), me, font=font1, fill=(0, 0, 255, 3))
    frame = np.array(frame_pil)
    cv2.imshow('RPS', frame)
        
    # press "Q" to stop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
# release resources
webcam.release()
cv2.destroyAllWindows()  