import qrcode
import os

def calcular_crc16(payload):
    crc = 0xFFFF
    for char in payload:
        crc ^= ord(char) << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ 0x1021
            else:
                crc = crc << 1
            crc &= 0xFFFF
    return f"{crc:04X}"

def gerar_qrcode(valor_pix):
    print("\n[Sistema] Montando código PIX dinâmico...")

    nome = os.getenv("MEU_NOME")
    cidade = os.getenv("MINHA_CIDADE")
    chave = os.getenv("MINHA_CHAVE")

    tam_nome = f"{len(nome):02d}"
    tam_cidade = f"{len(cidade):02d}"
    tam_chave = f"{len(chave):02d}"

    str_valor = f"{valor_pix:.2f}"
    tamanho_valor = f"{len(str_valor):02d}"
    bloco_valor = f"54{tamanho_valor}{str_valor}"

    payload = (
        f"00020101021126360014br.gov.bcb.pix01{tam_chave}{chave}520400005303986"
        + bloco_valor
        + f"5802BR59{tam_nome}{nome}60{tam_cidade}{cidade}62070503***6304"
    )

    assinatura_crc16 = calcular_crc16(payload)
    texto_pix = payload + assinatura_crc16

    img_qr = qrcode.make(texto_pix)
    img_qr.save("qr_code_gerado.png")

    print("[Sistema] QR CODE dinâmico gerado com sucesso!")