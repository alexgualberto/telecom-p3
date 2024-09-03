def decode(sig):
    estado_atual = 0
    quadro_ethernet = list()
    ultimo_simbolo = 0
    contador_bits = 0
    byte_atual = 0

    for simbolo in extrair_simbolos(sig):
        if estado_atual == 0:
            if ultimo_simbolo == 1 and simbolo == 1:
                estado_atual = 1
            ultimo_simbolo = simbolo
        elif estado_atual == 1:
            byte_atual = byte_atual | (simbolo << contador_bits)
            
            if contador_bits == 7:
                quadro_ethernet.append(byte_atual)
                byte_atual = 0
            contador_bits = (contador_bits + 1) % 8
    return bytes(quadro_ethernet)

def extrair_simbolos(amostras):
    posicao = 1
    nivel_atual = amostras[0]

    for amostra in amostras[1:]:
        if amostra == nivel_atual:
            posicao += 1
        else:
            if posicao >= 20:
                # Canal ocioso detectado, encerra a transmissão
                break
            if posicao >= 6:
                yield 1 - nivel_atual  # Inversão do símbolo
            posicao = 1
            nivel_atual = amostra
