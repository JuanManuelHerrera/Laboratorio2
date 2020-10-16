import socket
import DH as dh
from pyDes import *
import binascii

con = socket.socket()

con.connect(('localhost',8050))
print("Conectado al servidor")

def Decriptar(texto):
   llave = '123412341234ABCD'
   cipher = triple_des(llave, ECB, padmode = PAD_PKCS5)
   textoDecifrado = cipher.decrypt(texto)
   return textoDecifrado.decode()


privateKey = 13 #Llave privada cliente

#Llaves Publicas
array = [2305843009213693951,5614156465]

#Llave parcial Cliente

cliente = dh.DH_Endpoint(array[1], array[0], privateKey)
llaveParcial = str(cliente.generate_partial_key())

cont = 1

while True:
   if cont == 1:
      mens = input("Presione enter para iniciar la conexión: ")
      con.send(llaveParcial.encode('ascii'))
      recibido = con.recv(1024)
      llaveParcialServidor = recibido.decode('utf-8')
      array.append(int(llaveParcialServidor))
      cont = 2
      
   elif cont == 2:
      fullKey = str(cliente.generate_full_key(array[2]))
      con.send(fullKey.encode('ascii'))
      recibido = con.recv(1024)
      print(recibido.decode())
      cont = 0

   else:   
      recibido = con.recv(1024)
      texto = recibido.decode('utf-8')
      
      decifrado = Decriptar(binascii.unhexlify(texto))
      archivo = open("mensajerecibido.txt","w")
      archivo.write(decifrado)
      archivo.close()
      break
   
con.close()
print("Conexión cerrada")



