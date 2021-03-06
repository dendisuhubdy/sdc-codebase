import obd
import time
import datetime
import numpy as np
import cv2

from pymongo import MongoClient

def main():
    # define On Board Diagnostics
    ports = obd.scan_serial()
    connection = obd.OBD(ports[0], baudrate=115200)

    # define camera capture
    cap = cv2.VideoCapture(0)

    #fourcc = cv2.VideoWriter_fourcc(*'XVID')
    #out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640,480))

    out = cv2.VideoWriter('../data/output.avi', -1, 20.0, (640,480))
    #out = cv2.VideoWriter('..\data\output.avi', -1, 20.0, (640,480))

    # define mongodb database

    client = MongoClient()
    db = client.selfdrivingcar

    # main loop

    #while (cap.isOpened()):
    while (True):
	cmd1    = obd.commands.RPM
	cmd2    = obd.commands.THROTTLE_POS
	cmd3    = obd.commands.ENGINE_LOAD
	cmd4    = obd.commands.SPEED

	response1 = connection.query(cmd1)
	response2 = connection.query(cmd2)
	response3 = connection.query(cmd3)
	response4 = connection.query(cmd4)

        ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

        result = db.selfdriving.insert_one({
                "drivingparams": {
                    "date": st,
                    "RPM": str(response1.value),
                    "THROTTLE_POS": str(response2.value),
                    "ENGINE_LOAD": str(response3.value),
                    "SPEED": str(response4.value)
                }
            }
	)

        ret, frame = cap.read()

	frame = cv2.flip(frame,0)

	# write the flipped frame
	#cv2.imshow('frame',frame)

        out.write(frame)

	print("Getting data for time " + st)

    # Release everything if job is finished
    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__=='__main__':
    main()
