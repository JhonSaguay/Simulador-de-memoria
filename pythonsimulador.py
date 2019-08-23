import sys
class Structure:
	def __init__ (self, a = -1, b = -1, c = -1, d = -1, e = 0):
		self.process = a
		self.logicPage = b 
		self.reference = c 
		self.dirty = d 
		self.clock = e 
class Process:
	def __init__ (self, a, b, c, d):
	        self.process = a
	        self.di = b
	        self.dm = c
	        self.type = d
#Leer archivos

def leerproceso(nombre,lis):
	try:
		file=open(nombre,'r')
	except:
		print('Error al leer el archivo con el nombre', nombre)
		return -1

	for process in file:
		process=process[:len(process)-1].split(' ')
		d=0
		if process[3] == 'W':
			d=1
		lis.append(Process(int(process[0]),int(process[1]),int(process[2]),d))
		
	file.close

	return lis

#quantum diferente de 0
def leerprocesoquantum(nombre):
	lis=[]
	try:
		file=open(nombre,'r')
	except:
		print('Error al leer el archivo con el nombre', nombre)
		return -1

	for process in file:
		process=process[:len(process)-1].split(' ')
		d=0
		if process[3] == 'W':
			d=1
		lis.append(Process(int(process[0]),int(process[1]),int(process[2]),d))
		
	file.close

	return lis
def creararchivo(lis,quantum):
	init=0
	afir=True
	archivo=[]
	while afir:
		cont=0
		for i in range(len(lis)):
			if init>=(len(lis[i])):
				cont+=1
		if cont==len(lis):
			break
		
		for j in range(len(lis)):
			star=init
			while star<init+quantum and star<len(lis[j]) :
				archivo.append(lis[j][star])
				star+=1
		init=init+quantum

	return (archivo)
#Parametros iniciales

def leerparametros(archivo):
	lis=[]
	try:
		file=open(archivo,'r')
	except :
		print('Error al leer el archivo con el nombre', archivo)

	for process in file:
		process = process[:len(process)-1].split()
		lis.append(process[0])
		
	return lis

#Estructurainicial
def startList(memorysize):
	lis = []
	for _ in range(memorysize):
		lis.append(Structure())
	return lis
#Version1 busqueda

def busquedaversion1(estructura):
	find = False
	escritura = False
	case = [(0,0),(0,1),(1,0),(1,1)]
	i=0
	while i < 4 and not find:
		pos = 0
		for elemento in estructura:
			if (elemento.reference,elemento.dirty)==case[i]:
				find=True
				if elemento.dirty==1:
					escritura=True
				return pos , escritura

			pos+=1
		i+=1
	return pos,escritura

#Estructura llena

def estructurallena(estructura,memorysize):
	empty=False	
	pos=0
	while pos<memorysize and not empty:
		if estructura[pos].process==-1:
			empty=True
		else:
			pos+=1

	return (pos,empty)

#Referencia 0
def refToZero(estructura):
	for elemento in estructura:
		elemento.reference = 0
	return estructura

#Buscar proceso en estructura

def buscarenestructura(estructura,proceso,direccion,pagesize):

	find=False
	index=0
	for elemento in estructura:
		if elemento.process==proceso.process and elemento.logicPage==direccion//pagesize:
			find=True
			break
		index+=1
		
	return index,find

#Version 1

