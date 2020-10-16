from os import remove
try:
    remove("mensajerecibido.txt")
except:
    pass

a = open("mensajeentrada.txt","w+")
a.write("Holanda Que Talca")
a.close()
