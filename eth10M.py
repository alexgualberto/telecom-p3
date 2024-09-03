def decode(sig):
    estado_atual = 0
    quadro_ethernet = []
    ultimo_simbolo = None
    contador_de_bits = 0
    byte_atual = 0

    for simbolo in extrair_simbolos(sig):
        if estado_atual == 0:
            if ultimo_simbolo == 1 and simbolo == 1:
                estado_atual = 1
            ultimo_simbolo = simbolo
        elif estado_atual == 1:
            byte_atual |= (simbolo << contador_de_bits)
            contador_de_bits += 1
            
            if contador_de_bits == 8:
                quadro_ethernet.append(byte_atual)
                byte_atual = 0
                contador_de_bits = 0

    return bytes(quadro_ethernet)

def extrair_simbolos(amostras):
    contador_de_posicao = 1
    nivel_atual = amostras[0]

    for amostra in amostras[1:]:
        if amostra == nivel_atual:
            contador_de_posicao += 1
        else:
            if contador_de_posicao >= 20:
                # Canal ocioso detectado, encerra a transmissão
                break
            if contador_de_posicao >= 6:
                yield 1 - nivel_atual  # Inversão do símbolo
            contador_de_posicao = 1
            nivel_atual = amostra
