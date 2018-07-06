#!/usr/bin/env python


from picamera import PiCamera
from time import sleep
from sense_hat import SenseHat
from pynput import keyboard
import cv2
import os
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders


def take_photos():
	x = 0
	cycle= True
	sense = SenseHat()
	camera = PiCamera()
	camera.rotation = 180

	camera.start_preview()

	
	while cycle:
		event = sense.stick.wait_for_event()
		if event.action == "pressed":
			x += 1
			path= "/home/pi/Desktop/animation/frame%03d.jpg" % x
			camera.capture(path)
			print "Taking photo " + path
			
			if x==10:
				break


	camera.stop_preview()

	return x



def main():
	num_fotos=take_photos()
	images=[]
	for x in range(1, num_fotos+1):
		path = '/home/pi/Desktop/animation/frame%03d.jpg' % x
		print "Appending " + path
		images.append(path)

	vid = make_video(images)
	send_email(vid)
	
def make_video(gg):
	try:
		os.remove("/home/pi/Desktop/animation2.mp4")
	except OSError, e:  ## if failed, report it back to the user ##
		print "Error: " + e.filename
	os.system("avconv -r 4 -i animation/frame%03d.jpg -qscale 5  animation2.mp4")
	return "animation2.mp4"


"""
def make_video(images, fps=2, size=None, is_color=True, format='I420'):
	fourcc = cv2.cv.CV_FOURCC(*format)
	vid = None
	outvid = "video4.avi"
	for image in images:
		print "saving " + image
		if not os.path.exists(image):
			raise FileNotFoundError(image)
		img = cv2.imread(image)

		if vid is None:
			if size is None:
				size = img.shape[1], img.shape[0]
			vid = cv2.VideoWriter(outvid, fourcc, float(fps), size)
			if size[0] != img.shape[1] and size [1] != img.shape[0]:
				img = cv2.resize(img, size)
				print img

		vid.write(img)

	vid.release()
	return outvid
"""   


def send_email(filename):
	fromaddr = "cacaslindas@gmail.com"
	toaddr = "cacaslindas@gmail.com"

	msg =MIMEMultipart()

	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = "Video stop motion"

	body = "ola"

	msg.attach(MIMEText(body,'plain'))

	attachment = open("/home/pi/Desktop/"+filename, "rb")

	part = MIMEBase('application', 'octet-stream')
	part.set_payload((attachment).read())
	encoders.encode_base64(part)
	part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

	msg.attach(part)

	server = smtplib.SMTP_SSL('smtp.gmail.com',465)

	server.login(fromaddr, "cacaslindas1234")
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()
	


if __name__ == "__main__":
	main()
