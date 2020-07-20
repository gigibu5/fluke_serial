#!/usr/bin/env python3
import serial
import pygame

fluke_device = "/dev/ttyUSB0"

SIRINA = 400
VISINA = 150
FPS = 60

pygame.init()
zaslon = pygame.display.set_mode((SIRINA,VISINA))
clock = pygame.time.Clock()
done = False

pygame.display.set_caption('Fluke multimeter interface')
pygame.font.init()

pisava = pygame.font.SysFont("Ericsson Hilda", 60)
fluke_logo = pygame.image.load("fluke_logo.png")
fluke_logo = pygame.transform.scale(fluke_logo, (405, 86))
pygame.display.set_icon(fluke_logo)

def getLine(serial_device):
	out = ""
	while True:
		s = serial_device.read()
		if(s == b"\r"):
			break
		else:
			out += s.decode("utf-8")
	return out

def toNum(string):
	temp = 0
	pozicija_pike = string.find(".")
	i = pozicija_pike - 1
	veckratnik = 1
	while(i > 0):
		temp += veckratnik * int(string[i])
		veckratnik *= 10
		i -= 1
	i = pozicija_pike + 1
	veckratnik = 0.1
	while(i < len(string)):
		temp += veckratnik * int(string[i])
		veckratnik /= 10
		i += 1
	if(string[0] == "-"):
		temp *= -1
	# print(type(temp))
	# print(temp)
	return round(temp, 4)

def get_text_multi(serial_device):
	serial_device.write(b"QM\r")
	getLine(serial_device) # zneba ničle
	measure = getLine(serial_device)
	#print("Dobil: " + measure)
	measure = measure.split(",")
	measuree = measure[1].split(" ")
	#print(measuree)

	if(len(measuree) > 3):
		return "Out of range"
	else:
		measuree[0] = toNum(measuree[0])
		if(len(measuree) == 3):
			if(measuree[1] == ""):
				return str(measuree[0]) + " " + measuree[2]
			elif(measuree[1] == "Deg"):
				return str(measuree[0])+" °"+measuree[2]
			else:
				return str(measuree[0]) + " " + measuree[1] + " " + measuree[2]
		elif(len(measuree) == 2):
			return str(measuree[0]) + " " + measuree[1]

fluke = serial.Serial(fluke_device)

while not done:
	for event in pygame.event.get():  
		if event.type == pygame.QUIT:  
			done = True  
	zaslon.fill((255,191,0))

	zaslon.blit(fluke_logo, (0,0))
	napis = pisava.render(get_text_multi(fluke), False, (0,0,0))
	zaslon.blit(napis, ((zaslon.get_width()-napis.get_width())/2,75))
	pygame.display.update()