def actualizarversion1(archivo,estructura,debug,pagesize,memorysize):
	contIns = 1
	cont = 1
	contFails = 0
	contEscritura = 0
	for process in archivo:
		pos1, find1 = buscarenestructura(estructura,process,process.di,pagesize)
		if find1:
			estructura[pos1] = Structure(process.process,process.di//pagesize,1,estructura[pos1].dirty or 0,cont)

		else:
			contFails+=1
			pos3 , empty= estructurallena(estructura,memorysize)
			if empty:
				estructura[pos3] = Structure(process.process,process.di//pagesize,1,0,cont)
			else:
				pos4, escritura = busquedaversion1(estructura)
				if debug:
					print ("---",'\t', cont,'\t',pos4,'\t',estructura[pos4].process,'\t',estructura[pos4].logicPage,'\t',estructura[pos4].dirty,'\t', "---")
		       
				if escritura:
					contEscritura+=1

				estructura[pos4] = Structure(process.process,process.di//pagesize,1,0,cont)
            
        
		pos2,find2 = buscarenestructura(estructura,process,process.dm,pagesize)

		if find2:
			estructura[pos2] = Structure(process.process,process.dm//pagesize,1,estructura[pos2].dirty or process.type,cont)

		else:

			contFails+=1
			pos3 , empty= estructurallena(estructura,memorysize)
			if empty:
				estructura[pos3] = Structure(process.process,process.dm//pagesize,1,process.type,cont)
			else:
				pos4, escritura = busquedaversion1(estructura)
				if debug:
					print ("---",'\t', cont,'\t',pos4,'\t',estructura[pos4].process,'\t',estructura[pos4].logicPage,'\t',estructura[pos4].dirty,'\t', "---")
				if escritura:
					contEscritura+=1
				estructura[pos4] = Structure(process.process,process.dm//pagesize,1,process.type,cont)
           
		if contIns == 200:
			estructura = refToZero(estructura)
			contIns = 0
		
		contIns+=1
		cont+=1
	
	return contFails, contEscritura,estructura

#Version 2 busqueda
def lowerClock(lis):
	j = 0
	for i in range(len(lis)):
		if lis[i].clock < lis[j].clock:
			j = i
	return j

def busquedaversion2(lis):
	pos = lowerClock(lis)
	write = lis[pos].dirty or 0
	return pos , write

#Version 2

def actualizarversion2(archivo,estructura,debug,pagesize,memorysize):
	contIns = 1
	cont = 1
	contFails = 0
	contEscritura = 0
	for process in archivo:
		pos1, find1 = buscarenestructura(estructura,process,process.di,pagesize)
		if find1:
			estructura[pos1] = Structure(process.process,process.di//pagesize,1,estructura[pos1].dirty or 0,cont)

		else:
			contFails+=1
			pos3 , empty= estructurallena(estructura,memorysize)
			if empty:
				estructura[pos3] = Structure(process.process,process.di//pagesize,1,0,cont)
			else:
				pos4, escritura = busquedaversion2(estructura)
				if debug:
					print ("---",'\t', cont,'\t',pos4,'\t',estructura[pos4].process,'\t',estructura[pos4].logicPage,'\t',estructura[pos4].dirty,'\t', "---")
		       
				if escritura:
					contEscritura+=1

				estructura[pos4] = Structure(process.process,process.di//pagesize,1,0,cont)
            
        
		pos2,find2 = buscarenestructura(estructura,process,process.dm,pagesize)

		if find2:
			estructura[pos2] = Structure(process.process,process.dm//pagesize,1,estructura[pos2].dirty or process.type,cont)

		else:

			contFails+=1
			pos3 , empty= estructurallena(estructura,memorysize)
			if empty:
				estructura[pos3] = Structure(process.process,process.dm//pagesize,1,process.type,cont)
			else:
				pos4, escritura = busquedaversion2(estructura)
				if debug:
					print ("---",'\t', cont,'\t',pos4,'\t',estructura[pos4].process,'\t',estructura[pos4].logicPage,'\t',estructura[pos4].dirty,'\t', "---")
				if escritura:
					contEscritura+=1
				estructura[pos4] = Structure(process.process,process.dm//pagesize,1,process.type,cont)
           
		if contIns == 200:
			estructura = refToZero(estructura)
			contIns = 0
		
		contIns+=1
		cont+=1
	
	return contFails, contEscritura,estructura

###
#Funcion principal
def main():
	
	Parameter = sys.argv
	l = len(Parameter)
	Parametros=leerparametros(Parameter[1])
	pagesize=int(Parametros[0])
	memorysize=int(Parametros[1])
	quantum=int(Parametros[2])
	process=int(Parametros[3])

	if quantum!=0:
		temp=[]
		for i in range (process):
			temp.append(leerprocesoquantum(Parametros[4+i]))

		archivo=creararchivo(temp,quantum)
	
	else:
		temp=[]
		for i in range (1,process+1):
			archivo=leerproceso(Parametros[3+i],temp)
	print("READING DATA")
	
	l=len(Parameter)
	
	if l==3:
		Parameter.append('0')
		if Parameter[2] == '1':
			contFails, contWrites,_ =  actualizarversion1(archivo,startList(memorysize),int(Parameter[3]),pagesize,memorysize)
			print('PAGESIZE=',pagesize,'\nNumber of Frames=',memorysize,'\nQuantum=',quantum,'\nNumber of processes=',process)
			print ('Version: ',Parameter[2],'\nPage faults: ',contFails,'\tWritings: ',contWrites)
		
		elif Parameter[2] == '2':
			contFails, contWrites, _ =  actualizarversion2(archivo,startList(memorysize),int(Parameter[3]),pagesize,memorysize)
			print('PAGESIZE=',pagesize,'\nNumber of Frames=',memorysize,'\nQuantum=',quantum,'\nNumber of processes=',process)
			print ('Version: ',Parameter[2],'\nPage faults: ',contFails,'\tWritings: ',contWrites)
		

		else:
			print ('Version Desconocida')

   
	elif l < 3:
		print ('Error: La estructura es la siguiente, el tercer parametro es opcional')
		print ('''Menu:
		Parametro 1 : Nombre archivo
		Parametro 2 : Version(1/2)
		Parametro 3 : Debug(1/0) ''')
	else:
		
		if Parameter[2] == '1':
			contFails, contWrites,_ =  actualizarversion1(archivo,startList(memorysize),int(Parameter[3]),pagesize,memorysize)
			print('PAGESIZE=',pagesize,'\nNumber of Frames=',memorysize,'\nQuantum=',quantum,'\nNumber of processes=',process)
			print ('Version: ',Parameter[2],'\nPage faults: ',contFails,'\tWritings: ',contWrites)
		
		
		elif Parameter[2] == '2':
			contFails, contWrites, _ =  actualizarversion2(archivo,startList(memorysize),int(Parameter[3]),pagesize,memorysize)
			print('PAGESIZE=',pagesize,'\nNumber of Frames=',memorysize,'\nQuantum=',quantum,'\nNumber of processes=',process)
			print ('Version: ',Parameter[2],'\nPage faults: ',contFails,'\tWritings: ',contWrites)
		
		
		else:
			print ('Version Desconocida')

main()
