import socket
import DH as dh
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad
import binascii

con = socket.socket()

con.connect(('localhost',8050))
print("Conectado al servidor")

def Decriptar(texto):
   key =  b'Sixteen byte key'
   dcipher = AES.new(key, AES.MODE_CBC, iv=b'0123456789abcdef')
   data = unpad(dcipher.decrypt(texto), AES.block_size)
   return data.decode()
   


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

      dataD = binascii.unhexlify(texto)
      decifrado = Decriptar(dataD)
      archivo = open("mensajerecibido.txt","w")
      archivo.write(decifrado)
      archivo.close()
      break
   
con.close()
print("Conexión cerrada")



