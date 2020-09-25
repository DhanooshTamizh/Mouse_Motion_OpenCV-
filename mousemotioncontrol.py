import cv2
import numpy as np
from pynput.mouse import Button, Controller
import wx

mouse=Controller()
app=wx.App(False)
dx,dy=wx.GetDisplaySize()
fx,fy=(320,240)
lower=np.array([33,80,40])
upper=np.array([102,255,255])
cam= cv2.VideoCapture(0)
kernelOpen=np.ones((10,10))
while(True):
  ret,img=cam.read()
  img=cv2.resize(img,(330,220))
 
  imgHSV=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
  mask=cv2.inRange(imgHSV,lower,upper)
  maskOpen=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
  
  maskFinal=maskOpen
  conts,h=cv2.findContours(maskFinal.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
  
  if len(conts)==2:
      mouse.release(Button.left)
      x1,y1,w1,h1=cv2.boundingRect(conts[0])
      x2,y2,w2,h2=cv2.boundingRect(conts[1])
      cv2.rectangle(img,(x1,y1),(x1+w1,y1+h1),(0,0,255),2)
      cv2.rectangle(img,(x2,y2),(x2+w2,y2+h2),(0,0,255),2)
      
      centrex1=int(x1+w1/2)
      centrey1=int(y1+h1/2)
      centrex2=int(x2+w2/2)
      centrey2=int(y2+h2/2)
      centrelx=int((centrex1+centrex2)/2)
      centrely=int((centrey1+centrey2)/2)
      cv2.line(img,(centrex1,centrey1),(centrex2,centrey2),(0,255,0),2)
      cv2.circle(img,(centrelx,centrely),2,(255,0,0),2)
      
      mouse.position=(int(dx-(centrelx*dx/fx)),int(centrely*dx/fy))
      while mouse.position!=(int(dx-(centrelx*dx/fx)),int(centrely*dx/fy)):
          pass
  elif len(conts)==1:
      x,y,w,h=cv2.boundingRect(conts[0])
      cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
      centrex=int(x+w/2)
      centrey=int(y+h/2)
      cv2.circle(img,(centrex,centrey),int((w+h)/4),(0,0,255),2)
      mouse.press(Button.left)
      mouseLoc=(int(dx-(centrex*dx/fx)), int(centrey*dy/fy))
      mouse.position=mouseLoc 
      while mouse.position!=mouseLoc: 
          pass
  cv2.imshow("camera",img)
  cv2.imshow("mask",mask)
  cv2.imshow("maskopen",maskOpen)
  if cv2.waitKey(10)==ord('q'):
    break


cam.release()
cv2.destroyAllWindows()