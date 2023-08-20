def decimal_to_binary(n):
    """Convert a decimal number to its binary representation as a string."""
    if n == 0:
        return "0"
    
    binary_rep = ""
    while n:
        binary_rep = str(n % 2) + binary_rep
        n //= 2
    
    return binary_rep

def binary_to_decimal(bin_str):
    """Convert a binary string to its decimal representation."""
    decimal_value = 0
    for i, bit in enumerate(reversed(bin_str)):
        decimal_value += int(bit) * (2 ** i)
    return decimal_value


def decimal_to_ieee754(n):
    if n == 0.0:
        return "0" * 32

    if n < 0:
        sign = "1"
        n = -n
    else:
        sign = "0"
    
    int_part = int(n)
    frac_part = n - int_part

    int_bin = decimal_to_binary(int_part)
    frac_bin = ""

    while frac_part > 0 and len(frac_bin) < 23:  # Agregar la condicin de longitud para evitar bucles infinitos
        frac_part *= 2
        bit = int(frac_part)
        frac_bin += str(bit)
        frac_part -= bit

    if int_part:
        mantissa = int_bin + frac_bin
        exponent = len(int_bin) - 1
        mantissa = mantissa[1:24]
    else:
        mantissa = frac_bin
        exponent = 0
        while mantissa[0] != "1":
            mantissa = mantissa[1:]
            exponent -= 1
        mantissa = mantissa[1:24]

    exponent += 127
    exponent_bin = decimal_to_binary(exponent).zfill(8)

    return sign + exponent_bin + mantissa.ljust(23, '0')



def ieee754_to_decimal(ieee):
    # Extract sign, exponent, and mantissa
    sign_bit = ieee[0]
    exponent = ieee[1:9]
    mantissa = ieee[9:]
    
    # Convertir exponente a decimal y restar el bias
    exponent_decimal = binary_to_decimal(exponent) - 127
    
    # Calcular el valor decimal de la mantisa
    mantissa_decimal = sum([int(bit) * (2**(-idx)) for idx, bit in enumerate(mantissa, start=1)])
    if exponent_decimal != -127:  # Excluyendo el caso de exponentes denormalizados
        mantissa_decimal += 1

    # Calcular el nmero final
    number = (-1)**int(sign_bit) * mantissa_decimal * (2**exponent_decimal)
    
    return number

def add_ieee754(bin1, bin2):
    # Extract sign, exponent, and mantissa
    sign1, exponent1, mantissa1 = bin1[0], bin1[1:9], "1" + bin1[9:]
    sign2, exponent2, mantissa2 = bin2[0], bin2[1:9], "1" + bin2[9:]

    # Convert exponents to decimal using our function
    exponent1_decimal = binary_to_decimal(exponent1) - 127
    exponent2_decimal = binary_to_decimal(exponent2) - 127

    # If exponents are different, shift mantissa of smaller exponent
    while exponent1_decimal < exponent2_decimal:
        mantissa1 = "0" + mantissa1[:-1]
        exponent1_decimal += 1

    while exponent2_decimal < exponent1_decimal:
        mantissa2 = "0" + mantissa2[:-1]
        exponent2_decimal += 1

    # Add mantissas with carry
    result_mantissa = ''
    carry = 0
    for i in range(23, -1, -1):  # Starting from the least significant bit
        sum_bits = int(mantissa1[i]) + int(mantissa2[i]) + carry
        if sum_bits == 2:
            carry = 1
            result_mantissa = "0" + result_mantissa
        elif sum_bits == 3:
            carry = 1
            result_mantissa = "1" + result_mantissa
        else:
            carry = 0
            result_mantissa = str(sum_bits) + result_mantissa

    # Handle carry overflow and normalize
    if carry == 1:
        result_mantissa = result_mantissa[:-1]  # Drop least significant bit
        exponent1_decimal += 1

    # Handle possible normalization if leading bit is 0
    while result_mantissa[0] != '1' and exponent1_decimal > 0:
        result_mantissa = result_mantissa[1:] + '0'
        exponent1_decimal -= 1

    exponent_result = decimal_to_binary(exponent1_decimal).zfill(8)

    # Return IEEE754 format
    return sign1 + exponent_result + result_mantissa[1:]

def main():
    with open("operaciones.txt", "r") as file:
        lines = file.readlines()

    same_sign_count = 0
    diff_sign_count = 0
    positive_results = 0
    negative_results = 0
    output_lines = []

    for line in lines:
        num1, num2 = [float(x) for x in line.strip().split(";")]

        bin1 = decimal_to_ieee754(num1)
        bin2 = decimal_to_ieee754(num2)

        if (num1 >= 0 and num2 >= 0) or (num1 < 0 and num2 < 0):  # same sign
            same_sign_count += 1
            sum_bin = add_ieee754(bin1, bin2)
            sum_check = ieee754_to_decimal(sum_bin)
            output_lines.append(f"{sum_check:.3f}/{sum_bin}")

            if sum_check >= 0:
                positive_results += 1
            else:
                negative_results += 1
        else:
            diff_sign_count += 1
            output_lines.append(f"{num1:.3f}/{bin1};{num2:.3f}/{bin2}")

    with open("resultados.txt", "w") as file:
        file.write("\n".join(output_lines))

    print(f"Lineas procesadas: {len(lines)}")
    print(f"Sumas realizadas: {same_sign_count}")
    print(f"Sumas no realizadas (signos opuestos): {diff_sign_count}")
    print(f"Resultados positivos: {positive_results}")
    print(f"Resultados negativos: {negative_results}")

if __name__ == "__main__":
    main()