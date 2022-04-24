from msilib import type_string
import face_recognition
import cv2
import os
from datetime import datetime
import numpy as np
def attend():
    path="images"
    images=[]
    personName=[]
    myList=os.listdir(path)
    print(myList)
    for cu_img in myList:
        current_Img=cv2.imread(f'{path}/{cu_img}')
        images.append(current_Img)
        personName.append(os.path.splitext(cu_img)[0])
    print(personName) 

    def faceEncodings(images):
        encodeList=[]
        for img in images:
            img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            encode=face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList
    encodeListKnown=faceEncodings(images)
    print("All Encoding Completed")
    # print(faceEncodings(images))
    # hog transformation encoding used
    def attendance(name):
        print("start")
        print("line 32",name)
        with open('Attendance.csv','r+') as f:
            myDataList=f.readlines()
            nameList=[]
            entryList=[]

            for line in myDataList:
                entry=line.split(',')
                
                entryList.append(entry)
                nameList.append(entry[0])
            print("line 43",entryList)
            if name not in nameList:
                time_now=datetime.now()
                tStr=time_now.strftime('%H:%M:%S')
                dStr=time_now.strftime('%d/%m/%Y')
                print("inside 47 line ")
                f.write("\n")
            
                f.writelines(f'{name},{tStr},{dStr},{1},{30},{3.33}')
                return 
            i=0
            print("line 51",nameList)
            caught=-1
            days=[]
            for n in nameList:
              
                if(name==n):
                    caught=i
                    time_now=datetime.now()
                    print("line 57",entryList[i])
                    # time_now=datetime.now()
                    # prev=datetime.strptime(entryList[i][2]+" "+entryList[i][1],'%d/%m/%Y %H:%M:%S')
                    # time_diff=time_now-prev
                    # print(time_diff.days)
                    time_diff= datetime.now() - datetime.strptime(entryList[i][2]+" "+entryList[i][1],'%d/%m/%Y %H:%M:%S' )
                    duration=time_diff.total_seconds()
                  
                    days = list(divmod(duration, 86400))        # Get days (without [0]!)
                    print(type(days))
                    hours   = divmod(days[1], 3600) 
                    # print(type(int(hours[0])))   
                    # # print("days=",time_diff.days)
                    
                    print(days)
                 
                    
                 
                i+=1
            if( int(days[0])>=1):
                        print("line 71 days=",int(days[0]))
                        time_now=datetime.now()
                        tStr=time_now.strftime('%H:%M:%S')
                        dStr=time_now.strftime('%d/%m/%Y')
                        f.write("\n")
                        p=int(entryList[caught][3])+1
                        print("inside 76 line")
                        perc=(p*100)/30
                        f.writelines(f'{name},{tStr},{dStr},{p},{30},{perc}')
           


    cap=cv2.VideoCapture(0)
    # for laptop camera id is 0 and external camera it is 1

    while True:
        
        print("line 90")
        ret,frame=cap.read()
        faces=cv2.resize(frame,(0,0),None,0.25,0.25)
        # fx and fy deides the size of frame
        faces=cv2.cvtColor(faces,cv2.COLOR_BGR2RGB)
        # cv2 retyrns the images or video in bgr forat so we cinvert it t rgb format here
        facesCurrentFrame =face_recognition.face_locations(faces)
        encodesCurrentFrame=face_recognition.face_encodings(faces,facesCurrentFrame)
        for encodeFace,faceLoc in zip(encodesCurrentFrame,facesCurrentFrame):
            matches=face_recognition.compare_faces(encodeListKnown,encodeFace)
            faceDis=face_recognition.face_distance(encodeListKnown,encodeFace)
            
            matchIndex=np.argmin(faceDis)

            if matches[matchIndex]:
                name=personName[matchIndex].upper()
                y1,x2,y2,x1=faceLoc
                y1,x2,y2,x1=y1*4,x2*4,y2*4,x1*4
                cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.rectangle(frame,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                cv2.putText(frame,name,(x1+6,y2+6),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
                attendance(name)
            print("line 112")
                
        
        cv2.imshow("Camera",frame)
        if cv2.waitKey(10)==13:
            print("line 117")
            break
    cap.release()
    cv2.destroyAllWindows()







