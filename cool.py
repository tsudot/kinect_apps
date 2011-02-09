import freenect
import matplotlib.pyplot as mp
import frame_convert
import signal
import Queue
import numpy as np
import uinput
import time

keep_running = True
last_point_location = Queue.LifoQueue(4)
go = False

capabilities = {uinput.EV_ABS: [uinput.ABS_X, uinput.ABS_Y],
				uinput.EV_KEY: [uinput.BTN_LEFT, uinput.BTN_RIGHT],
				}

device = uinput.Device(name="python-uinput-mouse",
						capabilities=capabilities)

def get_depth():
	d,_ = freenect.sync_get_depth()
	
	try:
		np.where(d <= 600)[0][0]
		points = np.where(d <=600)
		go = True
	except:
		IndexError
		go = False
	
	if go:
		device.emit(uinput.EV_ABS, uinput.ABS_X, points[0][0], syn=False)
		device.emit(uinput.EV_ABS, uinput.ABS_Y, points[0][1])
#		time.sleep(0.01)
		print "x: %d"%(points[0][0])
		print "y: %d"%(points[0][1])
	
	else:
		device.emit(uinput.EV_ABS, uinput.ABS_X, 10, syn=False)
		device.emit(uinput.EV_ABS, uinput.ABS_Y, 20)
		print 'no 2000'
		print d[240, 320]
	return frame_convert.pretty_depth(d)[120:360, 160:480]


def get_video():
	return freenect.sync_get_rgb()[0][120:360, 160:480]

def handler(signum, frame):
	"""Sets up the kill handler, catches SIGINT"""
	global keep_running
	keep_running = False

mp.ion()
mp.gray()
mp.figure(1)
image_depth = mp.imshow(get_depth(), interpolation='nearest', animated=True)
mp.figure(2)
image_rgb = mp.imshow(get_video(), interpolation='nearest', animated=True)
print('Press Ctrl-C in terminal to stop')
signal.signal(signal.SIGINT, handler)

while keep_running:
	mp.figure(1)
	image_depth.set_data(get_depth())
	mp.figure(2)
	image_rgb.set_data(get_video())
	mp.draw()
	mp.waitforbuttonpress(0.01)
