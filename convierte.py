'''def separar(numstr):
    entero, decimal = numstr.split('.')
    precision = len(decimal) + 1
    return EnteroaBinario(int(entero)) +'.'+ DecimalaBinario(int(decimal),precision)


def EnteroaBinario(n):
    respuesta = ""
    if (n == 0):
        return 0
    while (n):
        respuesta += str(n&1)
        n = n >> 1
    respuesta = respuesta[::-1]
    return respuesta

def DecimalaBinario(n, precision):
    respuesta = ""
    if (n == 0):
        return 0
    while (n and precision > 0):
        respuesta += str(n&1)
        n = n >> 1
        precision -= 1
    return respuesta



archivo = open('operaciones.txt')
lineas = sumas = 0
for linea in archivo:
    lineas +=1
    num1, num2 =linea.strip().split(';')
    print(separar(num1), separar(num2))
archivo.close()'''

def decimal_a_bin(n):
    if (n == 0):
        return 0
    binario = ""
    while (n):
        binario = str(n % 2) + binario
        n // 2
    return binario

def bin_a_decimal(bin):
    decimal = 0
    largo_bin = len(bin)
    for i in range(largo_bin):
        bit = bin[largo_bin - i - 1]
        decimal += int(bit) * (2 ** i)
    return decimal

def decimal_a_IEEE754(n):
    if ( n == 0.0 ):
        return "0" * 32
    if (n < 0):
        signo = 1
        n = -n
    else:
        signo = 0
    
    entero = int(n)
    fraccion = n - entero
    entero_bin = decimal_a_bin(entero)
    fraccion_bin = ""

    while fraccion > 0 and len(fraccion_bin) < 23:
        fraccion *= 2
        bit = int(fraccion)
        fraccion_bin += str(bit)
        fraccion -= bit
    if entero:
        mantisa = entero_bin + fraccion_bin
        exponente = len(entero_bin) - 1
        mantisa = mantisa[1:24]
    else:
        mantisa = fraccion_bin
        exponente = 0
        while mantisa[0] != "1":
            mantisa = mantisa[1:]
            exponente -= 1
        mantisa = mantisa[1:24]
    exponente += 127
    exponente_bin = decimal_a_bin(exponente).zfill(8)

    return signo + exponente_bin + mantisa.ljust(23,'0')

def IEEE754_a_decimal(ieee):
    signo = ieee[0]
    exponente = ieee[1:9]
    mantisa = ieee[9:]

    exponente_decimal = bin_a_decimal(exponente) - 127

    mantisa_decimal = sum([int(bit) * (2**(-idx)) for idx, bit in enumerate(mantisa, start=1)])
    if exponente_decimal != - 127:
        mantisa_decimal += 1
    
    numero_final = (-1)**int(signo) * mantisa_decimal * (2**exponente_decimal)
    return numero_final

def suma_IEEE754(bin1, bin2):
    signo1, exponente1, mantisa1 = bin1[0], bin1[1:9], "1" + bin1[9:]
    signo2, exponente2, mantisa2 = bin2[0], bin2[1:9], "1" + bin2[9:]

    exponente1_decimal = bin_a_decimal(exponente1) - 127
    exponente2_decimal = bin_a_decimal(exponente2) - 127

    while exponente1_decimal < exponente2_decimal:
        mantisa1 = "0" + mantisa2[:-1]
        exponente2_decimal += 1
    
    while exponente2_decimal < exponente1_decimal:
        mantisa2 = "0" + mantisa2[:-1]
        exponente2_decimal += 1
    
    mantisa_resultado = ''
    carry = 0

    if (carry == 1):
        mantisa_resultado = mantisa_resultado[:1]
        exponente1_decimal += 1

    while (mantisa_resultado[0] != '1' and exponente1_decimal > 0):
        mantisa_resultado = mantisa_resultado[1:] + '0'
        exponente1_decimal -= 1

    exponente_resultado = decimal_a_bin(exponente1_decimal).zfill(8)

    return signo1 + exponente_resultado + mantisa_resultado[1:]
