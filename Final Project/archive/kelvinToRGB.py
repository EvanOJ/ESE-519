import math

def clamp(n,smallest,largest):
	return max(smallest,min(n,largest))

def tempToRGB(kelvin):
	temp = kelvin/100


	if(temp <= 66):
		red = 255
		green = temp
		green = tempgreen = 99.4708025861 * math.log(green) - 161.1195681661

		if(temp <= 10):
			blue = 0
		else:
			blue = temp - 10
			blue = 138.5177312231 * math.log(blue) - 305.0447927307
	else:
		red = temp - 60
		red = 329.698727446 * math.pow(red, -0.1332047592)
		green = temp - 60
		green = 288.1221695283 * math.pow(green, -0.0755148492 )
		blue = 255

	r = clamp(red,0,255)
	g = clamp(green,0,255)
	b = clamp(blue,0,255)
	
	return (r,g,b)

def main():
	print(tempToRGB(15000))

main()
if __name__ == "__name__":
	main()