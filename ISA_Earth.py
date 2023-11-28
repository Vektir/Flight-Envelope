import numpy as np
import matplotlib.pyplot as plt
# Define the starting values

def density_of_Earth(h):
	g_0 = 9.80665  # m/s^2
	p_0 = 101325.0  # Pa
	T_0 = 288.150  # K


	#h=np.arange(0,32000,1)
	# Define the temperature gradients
	T_gradients = {
		"0-11 km": -6.5/1000,
		"11-20 km": 0.0,
		"20-32 km": 1.0/1000,
		"32-47 km": 2.8/1000,
	}

	# Define the density function

	T_1 = T_0 + T_gradients["0-11 km"] * 11_000
	T_2 = T_1 + T_gradients["11-20 km"] * (20_000-11_000)
	T_3 = T_2 + T_gradients["20-32 km"] * (32_000-20_000)
	def Temperature(h):
		if h<=11_000:
			T = T_0 + T_gradients["0-11 km"] * h
			return T
		elif h<=20_000:
			T=T_1 + T_gradients["11-20 km"] * (h-11_000)
			return T

		elif h<=32_000:
			T=T_2 + T_gradients["20-32 km"] * (h-20_000)
			return T
		elif h <= 47_000:
			T = T_3 + T_gradients["32-47 km"] * (h - 32_000)
			return T
	p_1 = p_0 * (T_1 / T_0) ** (-g_0 / (T_gradients["0-11 km"] * 287.05))
	p_2 = p_1 * np.exp(-g_0 / (T_1 * 287.05) * (20_000-11_000))
	p_3 = p_2 * (T_3 / T_2) ** (-g_0 / (T_gradients["20-32 km"] * 287.05))
	def Pressure(T, h):
		
		if h<=11_000:
			p = p_0 * (T / T_0) ** (-g_0 / (T_gradients["0-11 km"] * 287.05))
			return p
		elif h<=20_000:
			p = p_1 * np.exp(-g_0 / (T_1 * 287.05) * (h - 11_000))
			return p
		elif h<=32_000:
			p = p_2 * (T / T_2) ** (-g_0 / (T_gradients["20-32 km"] * 287.05))
			return p
		elif h<=47_000:
			p = p_3 * (T / T_3) ** (-g_0 / (T_gradients["32-47 km"] * 287.05))
			return p


	T=[Temperature(i) for i in h]
	standrad_pressure = [Pressure(i,i2) for i,i2 in zip(T,h)]

	density=[i/(287.05*j) for i,j in zip(standrad_pressure,T)]



	return np.copy(density)
	#print(density[31000])
	#plt.plot(h, density)
	#plt.show()


def HeightfromDensity_for_less_than_32km(rho):
	g_0 = 9.80665  # m/s^2
	p_0 = 101325.0  # Pa
	T_0 = 288.150  # K


	T_gradients = {
		"0-11 km": -6.5/1000,
		"11-20 km": 0.0,
		"20-32 km": 1.0/1000,
		"32-47 km": 2.8/1000,
	}

	T_1 = T_0 + T_gradients["0-11 km"] * 11_000
	T_2 = T_1 + T_gradients["11-20 km"] * (20_000-11_000)

	p_1 = p_0 * (T_1 / T_0) ** (-g_0 / (T_gradients["0-11 km"] * 287.05))
	p_2 = p_1 * np.exp(-g_0 / (T_1 * 287.05) * (20_000-11_000))
	a=T_gradients["11-20 km"]
	R=287.05
	#Temp=(T_2*(rho*287.05/p_2)**(-a*R/g_0))**(1/(1+a*R/g_0))
	#Temp = T_1*(rho/(p_1/R/T_1))**(-1/(g_0/(R*a)+1))


	#height = (Temp-T_2)/T_gradients["20-32 km"]+11_000
	# print(rho*R*T_2, "density")
	# print(p_1, "pressure ")
	# print(p_1/(rho*R*T_1),"ratio")
	# print(np.log(p_1/(rho*R*T_1)),"neshto")
	height = 11_000 + np.log((rho*R*T_1)/p_1)/(-g_0/(R*T_1))

	return height

h=np.arange(0,47000,1)
rho=density_of_Earth(h)
print(rho[46999])
#print(density_of_Earth(haaa))