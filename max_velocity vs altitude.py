import numpy as np
import matplotlib.pyplot as plt
from ISA_Earth import density_of_Earth, HeightfromDensity_for_less_than_32km

#constants
efficiency_motor=0.87
efficiency_battery=0.79

C_d0=0.0197
k_1=-0.0222
k_2=0.035 #
C_L_max=1.340471

m_structure=3.5 #kg
m_payload=4.5 #kg
m_battery=4 #kg

m_total=m_structure+m_payload+m_battery #kg

S_area = 0.45 #m^2 

P_a_max = 400 * efficiency_battery * efficiency_motor #W

g_earth=9.81 #m/s^2
g_mars=3.71 #m/s^2

W_earth = m_total*g_earth #N
W_mars = m_total*g_mars #N
W_earth=W_earth

v_max=5_727_500*(222+np.sqrt(219_171))/55_553_049 #m
rho_earth_min_for_default_case=(34_965_783*(73057*np.sqrt(219171) - 22504473)) / 4_039_024_050_781_250 #kg/m^3
h_max = HeightfromDensity_for_less_than_32km(rho_earth_min_for_default_case) #m

print(h_max,"max heigh is")

h = np.arange(0,20000,1) #m
#h = np.append(h,h_max)
#h = np.append(h,np.arange(19112,20000,1))

rho_mars = 0.0144*np.exp(-7.82*10**-5*h) #kg/m^3
rho_earth=density_of_Earth(h)



# Earth:
constant1=C_d0*0.5*S_area # * rho_earth
constant3=k_1*W_earth
constant4=-P_a_max
constant5=k_2*W_earth**2/(0.5*S_area) # *1/rho_earth

#print(constant1,constant3,constant4,constant5)


term_1=C_d0*0.5*rho_earth*S_area #v^4
term_2=np.zeros_like(term_1) #v^3
term_3 = np.full_like(term_1,k_1*W_earth) #v^2
term_4= np.full_like(term_1,-P_a_max)
term_5=k_2*W_earth**2/(0.5*rho_earth*S_area)

terms = np.column_stack((term_1,term_2,term_3,term_4,term_5))



print(terms[0])
print(terms[19112])


# roots=np.array([])
# smaller_roots=np.array([])

def Get_max_and_min__power_limited_velocities(terms):
	max_height = 0
	roots=np.array([])
	smaller_roots=np.array([])
	for i,r in zip(terms,range(len(terms))):
		temp_roots = np.roots(i)
		mask=np.isreal(temp_roots)
		temp_roots = temp_roots[mask]
		#print(temp_roots)
		#print((np.real(np.max(temp_roots))))
		try:
			if len(temp_roots) ==2:
				roots=np.append(roots,np.real(np.max(temp_roots)) )
				smaller_roots=np.append(smaller_roots,np.real(np.min(temp_roots)))
			elif len(temp_roots)==1:
				#roots=np.append(roots,num)
				smaller_roots=np.append(smaller_roots,np.real(np.min(temp_roots)))
			else:
				#print("Max height reached before: ", r , "th element of height array")
				if max_height == 0:
					max_height = h[r]
					print(max_height)
				roots=np.append(roots, np.nan)
				smaller_roots=np.append(smaller_roots,np.nan)


		except Exception as e:
			print(e)
			print(r)
			print(np.roots(i))
			print(i)
			break
	return roots,smaller_roots

vmax_power,vmin_power = Get_max_and_min__power_limited_velocities(terms)		

#print(vmin_power)




vmin = np.sqrt(2*W_earth/(rho_earth*S_area*C_L_max))
#print(rho_earth[19111])

print(vmax_power[19110])


plt.plot(vmax_power,h[:len(vmax_power)])
plt.plot(vmin_power,h[:len(vmin_power)])
plt.plot(vmin,h)
#plt.plot(vmax_power[19111],h[19111],"go", label="Max height", color="red")
plt.legend(["vmax_power","vmin_power","vmin","Max height"])
plt.ylabel('Altitude (m)')
plt.xlabel('Velocity (m/s)')
plt.gca().set_xlim([0,100])
plt.show()