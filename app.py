from flask import Flask, request
from main import informeDadosCurto, informeDadosMedio, informeDadosLongo

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


@app.route('/calculoCurtoPrazo', methods=['POST'])
def calculoCurtoPrazo():
    body = request.get_json()

    dadosCurto = informeDadosCurto(body["quantas"], body["tempodeuso"], body["num_dias"])
    quantas = int(dadosCurto["quantas"])
    tempodeuso = int(dadosCurto["tempodeuso"])
    num_dias = int(dadosCurto["num_dias"])

    dia = 24 # Horas de 1 dia
    ano = 12 # Meses de 1 ano
    mes = 30 # dias de 1 mes
    anos = 1
    incandescentePotencia = 60
    fluorescentePotencia = 15
    ledPotencia = 7
    tarifa = 0.838020

    potencia_Incandescente = incandescentePotencia
    horas_consumo_Incandescente = quantas
    dias_consumo_Incandescente = num_dias
    tarifa_Incandescente = tarifa
    calculo_kwh_Incandescente = (potencia_Incandescente * horas_consumo_Incandescente * dias_consumo_Incandescente) / 1000
    valor_mes_Incandescente = tarifa_Incandescente * calculo_kwh_Incandescente
    valor_dia_Incandescente = valor_mes_Incandescente / 30
    valor_6h_Incandescente = valor_dia_Incandescente / 4

    potencia_Fluorescente = fluorescentePotencia
    horas_consumo_Fluorescente = quantas
    dias_consumo_Fluorescente = num_dias
    tarifa_Fluorescente = tarifa
    calculo_kwh_Fluorescente = (potencia_Fluorescente * horas_consumo_Fluorescente * dias_consumo_Fluorescente) / 1000
    valor_mes_Fluorescente = tarifa_Fluorescente * calculo_kwh_Fluorescente
    valor_dia_Fluorescente = valor_mes_Fluorescente / 30
    valor_6h_Fluorescente = valor_dia_Fluorescente / 4

    potencia_Led = ledPotencia
    horas_consumo_Led = quantas
    dias_consumo_Led = num_dias
    tarifa_Led = tarifa
    calculo_kwh_Led = (potencia_Led * horas_consumo_Led * dias_consumo_Led) / 1000
    valor_mes_Led = tarifa_Led * calculo_kwh_Led
    valor_dia_Led = valor_mes_Led / 30 
    valor_6h_Led = valor_dia_Led / 4


    icandescenteTempo = 1000 # Número de horas que dura em média essa lâmpada
    FluorescenteTempo = 8000 # Número de horas que dura em média essa lâmpada
    LedTempo = 50000 # Número de horas que dura em média essa lâmpada

    icandescentePreco = 2 # Preço médio da lâmpada
    FluorescentePreco = 11 # Preço médio da lâmpada
    LedPreco = 20 # Preço médio da lâmpada

    icandescenteConsumo6h = valor_6h_Incandescente # Valor cobrado em reais com um consumo em média de 6 Horas
    FluorescenteConsumo6h = valor_6h_Fluorescente # Valor cobrado em reais com um consumo em média de 6 Horas
    LedConsumo6h = valor_6h_Led # Valor cobrado em reais com um consumo em média de 6 Horas

    # Vida util da lâmpada x valor investido

    duracao_de_diasInc = (tempodeuso / dia) * (icandescenteTempo / ano)
    duracao_de_diasFlu = (tempodeuso / dia) * (FluorescenteTempo / ano)
    duracao_de_diasLed = (tempodeuso / dia) * (LedTempo / ano)

    duracao_de_diasIncF = int(f'''{duracao_de_diasInc:.0f}''')
    duracao_de_diasFluF = int(f'''{duracao_de_diasFlu:.0f}''')
    duracao_de_diasLedF = int(f'''{duracao_de_diasLed:.0f}''')

    # trocas por ano

    t_inc = ano * mes / duracao_de_diasInc
    t_flu = ano * mes / duracao_de_diasFlu
    t_led = ano * mes / duracao_de_diasLed
    
    t_incF = int(f'''{t_inc:.0f}''')
    t_fluF = int(f'''{t_flu:.0f}''')
    t_ledF = int(f'''{t_led:.0f}''')

    # valor gasto de acordo com a lampada que estiver usando

    gasto_em_lampadaINC = (t_inc * quantas) * icandescentePreco
    gasto_em_lampadaFLU = (t_flu * quantas) * FluorescentePreco
    gasto_em_lampadaLED = (t_led * quantas) * LedPreco

    gasto_em_lampadaINCF = float(f'''{gasto_em_lampadaINC:.2f}''')
    gasto_em_lampadaFLUF = float(f'''{gasto_em_lampadaFLU:.2f}''')
    gasto_em_lampadaLEDF = float(f'''{gasto_em_lampadaLED:.2f}''')

    # Economia no consumo
    # Lembrando que essa parte vai mostra apenas os consumos das lampadas, e as informações usada são baseadas no consumo de cada lampada a cada 6 horas

    taxa_consumo = tempodeuso / 6

    # Economia dia

    consumo_diaINC = icandescenteConsumo6h * taxa_consumo
    consumo_diaFLU = FluorescenteConsumo6h * taxa_consumo
    consumo_diaLED = LedConsumo6h * taxa_consumo

    consumo_diaINCF = float(f'''{consumo_diaINC:.2f}''')
    consumo_diaFLUF = float(f'''{consumo_diaFLU:.2f}''')
    consumo_diaLEDF = float(f'''{consumo_diaLED:.4f}''')

    # Economia mês

    consumo_mesINC = consumo_diaINC * mes
    consumo_mesFLU = consumo_diaFLU * mes
    consumo_mesLED = consumo_diaLED * mes

    consumo_mesINCF = float(f'''{consumo_mesINC:.2f}''')
    consumo_mesFLUF = float(f'''{consumo_mesFLU:.2f}''')
    consumo_mesLEDF = float(f'''{consumo_mesLED:.2f}''')

    # Economia ano

    consumo_anoINC = consumo_mesINC * ano
    consumo_anoFLU = consumo_mesFLU * ano
    consumo_anoLED = consumo_mesLED * ano

    consumo_anoINCF = float(f'''{consumo_anoINC:.2f}''')
    consumo_anoFLUF = float(f'''{consumo_anoFLU:.2f}''')
    consumo_anoLEDF = float(f'''{consumo_anoLED:.2f}''')

    saidaCurto = {'DuracaoLampadaIncadescenteDias': duracao_de_diasIncF,
            'DuracaoLampadaFluorescenteDias': duracao_de_diasFluF,
            'DuracaoLampadaLedDias': duracao_de_diasLedF,
            'VezesTrocaraLampadaIncadescente': t_incF,
            'VezesTrocaraLampadaFluorescente': t_fluF,
            'VezesTrocaraLampadaLed': t_ledF,
            'ValorGastoTrocaDeLampadasIncandescente': gasto_em_lampadaINCF,
            'ValorGastoTrocaDeLampadasFluorescente': gasto_em_lampadaFLUF,
            'ValorGastoTrocaDeLampadasLed': gasto_em_lampadaLEDF,
            'ConsumoDiaIncandescente': consumo_diaINCF,
            'ConsumoDiaFluorescente': consumo_diaFLUF,
            'ConsumoDiaLed': consumo_diaLEDF,
            'ConsumoMesIncandescente': consumo_mesINCF,
            'ConsumoMesFluorescente': consumo_mesFLUF,
            'ConsumoMesLed': consumo_mesLEDF,
            'ConsumoAnoIncandescente':consumo_anoINCF,
            'ConsumoAnoFluorescente': consumo_anoFLUF,
            'ConsumoAnoLed': consumo_anoLEDF}
    
    return saidaCurto
    
 
@app.route('/calculoMedioPrazo', methods=['POST'])
def calculoMedioPrazo():
    body = request.get_json()

    dadosMedio = informeDadosMedio(body["potencia"], body["tempodeuso"], body["n_dias"])
    potencia = int(dadosMedio["potencia"])
    tempodeuso = int(dadosMedio["tempodeuso"])
    n_dias = int(dadosMedio["n_dias"])

    def potencia_usuario():
        eletro = potencia
        return eletro

    def horas_dia():
        horas_dia = tempodeuso
        return horas_dia

    def num_dias():
        num_dias = n_dias
        return num_dias

    def tarifa_comp_eletrica():
        tarifa = 0.838020
        return tarifa

    # Aparelho de som
    valor_do_som = 1066.65
    potencia_som_escolhido = 15
    meses_ano = 12

    while True:
        valida1_1 = False
      
        potencia_som = potencia_usuario()
        horas_consumo_som = horas_dia()
        dias_consumo_som = num_dias()
        tarifa_som = tarifa_comp_eletrica()
        
        calculo_kwh_som = (potencia_som * horas_consumo_som * dias_consumo_som) / 1000
        valor_mes_som = tarifa_som * calculo_kwh_som
        valor_mes_somF = float(f'''{valor_mes_som:.2f}''')
        
        # comparação

        calculo_kwh_nosso_som = (potencia_som_escolhido * horas_consumo_som * dias_consumo_som) / 1000
        valor_mes_som_escolhido = tarifa_som * calculo_kwh_nosso_som
        valor_mes_som_escolhidoF = float(f'''{valor_mes_som_escolhido:.2f}''')

        diferenca_de_valor_som = valor_mes_som - valor_mes_som_escolhido
        tempo_de_retorno_som = valor_do_som / diferenca_de_valor_som
        tempo_em_anos_retorno_som = tempo_de_retorno_som / meses_ano
        tempo_em_anos_retorno_somF = int(f'''{tempo_em_anos_retorno_som:.0f}''')
        
        break

    # Umidificador
    valor_do_umidificador = 174.90
    potencia_umidificador_escolhido = 25
    meses_ano = 12

    while True:
      valida1_2 = False

      potencia_umidificador = potencia_usuario()
      horas_consumo_umidificador = horas_dia()
      dias_consumo_umidificador = num_dias()
      tarifa_umidificador = tarifa_comp_eletrica()
  
      calculo_kwh_umidificador = (potencia_umidificador * horas_consumo_umidificador * dias_consumo_umidificador) / 1000
      valor_mes_umidificador = tarifa_umidificador * calculo_kwh_umidificador
      valor_mes_umidificadorF = float(f'''{valor_mes_umidificador:.2f}''')
          
      # comparação

      calculo_kwh_nosso_umidificador = (potencia_umidificador_escolhido * horas_consumo_umidificador * dias_consumo_umidificador) / 1000
      valor_mes_umidificador_escolhido = tarifa_umidificador * calculo_kwh_nosso_umidificador
      valor_mes_umidificador_escolhidoF = float(f'''{valor_mes_umidificador_escolhido:.2f}''')
          
      diferenca_de_valor_umidificador = valor_mes_umidificador - valor_mes_umidificador_escolhido
      tempo_de_retorno_umidificador = valor_do_umidificador / diferenca_de_valor_umidificador
      tempo_em_anos_retorno_umidificador = tempo_de_retorno_umidificador / meses_ano
      tempo_em_anos_retorno_umidificadorF = int(f'''{tempo_em_anos_retorno_umidificador:.0f}''')
      
      break

    # Ar condicionado
    valor_do_ar = 1299
    potencia_ar_escolhido = 814
    meses_ano = 12

    while True:
        valida1_3 = False

        potencia_ar = potencia_usuario()
        horas_consumo_ar = horas_dia()
        dias_consumo_ar = num_dias()
        tarifa_ar = tarifa_comp_eletrica()

        calculo_kwh_ar = (potencia_ar * horas_consumo_ar * dias_consumo_ar) / 1000
        valor_mes_ar = tarifa_ar * calculo_kwh_ar
        valor_mes_arF = float(f'''{valor_mes_ar:.2f}''')
        
        # comparação

        calculo_kwh_nosso_ar = (potencia_ar_escolhido * horas_consumo_ar * dias_consumo_ar) / 1000
        valor_mes_ar_escolhido = tarifa_ar * calculo_kwh_nosso_ar
        valor_mes_ar_escolhidoF = float(f'''{valor_mes_ar_escolhido:.2f}''')

        diferenca_de_valor_ar = valor_mes_ar - valor_mes_ar_escolhido
        tempo_de_retorno_ar = valor_do_ar / diferenca_de_valor_ar
        tempo_em_anos_retorno_ar = tempo_de_retorno_ar / meses_ano
        tempo_em_anos_retorno_arF = int(f'''{tempo_em_anos_retorno_ar:.0f}''')

        break
    
    # DVD
    valor_do_DVD = 147.10
    potencia_DVD_escolhido = 10
    meses_ano = 12

    while True:
        valida1_4 = False
        potencia_DVD = potencia_usuario()
        horas_consumo_DVD = horas_dia()
        dias_consumo_DVD = num_dias()
        tarifa_DVD = tarifa_comp_eletrica()

        calculo_kwh_DVD = (potencia_DVD * horas_consumo_DVD * dias_consumo_DVD) / 1000
        valor_mes_DVD = tarifa_DVD * calculo_kwh_DVD
        valor_mes_DVDF = float(f'''{valor_mes_DVD:.2f}''')

        # comparação

        calculo_kwh_nosso_DVD = (potencia_DVD_escolhido * horas_consumo_DVD * dias_consumo_DVD) / 1000
        valor_mes_DVD_escolhido = tarifa_DVD * calculo_kwh_nosso_DVD
        valor_mes_DVD_escolhidoF = float(f'''{valor_mes_DVD_escolhido:.2f}''')

        diferenca_de_valor_DVD = valor_mes_DVD - valor_mes_DVD_escolhido
        tempo_de_retorno_DVD = valor_do_DVD / diferenca_de_valor_DVD
        tempo_em_anos_retorno_DVD = tempo_de_retorno_DVD / meses_ano
        tempo_em_anos_retorno_DVDF = int(f'''{tempo_em_anos_retorno_DVD:.0f}''')

        break

    valor_do_Home = 599
    potencia_Home_escolhido = 55
    meses_ano = 12

    # Home Theater
    while True:
        valida1_5 = False
        potencia_Home = potencia_usuario()
        horas_consumo_Home = horas_dia()
        dias_consumo_Home = num_dias()
        tarifa_Home = tarifa_comp_eletrica()

        calculo_kwh_Home = (potencia_Home * horas_consumo_Home * dias_consumo_Home) / 1000
        valor_mes_Home = tarifa_Home * calculo_kwh_Home
        valor_mes_HomeF = float(f'''{valor_mes_Home:.2f}''')

        # comparação

        calculo_kwh_nosso_Home = (potencia_Home_escolhido * horas_consumo_Home * dias_consumo_Home) / 1000
        valor_mes_Home_escolhido = tarifa_Home * calculo_kwh_nosso_Home
        valor_mes_Home_escolhidoF = float(f'''{valor_mes_Home_escolhido:.2f}''')

        diferenca_de_valor_Home = valor_mes_Home - valor_mes_Home_escolhido
        tempo_de_retorno_Home = valor_do_Home / diferenca_de_valor_Home
        tempo_em_anos_retorno_Home = tempo_de_retorno_Home / meses_ano
        tempo_em_anos_retorno_HomeF = int(f'''{tempo_em_anos_retorno_Home:.0f}''')

        break

    # Telefone fixo
    valor_do_Telefone = 120.59
    potencia_Telefone_escolhido = 1.1
    meses_ano = 12

    while True:
        valida1_6 = False
        potencia_Telefone = potencia_usuario()
        horas_consumo_Telefone = horas_dia()
        dias_consumo_Telefone = num_dias()
        tarifa_Telefone = tarifa_comp_eletrica()

        calculo_kwh_Telefone = (potencia_Telefone * horas_consumo_Telefone * dias_consumo_Telefone) / 1000
        valor_mes_Telefone = tarifa_Telefone * calculo_kwh_Telefone
        valor_mes_TelefoneF = float(f'''{valor_mes_Telefone:.2f}''')

        # comparação

        calculo_kwh_nosso_Telefone = (potencia_Telefone_escolhido * horas_consumo_Telefone * dias_consumo_Telefone) / 1000
        valor_mes_Telefone_escolhido = tarifa_Telefone * calculo_kwh_nosso_Telefone
        valor_mes_Telefone_escolhidoF = float(f'''{valor_mes_Telefone_escolhido:.2f}''')

        diferenca_de_valor_Telefone = valor_mes_Telefone - valor_mes_Telefone_escolhido
        tempo_de_retorno_Telefone = valor_do_Telefone / diferenca_de_valor_Telefone
        tempo_em_anos_retorno_Telefone = tempo_de_retorno_Telefone / meses_ano
        tempo_em_anos_retorno_TelefoneF = int(f'''{tempo_em_anos_retorno_Telefone:.0f}''')
        
        break

    # Televisão
    valor_do_Televisão = 2089.05
    potencia_Televisão_escolhido = 130
    meses_ano = 12

    while True:
        valida1_7 = False
        potencia_Televisão = potencia_usuario()
        horas_consumo_Televisão = horas_dia()
        dias_consumo_Televisão = num_dias()
        tarifa_Televisão = tarifa_comp_eletrica()

        calculo_kwh_Televisão = (potencia_Televisão * horas_consumo_Televisão * dias_consumo_Televisão) / 1000
        valor_mes_Televisão = tarifa_Televisão * calculo_kwh_Televisão
        valor_mes_TelevisãoF = float(f'''{valor_mes_Televisão:.2f}''')

        # comparação

        calculo_kwh_nosso_Televisão = (potencia_Televisão_escolhido * horas_consumo_Televisão * dias_consumo_Televisão) / 1000
        valor_mes_Televisão_escolhido = tarifa_Televisão * calculo_kwh_nosso_Televisão
        valor_mes_Televisão_escolhidoF = float(f'''{valor_mes_Televisão_escolhido:.2f}''')

        diferenca_de_valor_Televisão = valor_mes_Televisão - valor_mes_Televisão_escolhido
        tempo_de_retorno_Televisão = valor_do_Televisão / diferenca_de_valor_Televisão
        tempo_em_anos_retorno_Televisão = tempo_de_retorno_Televisão / meses_ano
        tempo_em_anos_retorno_TelevisãoF = int(f'''{tempo_em_anos_retorno_Televisão:.0f}''')
        
        break

    valor_do_Ventilador = 149.99
    potencia_Ventilador_escolhido = 50
    meses_ano = 12

    # Ventilador
    while True:
        valida1_8 = False
        potencia_Ventilador = potencia_usuario()
        horas_consumo_Ventilador = horas_dia()
        dias_consumo_Ventilador = num_dias()
        tarifa_Ventilador = tarifa_comp_eletrica()

        calculo_kwh_Ventilador = (potencia_Ventilador * horas_consumo_Ventilador * dias_consumo_Ventilador) / 1000
        valor_mes_Ventilador = tarifa_Ventilador * calculo_kwh_Ventilador
        valor_mes_VentiladorF = float(f'''{valor_mes_Ventilador:.2f}''')

        # comparação

        calculo_kwh_nosso_Ventilador = (potencia_Ventilador_escolhido * horas_consumo_Ventilador * dias_consumo_Ventilador) / 1000
        valor_mes_Ventilador_escolhido = tarifa_Ventilador * calculo_kwh_nosso_Ventilador
        valor_mes_Ventilador_escolhidoF = float(f'''{valor_mes_Ventilador_escolhido:.2f}''')
        
        diferenca_de_valor_Ventilador = valor_mes_Ventilador - valor_mes_Ventilador_escolhido
        tempo_de_retorno_Ventilador = valor_do_Ventilador / diferenca_de_valor_Ventilador
        tempo_em_anos_retorno_Ventilador = tempo_de_retorno_Ventilador / meses_ano
        tempo_em_anos_retorno_VentiladorF = int(f'''{tempo_em_anos_retorno_Ventilador:.0f}''')
        
        break

    # Video Game
    valor_do_Video = 2687.97
    potencia_Video_escolhido = 165
    meses_ano = 12

    while True:
        valida1_9 = False
        potencia_Video = potencia_usuario()
        horas_consumo_Video = horas_dia()
        dias_consumo_Video = num_dias()
        tarifa_Video = tarifa_comp_eletrica()

        calculo_kwh_Video = (potencia_Video * horas_consumo_Video * dias_consumo_Video) / 1000
        valor_mes_Video = tarifa_Video * calculo_kwh_Video
        valor_mes_VideoF = float(f'''{valor_mes_Video:.2f}''')

        # comparação

        calculo_kwh_nosso_Video = (potencia_Video_escolhido * horas_consumo_Video * dias_consumo_Video) / 1000
        valor_mes_Video_escolhido = tarifa_Video * calculo_kwh_nosso_Video
        valor_mes_Video_escolhidoF = float(f'''{valor_mes_Video_escolhido:.2f}''')

        diferenca_de_valor_Video = valor_mes_Video - valor_mes_Video_escolhido
        tempo_de_retorno_Video = valor_do_Video / diferenca_de_valor_Video
        tempo_em_anos_retorno_Video = tempo_de_retorno_Video / meses_ano
        tempo_em_anos_retorno_VideoF = int(f'''{tempo_em_anos_retorno_Video:.0f}''')
        
        break

    # Abajur
    valor_do_Abajur = 50.60 
    potencia_Abajur_escolhido = 30 
    meses_ano = 12

    while True:
        valida2_1 = False
        potencia_Abajur = potencia_usuario()
        horas_consumo_Abajur = horas_dia()
        dias_consumo_Abajur = num_dias()
        tarifa_Abajur = tarifa_comp_eletrica()

        calculo_kwh_Abajur = (potencia_Abajur * horas_consumo_Abajur * dias_consumo_Abajur) / 1000
        valor_mes_Abajur = tarifa_Abajur * calculo_kwh_Abajur
        valor_mes_AbajurF = float(f'''{valor_mes_Abajur:.2f}''')

        # comparação

        calculo_kwh_nosso_Abajur = (potencia_Abajur_escolhido * horas_consumo_Abajur * dias_consumo_Abajur) / 1000
        valor_mes_Abajur_escolhido = tarifa_Abajur * calculo_kwh_nosso_Abajur
        valor_mes_Abajur_escolhidoF = float(f'''{valor_mes_Abajur_escolhido:.2f}''')

        diferenca_de_valor_Abajur = valor_mes_Abajur - valor_mes_Abajur_escolhido
        tempo_de_retorno_Abajur = valor_do_Abajur / diferenca_de_valor_Abajur
        tempo_em_anos_retorno_Abajur = tempo_de_retorno_Abajur / meses_ano
        tempo_em_anos_retorno_AbajurF = int(f'''{tempo_em_anos_retorno_Abajur:.0f}''')

        break

    # Aquecedor
    valor_do_Aquecedor = 144.67 
    potencia_Aquecedor_escolhido = 800
    meses_ano = 12

    while True:
        valida2_2 = False
        potencia_Aquecedor = potencia_usuario()
        horas_consumo_Aquecedor = horas_dia()
        dias_consumo_Aquecedor = num_dias()
        tarifa_Aquecedor = tarifa_comp_eletrica()

        calculo_kwh_Aquecedor = (potencia_Aquecedor * horas_consumo_Aquecedor * dias_consumo_Aquecedor) / 1000
        valor_mes_Aquecedor = tarifa_Aquecedor * calculo_kwh_Aquecedor
        valor_mes_AquecedorF = float(f'''{valor_mes_Aquecedor:.2f}''')

        # comparação

        calculo_kwh_nosso_Aquecedor = (potencia_Aquecedor_escolhido * horas_consumo_Aquecedor * dias_consumo_Aquecedor) / 1000
        valor_mes_Aquecedor_escolhido = tarifa_Aquecedor * calculo_kwh_nosso_Aquecedor
        valor_mes_Aquecedor_escolhidoF = float(f'''{valor_mes_Aquecedor_escolhido:.2f}''')

        diferenca_de_valor_Aquecedor = valor_mes_Aquecedor - valor_mes_Aquecedor_escolhido
        tempo_de_retorno_Aquecedor = valor_do_Aquecedor / diferenca_de_valor_Aquecedor
        tempo_em_anos_retorno_Aquecedor = tempo_de_retorno_Aquecedor / meses_ano
        tempo_em_anos_retorno_AquecedorF = int(f'''{tempo_em_anos_retorno_Aquecedor:.0f}''')
        
        break

    # Nebulizador
    valor_do_Nebulizador = 187.63
    potencia_Nebulizador_escolhido = 70
    meses_ano = 12

    while True:
        valida2_3 = False
        potencia_Nebulizador = potencia_usuario()
        horas_consumo_Nebulizador = horas_dia()
        dias_consumo_Nebulizador = num_dias()
        tarifa_Nebulizador = tarifa_comp_eletrica()

        calculo_kwh_Nebulizador = (potencia_Nebulizador * horas_consumo_Nebulizador * dias_consumo_Nebulizador) / 1000
        valor_mes_Nebulizador = tarifa_Nebulizador * calculo_kwh_Nebulizador
        valor_mes_NebulizadorF = float(f'''{valor_mes_Aquecedor_escolhido:.2f}''')

        # comparação

        calculo_kwh_nosso_Nebulizador = (potencia_Nebulizador_escolhido * horas_consumo_Nebulizador * dias_consumo_Nebulizador) / 1000
        valor_mes_Nebulizador_escolhido = tarifa_Nebulizador * calculo_kwh_nosso_Nebulizador
        valor_mes_Nebulizador_escolhidoF = float(f'''{valor_mes_Aquecedor_escolhido:.2f}''')

        diferenca_de_valor_Nebulizador = valor_mes_Nebulizador - valor_mes_Nebulizador_escolhido
        tempo_de_retorno_Nebulizador = valor_do_Nebulizador / diferenca_de_valor_Nebulizador
        tempo_em_anos_retorno_Nebulizador = tempo_de_retorno_Nebulizador / meses_ano
        tempo_em_anos_retorno_NebulizadorF = int(f'''{tempo_em_anos_retorno_Aquecedor:.0f}''')

        break

    # Radio
    valor_do_Radio = 99.90
    potencia_Radio_escolhido = 6
    meses_ano = 12

    while True:
        valida2_4 = False
        potencia_Radio = potencia_usuario()
        horas_consumo_Radio = horas_dia()
        dias_consumo_Radio = num_dias()
        tarifa_Radio = tarifa_comp_eletrica()

        calculo_kwh_Radio = (potencia_Radio * horas_consumo_Radio * dias_consumo_Radio) / 1000
        valor_mes_Radio = tarifa_Radio * calculo_kwh_Radio
        valor_mes_RadioF = float(f'''{valor_mes_Radio:.2f}''')

        # comparação

        calculo_kwh_nosso_Radio = (potencia_Radio_escolhido * horas_consumo_Radio * dias_consumo_Radio) / 1000
        valor_mes_Radio_escolhido = tarifa_Radio * calculo_kwh_nosso_Radio
        valor_mes_Radio_escolhidoF = float(f'''{valor_mes_Radio_escolhido:.2f}''')

        diferenca_de_valor_Radio = valor_mes_Radio - valor_mes_Radio_escolhido
        tempo_de_retorno_Radio = valor_do_Radio / diferenca_de_valor_Radio
        tempo_em_anos_retorno_Radio = tempo_de_retorno_Radio / meses_ano
        tempo_em_anos_retorno_RadioF = int(f'''{tempo_em_anos_retorno_Radio:.0f}''')
        
        break

    # Apirador de pó
    valor_do_Apirador = 999
    potencia_Apirador_escolhido = 115
    meses_ano = 12

    while True:
        valida3_1 = False
        potencia_Apirador = potencia_usuario()
        horas_consumo_Apirador = horas_dia()
        dias_consumo_Apirador = num_dias()
        tarifa_Apirador = tarifa_comp_eletrica()

        calculo_kwh_Apirador = (potencia_Apirador * horas_consumo_Apirador * dias_consumo_Apirador) / 1000
        valor_mes_Apirador = tarifa_Apirador * calculo_kwh_Apirador
        valor_mes_ApiradorF = float(f'''{valor_mes_Apirador:.2f}''')

        # comparação

        calculo_kwh_nosso_Apirador = (potencia_Apirador_escolhido * horas_consumo_Apirador * dias_consumo_Apirador) / 1000
        valor_mes_Apirador_escolhido = tarifa_Apirador * calculo_kwh_nosso_Apirador
        valor_mes_Apirador_escolhidoF = float(f'''{valor_mes_Apirador_escolhido:.2f}''')
        
        diferenca_de_valor_Apirador = valor_mes_Apirador - valor_mes_Apirador_escolhido
        tempo_de_retorno_Apirador = valor_do_Apirador / diferenca_de_valor_Apirador
        tempo_em_anos_retorno_Apirador = tempo_de_retorno_Apirador / meses_ano
        tempo_em_anos_retorno_ApiradorF = int(f'''{tempo_em_anos_retorno_Apirador:.0f}''')
        
        break

    # Desumidificador
    valor_do_Desumidificador = 339.90
    potencia_Desumidificador_escolhido = 22.5
    meses_ano = 12

    while True:
        valida3_2 = False
        potencia_Desumidificador = potencia_usuario()
        horas_consumo_Desumidificador = horas_dia()
        dias_consumo_Desumidificador = num_dias()
        tarifa_Desumidificador = tarifa_comp_eletrica()

        calculo_kwh_Desumidificador = (potencia_Desumidificador * horas_consumo_Desumidificador * dias_consumo_Desumidificador) / 1000
        valor_mes_Desumidificador = tarifa_Desumidificador * calculo_kwh_Desumidificador
        valor_mes_DesumidificadorF = float(f'''{valor_mes_Desumidificador:.2f}''')

        # comparação

        calculo_kwh_nosso_Desumidificador = (potencia_Desumidificador_escolhido * horas_consumo_Desumidificador * dias_consumo_Desumidificador) / 1000
        valor_mes_Desumidificador_escolhido = tarifa_Desumidificador * calculo_kwh_nosso_Desumidificador
        valor_mes_Desumidificador_escolhidoF = float(f'''{valor_mes_Desumidificador_escolhido:.2f}''')
        
        diferenca_de_valor_Desumidificador = valor_mes_Desumidificador - valor_mes_Desumidificador_escolhido
        tempo_de_retorno_Desumidificador = valor_do_Desumidificador / diferenca_de_valor_Desumidificador
        tempo_em_anos_retorno_Desumidificador = tempo_de_retorno_Desumidificador / meses_ano
        tempo_em_anos_retorno_DesumidificadorF = int(f'''{tempo_em_anos_retorno_Desumidificador:.0f}''')
        
        break

    # Ferro de passar
    valor_do_Ferro = 61.83
    potencia_Ferro_escolhido = 1000
    meses_ano = 12

    while True:
        valida3_3 = False
        potencia_Ferro = potencia_usuario()
        horas_consumo_Ferro = horas_dia()
        dias_consumo_Ferro = num_dias()
        tarifa_Ferro = tarifa_comp_eletrica()

        calculo_kwh_Ferro = (potencia_Ferro * horas_consumo_Ferro * dias_consumo_Ferro) / 1000
        valor_mes_Ferro = tarifa_Ferro * calculo_kwh_Ferro
        valor_mes_FerroF = float(f'''{valor_mes_Ferro:.2f}''')

        # comparação

        calculo_kwh_nosso_Ferro = (potencia_Ferro_escolhido * horas_consumo_Ferro * dias_consumo_Ferro) / 1000
        valor_mes_Ferro_escolhido = tarifa_Ferro * calculo_kwh_nosso_Ferro
        valor_mes_Ferro_escolhidoF = float(f'''{valor_mes_Ferro_escolhido:.2f}''')

        diferenca_de_valor_Ferro = valor_mes_Ferro - valor_mes_Ferro_escolhido
        tempo_de_retorno_Ferro = valor_do_Ferro / diferenca_de_valor_Ferro
        tempo_em_anos_retorno_Ferro = tempo_de_retorno_Ferro / meses_ano
        tempo_em_anos_retorno_FerroF = int(f'''{tempo_em_anos_retorno_Ferro:.0f}''')
        
        break
    
    # Maquina de lavar
    valor_do_Maquina = 1829
    potencia_Maquina_escolhido = 450
    meses_ano = 12

    while True:
        valida3_4 = False
        potencia_Maquina = potencia_usuario()
        horas_consumo_Maquina = horas_dia()
        dias_consumo_Maquina = num_dias()
        tarifa_Maquina = tarifa_comp_eletrica()

        calculo_kwh_Maquina = (potencia_Maquina * horas_consumo_Maquina * dias_consumo_Maquina) / 1000
        valor_mes_Maquina = tarifa_Maquina * calculo_kwh_Maquina
        valor_mes_MaquinaF = float(f'''{valor_mes_Maquina:.2f}''')

        # comparação

        calculo_kwh_nosso_Maquina = (potencia_Maquina_escolhido * horas_consumo_Maquina * dias_consumo_Maquina) / 1000
        valor_mes_Maquina_escolhido = tarifa_Maquina * calculo_kwh_nosso_Maquina
        valor_mes_Maquina_escolhidoF = float(f'''{valor_mes_Maquina_escolhido:.2f}''')
        
        diferenca_de_valor_Maquina = valor_mes_Maquina - valor_mes_Maquina_escolhido
        tempo_de_retorno_Maquina = valor_do_Maquina / diferenca_de_valor_Maquina
        tempo_em_anos_retorno_Maquina = tempo_de_retorno_Maquina / meses_ano
        tempo_em_anos_retorno_MaquinaF = int(f'''{tempo_em_anos_retorno_Maquina:.0f}''')
        
        break

    # Maquina de secar
    valor_do_secar = 838.90
    potencia_secar_escolhido = 1350
    meses_ano = 12

    while True:
        valida3_5 = False
        potencia_secar = potencia_usuario()
        horas_consumo_secar = horas_dia()
        dias_consumo_secar = num_dias()
        tarifa_secar = tarifa_comp_eletrica()

        calculo_kwh_secar = (potencia_secar * horas_consumo_secar * dias_consumo_secar) / 1000
        valor_mes_secar = tarifa_secar * calculo_kwh_secar
        valor_mes_secarF = float(f'''{valor_mes_secar:.2f}''')

        # comparação

        calculo_kwh_nosso_secar = (potencia_secar_escolhido * horas_consumo_secar * dias_consumo_secar) / 1000
        valor_mes_secar_escolhido = tarifa_secar * calculo_kwh_nosso_secar
        valor_mes_secar_escolhidoF = float(f'''{valor_mes_secar_escolhido:.2f}''')
        
        diferenca_de_valor_secar = valor_mes_secar - valor_mes_secar_escolhido
        tempo_de_retorno_secar = valor_do_secar / diferenca_de_valor_secar
        tempo_em_anos_retorno_secar = tempo_de_retorno_secar / meses_ano
        tempo_em_anos_retorno_secarF = int(f'''{tempo_em_anos_retorno_secar:.0f}''')
        
        break

    # Maquina de costura
    valor_do_costura = 718
    potencia_costura_escolhido = 70
    meses_ano = 12

    while True:
        valida3_6 = False
        potencia_costura = potencia_usuario()
        horas_consumo_costura = horas_dia()
        dias_consumo_costura = num_dias()
        tarifa_costura = tarifa_comp_eletrica()
  
        calculo_kwh_costura = (potencia_costura * horas_consumo_costura * dias_consumo_costura) / 1000
        valor_mes_costura = tarifa_costura * calculo_kwh_costura
        valor_mes_costuraF = float(f'''{valor_mes_costura:.2f}''')

        # comparação

        calculo_kwh_nosso_costura = (potencia_costura_escolhido * horas_consumo_costura * dias_consumo_costura) / 1000
        valor_mes_costura_escolhido = tarifa_costura * calculo_kwh_nosso_costura
        valor_mes_costura_escolhidoF = float(f'''{valor_mes_costura_escolhido:.2f}''')
        
        diferenca_de_valor_costura = valor_mes_costura - valor_mes_costura_escolhido
        tempo_de_retorno_costura = valor_do_costura / diferenca_de_valor_costura
        tempo_em_anos_retorno_costura = tempo_de_retorno_costura / meses_ano
        tempo_em_anos_retorno_costuraF = int(f'''{tempo_em_anos_retorno_costura:.0f}''')
        
        break

    # Alarme
    valor_do_Alarme = 2687.97 
    potencia_Alarme_escolhido = 165 
    meses_ano = 12

    while True:
        valida4_1 = False
        potencia_Alarme = potencia_usuario()
        horas_consumo_Alarme = horas_dia()
        dias_consumo_Alarme = num_dias()
        tarifa_Alarme = tarifa_comp_eletrica()

        calculo_kwh_Alarme = (potencia_Alarme * horas_consumo_Alarme * dias_consumo_Alarme) / 1000
        valor_mes_Alarme = tarifa_Alarme * calculo_kwh_Alarme
        valor_mes_AlarmeF = float(f'''{valor_mes_Alarme:.2f}''')

        # comparação

        calculo_kwh_nosso_Alarme = (potencia_Alarme_escolhido * horas_consumo_Alarme * dias_consumo_Alarme) / 1000
        valor_mes_Alarme_escolhido = tarifa_Alarme * calculo_kwh_nosso_Alarme
        valor_mes_Alarme_escolhidoF = float(f'''{valor_mes_Alarme_escolhido:.2f}''')

        diferenca_de_valor_Alarme = valor_mes_Alarme - valor_mes_Alarme_escolhido
        tempo_de_retorno_Alarme = valor_do_Alarme / diferenca_de_valor_Alarme
        tempo_em_anos_retorno_Alarme = tempo_de_retorno_Alarme / meses_ano
        tempo_em_anos_retorno_AlarmeF = int(f'''{tempo_em_anos_retorno_Alarme:.0f}''')

        break

    # Portão elétrico
    valor_do_Portao = 466.40
    potencia_Portao_escolhido = 420
    meses_ano = 12

    while True:
        valida4_2 = False
        potencia_Portao = potencia_usuario()
        horas_consumo_Portao = horas_dia()
        dias_consumo_Portao = num_dias()
        tarifa_Portao = tarifa_comp_eletrica()

        calculo_kwh_Portao = (potencia_Portao * horas_consumo_Portao * dias_consumo_Portao) / 1000
        valor_mes_Portao = tarifa_Portao * calculo_kwh_Portao
        valor_mes_PortaoF = float(f'''{valor_mes_Portao:.2f}''')

        # comparação

        calculo_kwh_nosso_Portao = (potencia_Portao_escolhido * horas_consumo_Portao * dias_consumo_Portao) / 1000
        valor_mes_Portao_escolhido = tarifa_Portao * calculo_kwh_nosso_Portao
        valor_mes_Portao_escolhidoF = float(f'''{valor_mes_Portao_escolhido:.2f}''')

        diferenca_de_valor_Portao = valor_mes_Portao - valor_mes_Portao_escolhido
        tempo_de_retorno_Portao = valor_do_Portao / diferenca_de_valor_Portao
        tempo_em_anos_retorno_Portao = tempo_de_retorno_Portao / meses_ano
        tempo_em_anos_retorno_PortaoF = int(f'''{tempo_em_anos_retorno_Portao:.0f}''')
        
        break

    # Sensor de presença
    valor_do_Sensor = 466.40
    potencia_Sensor_escolhido = 48
    meses_ano = 12

    while True:
        valida4_3 = False
        potencia_Sensor = potencia_usuario()
        horas_consumo_Sensor = horas_dia()
        dias_consumo_Sensor = num_dias()
        tarifa_Sensor = tarifa_comp_eletrica()

        calculo_kwh_Sensor = (potencia_Sensor * horas_consumo_Sensor * dias_consumo_Sensor) / 1000
        valor_mes_Sensor = tarifa_Sensor * calculo_kwh_Sensor
        valor_mes_SensorF = float(f'''{valor_mes_Sensor:.2f}''')

        # comparação

        calculo_kwh_nosso_Sensor = (potencia_Sensor_escolhido * horas_consumo_Sensor * dias_consumo_Sensor) / 1000
        valor_mes_Sensor_escolhido = tarifa_Sensor * calculo_kwh_nosso_Sensor
        valor_mes_Sensor_escolhidoF = float(f'''{valor_mes_Sensor_escolhido:.2f}''')
        
        diferenca_de_valor_Sensor = valor_mes_Sensor - valor_mes_Sensor_escolhido
        tempo_de_retorno_Sensor = valor_do_Sensor / diferenca_de_valor_Sensor
        tempo_em_anos_retorno_Sensor = tempo_de_retorno_Sensor / meses_ano
        tempo_em_anos_retorno_SensorF = int(f'''{tempo_em_anos_retorno_Sensor:.0f}''')

        break

    # Computador
    valor_do_Computador = 859.99
    potencia_Computador_escolhido = 350
    meses_ano = 12

    while True:
        valida5_1 = False
        potencia_Computador = potencia_usuario()
        horas_consumo_Computador = horas_dia()
        dias_consumo_Computador = num_dias()
        tarifa_Computador = tarifa_comp_eletrica()

        calculo_kwh_Computador = (potencia_Computador * horas_consumo_Computador * dias_consumo_Computador) / 1000
        valor_mes_Computador = tarifa_Computador * calculo_kwh_Computador
        valor_mes_ComputadorF = float(f'''{valor_mes_Computador:.2f}''')

        # comparação

        calculo_kwh_nosso_Computador = (potencia_Computador_escolhido * horas_consumo_Computador * dias_consumo_Computador) / 1000
        valor_mes_Computador_escolhido = tarifa_Computador * calculo_kwh_nosso_Computador
        valor_mes_Computador_escolhidoF = float(f'''{valor_mes_Computador_escolhido:.2f}''')

        diferenca_de_valor_Computador = valor_mes_Computador - valor_mes_Computador_escolhido
        tempo_de_retorno_Computador = valor_do_Computador / diferenca_de_valor_Computador
        tempo_em_anos_retorno_Computador = tempo_de_retorno_Computador / meses_ano
        tempo_em_anos_retorno_ComputadorF = int(f'''{tempo_em_anos_retorno_Computador:.0f}''')
        
        break

    # Impressora
    valor_do_Impressora = 1099.99
    potencia_Impressora_escolhido = 12
    meses_ano = 12

    while True:
        valida5_2 = False
        potencia_Impressora = potencia_usuario()
        horas_consumo_Impressora = horas_dia()
        dias_consumo_Impressora = num_dias()
        tarifa_Impressora = tarifa_comp_eletrica()

        calculo_kwh_Impressora = (potencia_Impressora * horas_consumo_Impressora * dias_consumo_Impressora) / 1000
        valor_mes_Impressora = tarifa_Impressora * calculo_kwh_Impressora
        valor_mes_ImpressoraF = float(f'''{valor_mes_Impressora:.2f}''')

        # comparação

        calculo_kwh_nosso_Impressora = (potencia_Impressora_escolhido * horas_consumo_Impressora * dias_consumo_Impressora) / 1000
        valor_mes_Impressora_escolhido = tarifa_Impressora * calculo_kwh_nosso_Impressora
        valor_mes_Impressora_escolhidoF = float(f'''{valor_mes_Impressora_escolhido:.2f}''')

        diferenca_de_valor_Impressora = valor_mes_Impressora - valor_mes_Impressora_escolhido
        tempo_de_retorno_Impressora = valor_do_Impressora / diferenca_de_valor_Impressora
        tempo_em_anos_retorno_Impressora = tempo_de_retorno_Impressora / meses_ano
        tempo_em_anos_retorno_ImpressoraF = int(f'''{tempo_em_anos_retorno_Impressora:.0f}''')
        
        break

    # Moldem
    valor_do_Moldem = 218.58
    potencia_Moldem_escolhido = 12
    meses_ano = 12

    while True:
        valida5_3 = False
        potencia_Moldem = potencia_usuario()
        horas_consumo_Moldem = horas_dia()
        dias_consumo_Moldem = num_dias()
        tarifa_Moldem = tarifa_comp_eletrica()

        calculo_kwh_Moldem = (potencia_Moldem * horas_consumo_Moldem * dias_consumo_Moldem) / 1000
        valor_mes_Moldem = tarifa_Moldem * calculo_kwh_Moldem
        valor_mes_MoldemF = float(f'''{valor_mes_Moldem:.2f}''')

        # comparação

        calculo_kwh_nosso_Moldem = (potencia_Moldem_escolhido * horas_consumo_Moldem * dias_consumo_Moldem) / 1000
        valor_mes_Moldem_escolhido = tarifa_Moldem * calculo_kwh_nosso_Moldem
        valor_mes_Moldem_escolhidoF = float(f'''{valor_mes_Moldem_escolhido:.2f}''')

        diferenca_de_valor_Moldem = valor_mes_Moldem - valor_mes_Moldem_escolhido
        tempo_de_retorno_Moldem = valor_do_Moldem / diferenca_de_valor_Moldem
        tempo_em_anos_retorno_Moldem = tempo_de_retorno_Moldem / meses_ano
        tempo_em_anos_retorno_MoldemF = int(f'''{tempo_em_anos_retorno_Moldem:.0f}''')

        break	

    # Monitor
    valor_do_Monitor = 1559
    potencia_Monitor_escolhido = 24
    meses_ano = 12

    while True:
        valida5_4 = False
        potencia_Monitor = potencia_usuario()
        horas_consumo_Monitor = horas_dia()
        dias_consumo_Monitor = num_dias()
        tarifa_Monitor = tarifa_comp_eletrica()

        calculo_kwh_Monitor = (potencia_Monitor * horas_consumo_Monitor * dias_consumo_Monitor) / 1000
        valor_mes_Monitor = tarifa_Monitor * calculo_kwh_Monitor
        valor_mes_MonitorF = float(f'''{valor_mes_Monitor:.2f}''')

        # comparação

        calculo_kwh_nosso_Monitor = (potencia_Monitor_escolhido * horas_consumo_Monitor * dias_consumo_Monitor) / 1000
        valor_mes_Monitor_escolhido = tarifa_Monitor * calculo_kwh_nosso_Monitor
        valor_mes_Monitor_escolhidoF = float(f'''{valor_mes_Monitor_escolhido:.2f}''')

        diferenca_de_valor_Monitor = valor_mes_Monitor - valor_mes_Monitor_escolhido
        tempo_de_retorno_Monitor = valor_do_Monitor / diferenca_de_valor_Monitor
        tempo_em_anos_retorno_Monitor = tempo_de_retorno_Monitor / meses_ano
        tempo_em_anos_retorno_MonitorF = int(f'''{tempo_em_anos_retorno_Monitor:.0f}''')

        break

    # Multifuncional
    valor_do_Multifuncional = 971.10
    potencia_Multifuncional_escolhido = 14
    meses_ano = 12

    while True:
        valida5_5 = False
        potencia_Multifuncional = potencia_usuario()
        horas_consumo_Multifuncional = horas_dia()
        dias_consumo_Multifuncional = num_dias()
        tarifa_Multifuncional = tarifa_comp_eletrica()

        calculo_kwh_Multifuncional = (potencia_Multifuncional * horas_consumo_Multifuncional * dias_consumo_Multifuncional) / 1000
        valor_mes_Multifuncional = tarifa_Multifuncional * calculo_kwh_Multifuncional
        valor_mes_MultifuncionalF = float(f'''{valor_mes_Multifuncional:.2f}''')

        # comparação

        calculo_kwh_nosso_Multifuncional = (potencia_Multifuncional_escolhido * horas_consumo_Multifuncional * dias_consumo_Multifuncional) / 1000
        valor_mes_Multifuncional_escolhido = tarifa_Multifuncional * calculo_kwh_nosso_Multifuncional
        valor_mes_Multifuncional_escolhidoF = float(f'''{valor_mes_Multifuncional_escolhido:.2f}''')
        
        diferenca_de_valor_Multifuncional = valor_mes_Multifuncional - valor_mes_Multifuncional_escolhido
        tempo_de_retorno_Multifuncional = valor_do_Multifuncional / diferenca_de_valor_Multifuncional
        tempo_em_anos_retorno_Multifuncional = tempo_de_retorno_Multifuncional / meses_ano
        tempo_em_anos_retorno_MultifuncionalF = int(f'''{tempo_em_anos_retorno_Multifuncional:.0f}''')
        
        break

    # Notebook
    valor_do_Notebook = 5290.82
    potencia_Notebook_escolhido = 65
    meses_ano = 12

    while True:
        valida5_6 = False
        potencia_Notebook = potencia_usuario()
        horas_consumo_Notebook = horas_dia()
        dias_consumo_Notebook = num_dias()
        tarifa_Notebook = tarifa_comp_eletrica()

        calculo_kwh_Notebook = (potencia_Notebook * horas_consumo_Notebook * dias_consumo_Notebook) / 1000
        valor_mes_Notebook = tarifa_Notebook * calculo_kwh_Notebook
        valor_mes_NotebookF = float(f'''{valor_mes_Notebook:.2f}''')

        # comparação

        calculo_kwh_nosso_Notebook = (potencia_Notebook_escolhido * horas_consumo_Notebook * dias_consumo_Notebook) / 1000
        valor_mes_Notebook_escolhido = tarifa_Notebook * calculo_kwh_nosso_Notebook
        valor_mes_Notebook_escolhidoF = float(f'''{valor_mes_Notebook_escolhido:.2f}''')

        diferenca_de_valor_Notebook = valor_mes_Notebook - valor_mes_Notebook_escolhido
        tempo_de_retorno_Notebook = valor_do_Notebook / diferenca_de_valor_Notebook
        tempo_em_anos_retorno_Notebook = tempo_de_retorno_Notebook / meses_ano
        tempo_em_anos_retorno_NotebookF = int(f'''{tempo_em_anos_retorno_Notebook:.0f}''')
        
        break

    # Scaner
    valor_do_Scaner = 999
    potencia_Scaner_escolhido = 2.5
    meses_ano = 12

    while True:
        valida5_7 = False
        potencia_Scaner = potencia_usuario()
        horas_consumo_Scaner = horas_dia()
        dias_consumo_Scaner = num_dias()
        tarifa_Scaner = tarifa_comp_eletrica()

        calculo_kwh_Scaner = (potencia_Scaner * horas_consumo_Scaner * dias_consumo_Scaner) / 1000
        valor_mes_Scaner = tarifa_Scaner * calculo_kwh_Scaner
        valor_mes_ScanerF = float(f'''{valor_mes_Scaner:.2f}''')

        # comparação

        calculo_kwh_nosso_Scaner = (potencia_Scaner_escolhido * horas_consumo_Scaner * dias_consumo_Scaner) / 1000
        valor_mes_Scaner_escolhido = tarifa_Scaner * calculo_kwh_nosso_Scaner
        valor_mes_Scaner_escolhidoF = float(f'''{valor_mes_Scaner_escolhido:.2f}''')

        diferenca_de_valor_Scaner = valor_mes_Scaner - valor_mes_Scaner_escolhido
        tempo_de_retorno_Scaner = valor_do_Scaner / diferenca_de_valor_Scaner
        tempo_em_anos_retorno_Scaner = tempo_de_retorno_Scaner / meses_ano
        tempo_em_anos_retorno_ScanerF = int(f'''{tempo_em_anos_retorno_Scaner:.0f}''')

        break

    # Batedeira
    valor_do_Batedeira = 1187.10
    potencia_Batedeira_escolhido = 275
    meses_ano = 12

    while True:
        valida6_1 = False
        potencia_Batedeira = potencia_usuario()
        horas_consumo_Batedeira = horas_dia()
        dias_consumo_Batedeira = num_dias()
        tarifa_Batedeira = tarifa_comp_eletrica()

        calculo_kwh_Batedeira = (potencia_Batedeira * horas_consumo_Batedeira * dias_consumo_Batedeira) / 1000
        valor_mes_Batedeira = tarifa_Batedeira * calculo_kwh_Batedeira
        valor_mes_BatedeiraF = float(f'''{valor_mes_Batedeira:.2f}''')

        # comparação

        calculo_kwh_nosso_Batedeira = (potencia_Batedeira_escolhido * horas_consumo_Batedeira * dias_consumo_Batedeira) / 1000
        valor_mes_Batedeira_escolhido = tarifa_Batedeira * calculo_kwh_nosso_Batedeira
        valor_mes_Batedeira_escolhidoF = float(f'''{valor_mes_Batedeira_escolhido:.2f}''')

        diferenca_de_valor_Batedeira = valor_mes_Batedeira - valor_mes_Batedeira_escolhido
        tempo_de_retorno_Batedeira = valor_do_Batedeira / diferenca_de_valor_Batedeira
        tempo_em_anos_retorno_Batedeira = tempo_de_retorno_Batedeira / meses_ano
        tempo_em_anos_retorno_BatedeiraF = int(f'''{tempo_em_anos_retorno_Batedeira:.0f}''')
        
        break

    # Cafeteira
    valor_do_Cafeteira = 89.90
    potencia_Cafeteira_escolhido = 450
    meses_ano = 12

    while True:
        valida6_2 = False
        potencia_Cafeteira = potencia_usuario()
        horas_consumo_Cafeteira = horas_dia()
        dias_consumo_Cafeteira = num_dias()
        tarifa_Cafeteira = tarifa_comp_eletrica()

        calculo_kwh_Cafeteira = (potencia_Cafeteira * horas_consumo_Cafeteira * dias_consumo_Cafeteira) / 1000
        valor_mes_Cafeteira = tarifa_Cafeteira * calculo_kwh_Cafeteira
        valor_mes_CafeteiraF = float(f'''{valor_mes_Cafeteira:.2f}''')

        # comparação

        calculo_kwh_nosso_Cafeteira = (potencia_Cafeteira_escolhido * horas_consumo_Cafeteira * dias_consumo_Cafeteira) / 1000
        valor_mes_Cafeteira_escolhido = tarifa_Cafeteira * calculo_kwh_nosso_Cafeteira
        valor_mes_Cafeteira_escolhidoF = float(f'''{valor_mes_Cafeteira_escolhido:.2f}''')

        diferenca_de_valor_Cafeteira = valor_mes_Cafeteira - valor_mes_Cafeteira_escolhido
        tempo_de_retorno_Cafeteira = valor_do_Cafeteira / diferenca_de_valor_Cafeteira
        tempo_em_anos_retorno_Cafeteira = tempo_de_retorno_Cafeteira / meses_ano
        tempo_em_anos_retorno_CafeteiraF = int(f'''{tempo_em_anos_retorno_Cafeteira:.0f}''')
        
        break

    # Exaustor
    valor_do_Exaustor = 257.90
    potencia_Exaustor_escolhido = 60
    meses_ano = 12

    while True:
        valida6_3 = False
        potencia_Exaustor = potencia_usuario()
        horas_consumo_Exaustor = horas_dia()
        dias_consumo_Exaustor = num_dias()
        tarifa_Exaustor = tarifa_comp_eletrica()

        calculo_kwh_Exaustor = (potencia_Exaustor * horas_consumo_Exaustor * dias_consumo_Exaustor) / 1000
        valor_mes_Exaustor = tarifa_Exaustor * calculo_kwh_Exaustor
        valor_mes_ExaustorF = float(f'''{valor_mes_Exaustor:.2f}''')

        # comparação

        calculo_kwh_nosso_Exaustor = (potencia_Exaustor_escolhido * horas_consumo_Exaustor * dias_consumo_Exaustor) / 1000
        valor_mes_Exaustor_escolhido = tarifa_Exaustor * calculo_kwh_nosso_Exaustor
        valor_mes_Exaustor_escolhidoF = float(f'''{valor_mes_Exaustor_escolhido:.2f}''')

        diferenca_de_valor_Exaustor = valor_mes_Exaustor - valor_mes_Exaustor_escolhido
        tempo_de_retorno_Exaustor = valor_do_Exaustor / diferenca_de_valor_Exaustor
        tempo_em_anos_retorno_Exaustor = tempo_de_retorno_Exaustor / meses_ano
        tempo_em_anos_retorno_ExaustorF = int(f'''{tempo_em_anos_retorno_Exaustor:.0f}''')
        
        break

    # Fogão
    valor_do_Fogao = 1399
    potencia_Fogao_escolhido = 7000
    meses_ano = 12

    while True:
        valida6_4 = False
        potencia_Fogao = potencia_usuario()
        horas_consumo_Fogao = horas_dia()
        dias_consumo_Fogao = num_dias()
        tarifa_Fogao = tarifa_comp_eletrica()

        calculo_kwh_Fogao = (potencia_Fogao * horas_consumo_Fogao * dias_consumo_Fogao) / 1000
        valor_mes_Fogao = tarifa_Fogao * calculo_kwh_Fogao
        valor_mes_FogaoF = float(f'''{valor_mes_Fogao:.2f}''')
        
        # comparação

        calculo_kwh_nosso_Fogao = (potencia_Fogao_escolhido * horas_consumo_Fogao * dias_consumo_Fogao) / 1000
        valor_mes_Fogao_escolhido = tarifa_Fogao * calculo_kwh_nosso_Fogao
        valor_mes_Fogao_escolhidoF = float(f'''{valor_mes_Fogao_escolhido:.2f}''')
        
        diferenca_de_valor_Fogao = valor_mes_Fogao - valor_mes_Fogao_escolhido
        tempo_de_retorno_Fogao = valor_do_Fogao / diferenca_de_valor_Fogao
        tempo_em_anos_retorno_Fogao = tempo_de_retorno_Fogao / meses_ano
        tempo_em_anos_retorno_FogaoF = int(f'''{tempo_em_anos_retorno_Fogao:.0f}''')
        
        break

    # Forno
    valor_do_Forno = 609
    potencia_Forno_escolhido = 1750
    meses_ano = 12

    while True:
        valida6_5 = False
        potencia_Forno = potencia_usuario()
        horas_consumo_Forno = horas_dia()
        dias_consumo_Forno = num_dias()
        tarifa_Forno = tarifa_comp_eletrica()

        calculo_kwh_Forno = (potencia_Forno * horas_consumo_Forno * dias_consumo_Forno) / 1000
        valor_mes_Forno = tarifa_Forno * calculo_kwh_Forno
        valor_mes_FornoF = float(f'''{valor_mes_Forno:.2f}''')

        # comparação

        calculo_kwh_nosso_Forno = (potencia_Forno_escolhido * horas_consumo_Forno * dias_consumo_Forno) / 1000
        valor_mes_Forno_escolhido = tarifa_Forno * calculo_kwh_nosso_Forno
        valor_mes_Forno_escolhidoF = float(f'''{valor_mes_Forno_escolhido:.2f}''')

        diferenca_de_valor_Forno = valor_mes_Forno - valor_mes_Forno_escolhido
        tempo_de_retorno_Forno = valor_do_Forno / diferenca_de_valor_Forno
        tempo_em_anos_retorno_Forno = tempo_de_retorno_Forno / meses_ano
        tempo_em_anos_retorno_FornoF = int(f'''{tempo_em_anos_retorno_Forno:.0f}''')
        
        break

    # Freezer
    valor_do_Freezer = 2160.39
    potencia_Freezer_escolhido = 115
    meses_ano = 12

    while True:
        valida6_6 = False
        potencia_Freezer = potencia_usuario()
        horas_consumo_Freezer = horas_dia()
        dias_consumo_Freezer = num_dias()
        tarifa_Freezer = tarifa_comp_eletrica()

        calculo_kwh_Freezer = (potencia_Freezer * horas_consumo_Freezer * dias_consumo_Freezer) / 1000
        valor_mes_Freezer = tarifa_Freezer * calculo_kwh_Freezer
        valor_mes_FreezerF = float(f'''{valor_mes_Freezer:.2f}''')

        # comparação

        calculo_kwh_nosso_Freezer = (potencia_Freezer_escolhido * horas_consumo_Freezer * dias_consumo_Freezer) / 1000
        valor_mes_Freezer_escolhido = tarifa_Freezer * calculo_kwh_nosso_Freezer
        valor_mes_Freezer_escolhidoF = float(f'''{valor_mes_Freezer_escolhido:.2f}''')

        diferenca_de_valor_Freezer = valor_mes_Freezer - valor_mes_Freezer_escolhido
        tempo_de_retorno_Freezer = valor_do_Freezer / diferenca_de_valor_Freezer
        tempo_em_anos_retorno_Freezer = tempo_de_retorno_Freezer / meses_ano
        tempo_em_anos_retorno_FreezerF = int(f'''{tempo_em_anos_retorno_Freezer:.0f}''')

        break

    # Geladeira
    valor_do_Geladeira = 4299
    potencia_Geladeira_escolhido = 175
    meses_ano = 12

    while True:
        valida6_7 = False
        potencia_Geladeira = potencia_usuario()
        horas_consumo_Geladeira = horas_dia()
        dias_consumo_Geladeira = num_dias()
        tarifa_Geladeira = tarifa_comp_eletrica()

        calculo_kwh_Geladeira = (potencia_Geladeira * horas_consumo_Geladeira * dias_consumo_Geladeira) / 1000
        valor_mes_Geladeira = tarifa_Geladeira * calculo_kwh_Geladeira
        valor_mes_GeladeiraF = float(f'''{valor_mes_Geladeira:.2f}''')

        # comparação

        calculo_kwh_nosso_Geladeira = (potencia_Geladeira_escolhido * horas_consumo_Geladeira * dias_consumo_Geladeira) / 1000
        valor_mes_Geladeira_escolhido = tarifa_Geladeira * calculo_kwh_nosso_Geladeira
        valor_mes_Geladeira_escolhidoF = float(f'''{valor_mes_Geladeira_escolhido:.2f}''')

        diferenca_de_valor_Geladeira = valor_mes_Geladeira - valor_mes_Geladeira_escolhido
        tempo_de_retorno_Geladeira = valor_do_Geladeira / diferenca_de_valor_Geladeira
        tempo_em_anos_retorno_Geladeira = tempo_de_retorno_Geladeira / meses_ano
        tempo_em_anos_retorno_GeladeiraF = int(f'''{tempo_em_anos_retorno_Geladeira:.0f}''')
        
        break


    # Lava Louça
    valor_do_Louca = 1738
    potencia_Louca_escolhido = 780
    meses_ano = 12

    while True:
        valida6_8 = False
        potencia_Louca = potencia_usuario()
        horas_consumo_Louca = horas_dia()
        dias_consumo_Louca = num_dias()
        tarifa_Louca = tarifa_comp_eletrica()

        calculo_kwh_Louca = (potencia_Louca * horas_consumo_Louca * dias_consumo_Louca) / 1000
        valor_mes_Louca = tarifa_Louca * calculo_kwh_Louca
        valor_mes_LoucaF = float(f'''{valor_mes_Louca:.2f}''')

        # comparação

        calculo_kwh_nosso_Louca = (potencia_Louca_escolhido * horas_consumo_Louca * dias_consumo_Louca) / 1000
        valor_mes_Louca_escolhido = tarifa_Louca * calculo_kwh_nosso_Louca
        valor_mes_Louca_escolhidoF = float(f'''{valor_mes_Louca_escolhido:.2f}''')

        diferenca_de_valor_Louca = valor_mes_Louca - valor_mes_Louca_escolhido
        tempo_de_retorno_Louca = valor_do_Louca / diferenca_de_valor_Louca
        tempo_em_anos_retorno_Louca = tempo_de_retorno_Louca / meses_ano
        tempo_em_anos_retorno_LoucaF = int(f'''{tempo_em_anos_retorno_Louca:.0f}''')
        
        break

    # Microondas
    valor_do_Microondas = 1379
    potencia_Microondas_escolhido = 1000
    meses_ano = 12

    while True:
        valida6_9 = False
        potencia_Microondas = potencia_usuario()
        horas_consumo_Microondas = horas_dia()
        dias_consumo_Microondas = num_dias()
        tarifa_Microondas = tarifa_comp_eletrica()

        calculo_kwh_Microondas = (potencia_Microondas * horas_consumo_Microondas * dias_consumo_Microondas) / 1000
        valor_mes_Microondas = tarifa_Microondas * calculo_kwh_Microondas
        valor_mes_MicroondasF = float(f'''{valor_mes_Microondas:.2f}''')

        # comparação

        calculo_kwh_nosso_Microondas = (potencia_Microondas_escolhido * horas_consumo_Microondas * dias_consumo_Microondas) / 1000
        valor_mes_Microondas_escolhido = tarifa_Microondas * calculo_kwh_nosso_Microondas
        valor_mes_Microondas_escolhidoF = float(f'''{valor_mes_Microondas_escolhido:.2f}''')

        diferenca_de_valor_Microondas = valor_mes_Microondas - valor_mes_Microondas_escolhido
        tempo_de_retorno_Microondas = valor_do_Microondas / diferenca_de_valor_Microondas
        tempo_em_anos_retorno_Microondas = tempo_de_retorno_Microondas / meses_ano
        tempo_em_anos_retorno_MicroondasF = int(f'''{tempo_em_anos_retorno_Microondas:.0f}''')
        
        break

    # Processador
    valor_do_Processador = 1048.05
    potencia_Processador_escolhido = 250
    meses_ano = 12

    while True:
        valida6_10 = False
        potencia_Processador = potencia_usuario()
        horas_consumo_Processador = horas_dia()
        dias_consumo_Processador = num_dias()
        tarifa_Processador = tarifa_comp_eletrica()

        calculo_kwh_Processador = (potencia_Processador * horas_consumo_Processador * dias_consumo_Processador) / 1000
        valor_mes_Processador = tarifa_Processador * calculo_kwh_Processador
        valor_mes_ProcessadorF = float(f'''{valor_mes_Processador:.2f}''')

        # comparação

        calculo_kwh_nosso_Processador = (potencia_Processador_escolhido * horas_consumo_Processador * dias_consumo_Processador) / 1000
        valor_mes_Processador_escolhido = tarifa_Processador * calculo_kwh_nosso_Processador
        valor_mes_Processador_escolhidoF = float(f'''{valor_mes_Processador_escolhido:.2f}''')
        
        diferenca_de_valor_Processador = valor_mes_Processador - valor_mes_Processador_escolhido
        tempo_de_retorno_Processador = valor_do_Processador / diferenca_de_valor_Processador
        tempo_em_anos_retorno_Processador = tempo_de_retorno_Processador / meses_ano
        tempo_em_anos_retorno_ProcessadorF = int(f'''{tempo_em_anos_retorno_Processador:.0f}''')
        
        break

    # Purificador
    valor_do_Purificador = 812.14
    potencia_Purificador_escolhido = 82
    meses_ano = 12

    while True:
        valida6_11 = False
        potencia_Purificador = potencia_usuario()
        horas_consumo_Purificador = horas_dia()
        dias_consumo_Purificador = num_dias()
        tarifa_Purificador = tarifa_comp_eletrica()

        calculo_kwh_Purificador = (potencia_Purificador * horas_consumo_Purificador * dias_consumo_Purificador) / 1000
        valor_mes_Purificador = tarifa_Purificador * calculo_kwh_Purificador
        valor_mes_PurificadorF = float(f'''{valor_mes_Purificador:.2f}''')

        # comparação

        calculo_kwh_nosso_Purificador = (potencia_Purificador_escolhido * horas_consumo_Purificador * dias_consumo_Purificador) / 1000
        valor_mes_Purificador_escolhido = tarifa_Purificador * calculo_kwh_nosso_Purificador
        valor_mes_Purificador_escolhidoF = float(f'''{valor_mes_Purificador_escolhido:.2f}''')
        
        diferenca_de_valor_Purificador = valor_mes_Purificador - valor_mes_Purificador_escolhido
        tempo_de_retorno_Purificador = valor_do_Purificador / diferenca_de_valor_Purificador
        tempo_em_anos_retorno_Purificador = tempo_de_retorno_Purificador / meses_ano
        tempo_em_anos_retorno_PurificadorF = int(f'''{tempo_em_anos_retorno_Purificador:.0f}''')
        
        break

    # Sanduicheira
    valor_do_Sanduicheira = 149
    potencia_Sanduicheira_escolhido = 750
    meses_ano = 12

    while True:
        valida6_12 = False
        potencia_Sanduicheira = potencia_usuario()
        horas_consumo_Sanduicheira = horas_dia()
        dias_consumo_Sanduicheira = num_dias()
        tarifa_Sanduicheira = tarifa_comp_eletrica()

        calculo_kwh_Sanduicheira = (potencia_Sanduicheira * horas_consumo_Sanduicheira * dias_consumo_Sanduicheira) / 1000
        valor_mes_Sanduicheira = tarifa_Sanduicheira * calculo_kwh_Sanduicheira
        valor_mes_SanduicheiraF = float(f'''{valor_mes_Sanduicheira:.2f}''')

        # comparação

        calculo_kwh_nosso_Sanduicheira = (potencia_Sanduicheira_escolhido * horas_consumo_Sanduicheira * dias_consumo_Sanduicheira) / 1000
        valor_mes_Sanduicheira_escolhido = tarifa_Sanduicheira * calculo_kwh_nosso_Sanduicheira
        valor_mes_Sanduicheira_escolhidoF = float(f'''{valor_mes_Sanduicheira_escolhido:.2f}''')
        
        diferenca_de_valor_Sanduicheira = valor_mes_Sanduicheira - valor_mes_Sanduicheira_escolhido
        tempo_de_retorno_Sanduicheira = valor_do_Sanduicheira / diferenca_de_valor_Sanduicheira
        tempo_em_anos_retorno_Sanduicheira = tempo_de_retorno_Sanduicheira / meses_ano
        tempo_em_anos_retorno_SanduicheiraF = int(f'''{tempo_em_anos_retorno_Sanduicheira:.0f}''')
        
        break

    # Torneira elétrica
    valor_do_Torneira = 208.90
    potencia_Torneira_escolhido = 4500
    meses_ano = 12

    while True:
        valida6_13 = False
        potencia_Torneira = potencia_usuario()
        horas_consumo_Torneira = horas_dia()
        dias_consumo_Torneira = num_dias()
        tarifa_Torneira = tarifa_comp_eletrica()

        calculo_kwh_Torneira = (potencia_Torneira * horas_consumo_Torneira * dias_consumo_Torneira) / 1000
        valor_mes_Torneira = tarifa_Torneira * calculo_kwh_Torneira
        valor_mes_TorneiraF = float(f'''{valor_mes_Torneira:.2f}''')

        # comparação

        calculo_kwh_nosso_Torneira = (potencia_Torneira_escolhido * horas_consumo_Torneira * dias_consumo_Torneira) / 1000
        valor_mes_Torneira_escolhido = tarifa_Torneira * calculo_kwh_nosso_Torneira
        valor_mes_Torneira_escolhidoF = float(f'''{valor_mes_Torneira_escolhido:.2f}''')
        
        diferenca_de_valor_Torneira = valor_mes_Torneira - valor_mes_Torneira_escolhido
        tempo_de_retorno_Torneira = valor_do_Torneira / diferenca_de_valor_Torneira
        tempo_em_anos_retorno_Torneira = tempo_de_retorno_Torneira / meses_ano
        tempo_em_anos_retorno_TorneiraF = int(f'''{tempo_em_anos_retorno_Torneira:.0f}''')
        
        break

    # Torradeira
    valor_do_Torradeira = 211.94
    potencia_Torradeira_escolhido = 800
    meses_ano = 12

    while True:
        valida6_14 = False
        potencia_Torradeira = potencia_usuario()
        horas_consumo_Torradeira = horas_dia()
        dias_consumo_Torradeira = num_dias()
        tarifa_Torradeira = tarifa_comp_eletrica()

        calculo_kwh_Torradeira = (potencia_Torradeira * horas_consumo_Torradeira * dias_consumo_Torradeira) / 1000
        valor_mes_Torradeira = tarifa_Torradeira * calculo_kwh_Torradeira
        valor_mes_TorradeiraF = float(f'''{valor_mes_Torradeira:.2f}''')

        # comparação

        calculo_kwh_nosso_Torradeira = (potencia_Torradeira_escolhido * horas_consumo_Torradeira * dias_consumo_Torradeira) / 1000
        valor_mes_Torradeira_escolhido = tarifa_Torradeira * calculo_kwh_nosso_Torradeira
        valor_mes_Torradeira_escolhidoF = float(f'''{valor_mes_Torradeira_escolhido:.2f}''')
        
        diferenca_de_valor_Torradeira = valor_mes_Torradeira - valor_mes_Torradeira_escolhido
        tempo_de_retorno_Torradeira = valor_do_Torradeira / diferenca_de_valor_Torradeira
        tempo_em_anos_retorno_Torradeira = tempo_de_retorno_Torradeira / meses_ano
        tempo_em_anos_retorno_TorradeiraF = int(f'''{tempo_em_anos_retorno_Torradeira:.0f}''')
        
        break

    # Barbeador elétrico
    valor_do_Barbeador = 125.56
    potencia_Barbeador_escolhido = 8
    meses_ano = 12

    while True:
        valida7_1 = False
        potencia_Barbeador = potencia_usuario()
        horas_consumo_Barbeador = horas_dia()
        dias_consumo_Barbeador = num_dias()
        tarifa_Barbeador = tarifa_comp_eletrica()

        calculo_kwh_Barbeador = (potencia_Barbeador * horas_consumo_Barbeador * dias_consumo_Barbeador) / 1000
        valor_mes_Barbeador = tarifa_Barbeador * calculo_kwh_Barbeador
        valor_mes_BarbeadorF = float(f'''{valor_mes_Barbeador:.2f}''')

        # comparação

        calculo_kwh_nosso_Barbeador = (potencia_Barbeador_escolhido * horas_consumo_Barbeador * dias_consumo_Barbeador) / 1000
        valor_mes_Barbeador_escolhido = tarifa_Barbeador * calculo_kwh_nosso_Barbeador
        valor_mes_Barbeador_escolhidoF = float(f'''{valor_mes_Barbeador_escolhido:.2f}''')
        
        diferenca_de_valor_Barbeador = valor_mes_Barbeador - valor_mes_Barbeador_escolhido
        tempo_de_retorno_Barbeador = valor_do_Barbeador / diferenca_de_valor_Barbeador
        tempo_em_anos_retorno_Barbeador = tempo_de_retorno_Barbeador / meses_ano
        tempo_em_anos_retorno_BarbeadorF = int(f'''{tempo_em_anos_retorno_Barbeador:.0f}''')
        
        break

    # Chapinha
    valor_do_Chapinha = 107.10
    potencia_Chapinha_escolhido = 45
    meses_ano = 12

    while True:
        valida7_2 = False
        potencia_Chapinha = potencia_usuario()
        horas_consumo_Chapinha = horas_dia()
        dias_consumo_Chapinha = num_dias()
        tarifa_Chapinha = tarifa_comp_eletrica()

        calculo_kwh_Chapinha = (potencia_Chapinha * horas_consumo_Chapinha * dias_consumo_Chapinha) / 1000
        valor_mes_Chapinha = tarifa_Chapinha * calculo_kwh_Chapinha
        valor_mes_ChapinhaF = float(f'''{valor_mes_Chapinha:.2f}''')

        # comparação

        calculo_kwh_nosso_Chapinha = (potencia_Chapinha_escolhido * horas_consumo_Chapinha * dias_consumo_Chapinha) / 1000
        valor_mes_Chapinha_escolhido = tarifa_Chapinha * calculo_kwh_nosso_Chapinha
        valor_mes_Chapinha_escolhidoF = float(f'''{valor_mes_Chapinha_escolhido:.2f}''')

        diferenca_de_valor_Chapinha = valor_mes_Chapinha - valor_mes_Chapinha_escolhido
        tempo_de_retorno_Chapinha = valor_do_Chapinha / diferenca_de_valor_Chapinha
        tempo_em_anos_retorno_Chapinha = tempo_de_retorno_Chapinha / meses_ano
        tempo_em_anos_retorno_ChapinhaF = int(f'''{tempo_em_anos_retorno_Chapinha:.0f}''')
        
        break

    # Chuveiro
    valor_do_Chuveiro = 99
    potencia_Chuveiro_escolhido = 5500
    meses_ano = 12

    while True:
        valida7_3 = False
        potencia_Chuveiro = potencia_usuario()
        horas_consumo_Chuveiro = horas_dia()
        dias_consumo_Chuveiro = num_dias()
        tarifa_Chuveiro = tarifa_comp_eletrica()

        calculo_kwh_Chuveiro = (potencia_Chuveiro * horas_consumo_Chuveiro * dias_consumo_Chuveiro) / 1000
        valor_mes_Chuveiro = tarifa_Chuveiro * calculo_kwh_Chuveiro
        valor_mes_ChuveiroF = float(f'''{valor_mes_Chuveiro:.2f}''')

        # comparação

        calculo_kwh_nosso_Chuveiro = (potencia_Chuveiro_escolhido * horas_consumo_Chuveiro * dias_consumo_Chuveiro) / 1000
        valor_mes_Chuveiro_escolhido = tarifa_Chuveiro * calculo_kwh_nosso_Chuveiro
        valor_mes_Chuveiro_escolhidoF = float(f'''{valor_mes_Chuveiro_escolhido:.2f}''')
        
        diferenca_de_valor_Chuveiro = valor_mes_Chuveiro - valor_mes_Chuveiro_escolhido
        tempo_de_retorno_Chuveiro = valor_do_Chuveiro / diferenca_de_valor_Chuveiro
        tempo_em_anos_retorno_Chuveiro = tempo_de_retorno_Chuveiro / meses_ano
        tempo_em_anos_retorno_ChuveiroF = int(f'''{tempo_em_anos_retorno_Chuveiro:.0f}''')
        
        break

    # Secador de cabelo
    valor_do_Secador = 58.50
    potencia_Secador_escolhido = 1200
    meses_ano = 12

    while True:
        valida7_4 = False
        potencia_Secador = potencia_usuario()
        horas_consumo_Secador = horas_dia()
        dias_consumo_Secador = num_dias()
        tarifa_Secador = tarifa_comp_eletrica()

        calculo_kwh_Secador = (potencia_Secador * horas_consumo_Secador * dias_consumo_Secador) / 1000
        valor_mes_Secador = tarifa_Secador * calculo_kwh_Secador
        valor_mes_SecadorF = float(f'''{valor_mes_Secador:.2f}''')

        # comparação

        calculo_kwh_nosso_Secador = (potencia_Secador_escolhido * horas_consumo_Secador * dias_consumo_Secador) / 1000
        valor_mes_Secador_escolhido = tarifa_Secador * calculo_kwh_nosso_Secador
        valor_mes_Secador_escolhidoF = float(f'''{valor_mes_Secador_escolhido:.2f}''')
        
        diferenca_de_valor_Secador = valor_mes_Secador - valor_mes_Secador_escolhido
        tempo_de_retorno_Secador = valor_do_Secador / diferenca_de_valor_Secador
        tempo_em_anos_retorno_Secador = tempo_de_retorno_Secador / meses_ano
        tempo_em_anos_retorno_SecadorF = int(f'''{tempo_em_anos_retorno_Secador:.0f}''')
        
        break

    # Escova elétrica
    valor_do_Escova = 109.49
    potencia_Escova_escolhido = 14
    meses_ano = 12

    while True:
        valida7_5 = False
        potencia_Escova = potencia_usuario()
        horas_consumo_Escova = horas_dia()
        dias_consumo_Escova = num_dias()
        tarifa_Escova = tarifa_comp_eletrica()

        calculo_kwh_Escova = (potencia_Escova * horas_consumo_Escova * dias_consumo_Escova) / 1000
        valor_mes_Escova = tarifa_Escova * calculo_kwh_Escova
        valor_mes_EscovaF = float(f'''{valor_mes_Escova:.2f}''')

        # comparação

        calculo_kwh_nosso_Escova = (potencia_Escova_escolhido * horas_consumo_Escova * dias_consumo_Escova) / 1000
        valor_mes_Escova_escolhido = tarifa_Escova * calculo_kwh_nosso_Escova
        valor_mes_Escova_escolhidoF = float(f'''{valor_mes_Escova_escolhido:.2f}''')
        
        diferenca_de_valor_Escova = valor_mes_Escova - valor_mes_Escova_escolhido
        tempo_de_retorno_Escova = valor_do_Escova / diferenca_de_valor_Escova
        tempo_em_anos_retorno_Escova = tempo_de_retorno_Escova / meses_ano
        tempo_em_anos_retorno_EscovaF = int(f'''{tempo_em_anos_retorno_Escova:.0f}''')
        
        break

    # Bomba de água
    valor_do_Bomba = 450
    potencia_Bomba_escolhido = 450
    meses_ano = 12

    while True:
        valida8_1 = False
        potencia_Bomba = potencia_usuario()
        horas_consumo_Bomba = horas_dia()
        dias_consumo_Bomba = num_dias()
        tarifa_Bomba = tarifa_comp_eletrica()

        calculo_kwh_Bomba = (potencia_Bomba * horas_consumo_Bomba * dias_consumo_Bomba) / 1000
        valor_mes_Bomba = tarifa_Bomba * calculo_kwh_Bomba
        valor_mes_BombaF = float(f'''{valor_mes_Bomba:.2f}''')

        # comparação

        calculo_kwh_nosso_Bomba = (potencia_Bomba_escolhido * horas_consumo_Bomba * dias_consumo_Bomba) / 1000
        valor_mes_Bomba_escolhido = tarifa_Bomba * calculo_kwh_nosso_Bomba
        valor_mes_Bomba_escolhidoF = float(f'''{valor_mes_Bomba_escolhido:.2f}''')
        
        diferenca_de_valor_Bomba = valor_mes_Bomba - valor_mes_Bomba_escolhido
        tempo_de_retorno_Bomba = valor_do_Bomba / diferenca_de_valor_Bomba
        tempo_em_anos_retorno_Bomba = tempo_de_retorno_Bomba / meses_ano
        tempo_em_anos_retorno_BombaF = int(f'''{tempo_em_anos_retorno_Bomba:.0f}''')
        
        break

    # Cerca elétrica
    valor_do_Cerca = 236.65
    potencia_Cerca_escolhido = 4.5
    meses_ano = 12

    while True:
        valida8_2 = False
        potencia_Cerca = potencia_usuario()
        horas_consumo_Cerca = horas_dia()
        dias_consumo_Cerca = num_dias()
        tarifa_Cerca = tarifa_comp_eletrica()

        calculo_kwh_Cerca = (potencia_Cerca * horas_consumo_Cerca * dias_consumo_Cerca) / 1000
        valor_mes_Cerca = tarifa_Cerca * calculo_kwh_Cerca
        valor_mes_CercaF = float(f'''{valor_mes_Cerca:.2f}''')

        # comparação

        calculo_kwh_nosso_Cerca = (potencia_Cerca_escolhido * horas_consumo_Cerca * dias_consumo_Cerca) / 1000
        valor_mes_Cerca_escolhido = tarifa_Cerca * calculo_kwh_nosso_Cerca
        valor_mes_Cerca_escolhidoF = float(f'''{valor_mes_Cerca_escolhido:.2f}''')
        
        diferenca_de_valor_Cerca = valor_mes_Cerca - valor_mes_Cerca_escolhido
        tempo_de_retorno_Cerca = valor_do_Cerca / diferenca_de_valor_Cerca
        tempo_em_anos_retorno_Cerca = tempo_de_retorno_Cerca / meses_ano
        tempo_em_anos_retorno_CercaF = int(f'''{tempo_em_anos_retorno_Cerca:.0f}''')
        
        break

    # Churrasqueira elétrica
    valor_do_Churrasqueira = 140.25
    potencia_Churrasqueira_escolhido = 1800
    meses_ano = 12

    while True:
        valida8_3 = False
        potencia_Churrasqueira = potencia_usuario()
        horas_consumo_Churrasqueira = horas_dia()
        dias_consumo_Churrasqueira = num_dias()
        tarifa_Churrasqueira = tarifa_comp_eletrica()

        calculo_kwh_Churrasqueira = (potencia_Churrasqueira * horas_consumo_Churrasqueira * dias_consumo_Churrasqueira) / 1000
        valor_mes_Churrasqueira = tarifa_Churrasqueira * calculo_kwh_Churrasqueira
        valor_mes_ChurrasqueiraF = float(f'''{valor_mes_Churrasqueira:.2f}''')

        # comparação

        calculo_kwh_nosso_Churrasqueira = (potencia_Churrasqueira_escolhido * horas_consumo_Churrasqueira * dias_consumo_Churrasqueira) / 1000
        valor_mes_Churrasqueira_escolhido = tarifa_Churrasqueira * calculo_kwh_nosso_Churrasqueira
        valor_mes_Churrasqueira_escolhidoF = float(f'''{valor_mes_Churrasqueira_escolhido:.2f}''')
        
        diferenca_de_valor_Churrasqueira = valor_mes_Churrasqueira - valor_mes_Churrasqueira_escolhido
        tempo_de_retorno_Churrasqueira = valor_do_Churrasqueira / diferenca_de_valor_Churrasqueira
        tempo_em_anos_retorno_Churrasqueira = tempo_de_retorno_Churrasqueira / meses_ano
        tempo_em_anos_retorno_ChurrasqueiraF = int(f'''{tempo_em_anos_retorno_Churrasqueira:.0f}''')
        
        break

    # Cortador de grama
    valor_do_Cortador = 444.90
    potencia_Cortador_escolhido = 1000
    meses_ano = 12

    while True:
        valida8_4 = False
        potencia_Cortador = potencia_usuario()
        horas_consumo_Cortador = horas_dia()
        dias_consumo_Cortador = num_dias()
        tarifa_Cortador = tarifa_comp_eletrica()

        calculo_kwh_Cortador = (potencia_Cortador * horas_consumo_Cortador * dias_consumo_Cortador) / 1000
        valor_mes_Cortador = tarifa_Cortador * calculo_kwh_Cortador
        valor_mes_CortadorF = float(f'''{valor_mes_Cortador:.2f}''')

        # comparação

        calculo_kwh_nosso_Cortador = (potencia_Cortador_escolhido * horas_consumo_Cortador * dias_consumo_Cortador) / 1000
        valor_mes_Cortador_escolhido = tarifa_Cortador * calculo_kwh_nosso_Cortador
        valor_mes_Cortador_escolhidoF = float(f'''{valor_mes_Cortador_escolhido:.2f}''')
        
        diferenca_de_valor_Cortador = valor_mes_Cortador - valor_mes_Cortador_escolhido
        tempo_de_retorno_Cortador = valor_do_Cortador / diferenca_de_valor_Cortador
        tempo_em_anos_retorno_Cortador = tempo_de_retorno_Cortador / meses_ano
        tempo_em_anos_retorno_CortadorF = int(f'''{tempo_em_anos_retorno_Cortador:.0f}''')
        
        break

    # Irrigador de água
    valor_do_Irrigador = 37.41
    potencia_Irrigador_escolhido = 25
    meses_ano = 12

    while True:
        valida8_5 = False
        potencia_Irrigador = potencia_usuario()
        horas_consumo_Irrigador = horas_dia()
        dias_consumo_Irrigador = num_dias()
        tarifa_Irrigador = tarifa_comp_eletrica()

        calculo_kwh_Irrigador = (potencia_Irrigador * horas_consumo_Irrigador * dias_consumo_Irrigador) / 1000
        valor_mes_Irrigador = tarifa_Irrigador * calculo_kwh_Irrigador
        valor_mes_IrrigadorF = float(f'''{valor_mes_Irrigador:.2f}''')

        # comparação

        calculo_kwh_nosso_Irrigador = (potencia_Irrigador_escolhido * horas_consumo_Irrigador * dias_consumo_Irrigador) / 1000
        valor_mes_Irrigador_escolhido = tarifa_Irrigador * calculo_kwh_nosso_Irrigador
        valor_mes_Irrigador_escolhidoF = float(f'''{valor_mes_Irrigador_escolhido:.2f}''')
        
        diferenca_de_valor_Irrigador = valor_mes_Irrigador - valor_mes_Irrigador_escolhido
        tempo_de_retorno_Irrigador = valor_do_Irrigador / diferenca_de_valor_Irrigador
        tempo_em_anos_retorno_Irrigador = tempo_de_retorno_Irrigador / meses_ano
        tempo_em_anos_retorno_IrrigadorF = int(f'''{tempo_em_anos_retorno_Irrigador:.0f}''')
        
        break

    saidaMedio = {'ValorConsumidoNoMesSom': valor_mes_somF,
                    'ValorConsumidoNoMesSomSugerido': valor_mes_som_escolhidoF,
                    'TempoRetornoValorInvestidoSom': tempo_em_anos_retorno_somF,
                    'ValorConsumidoNoMesUmidificador': valor_mes_umidificadorF,
                    'ValorConsumidoNoMesUmidificadorSugerido': valor_mes_umidificador_escolhidoF,
                    'TempoRetornoValorInvestidoUmidificador': tempo_em_anos_retorno_umidificadorF,
                    'ValorConsumidoNoMesAr': valor_mes_arF,
                    'ValorConsumidoNoMesArSugerido': valor_mes_ar_escolhidoF,
                    'TempoRetornoValorInvestidoAr': tempo_em_anos_retorno_arF,
                    'ValorConsumidoNoMesDVD': valor_mes_DVDF,
                    'ValorConsumidoNoMesDVDSugerido': valor_mes_DVD_escolhidoF,
                    'TempoRetornoValorInvestidoDVD': tempo_em_anos_retorno_DVDF,
                    'ValorConsumidoNoMesHome': valor_mes_HomeF,
                    'ValorConsumidoNoMesHomeSugerido': valor_mes_Home_escolhidoF,
                    'TempoRetornoValorInvestidoHome': tempo_em_anos_retorno_HomeF,
                    'ValorConsumidoNoMesTelefone': valor_mes_TelefoneF,
                    'ValorConsumidoNoMesTelefoneSugerido': valor_mes_Telefone_escolhidoF,
                    'TempoRetornoValorInvestidoTelefone': tempo_em_anos_retorno_TelefoneF,
                    'ValorConsumidoNoMesTelevisão': valor_mes_TelevisãoF,
                    'ValorConsumidoNoMesTelevisãoSugerido': valor_mes_Televisão_escolhidoF,
                    'TempoRetornoValorInvestidoTelevisão': tempo_em_anos_retorno_TelevisãoF,
                    'ValorConsumidoNoMesVentilador': valor_mes_VentiladorF,
                    'ValorConsumidoNoMesVentiladorSugerido': valor_mes_Ventilador_escolhidoF,
                    'TempoRetornoValorInvestidoVentilador': tempo_em_anos_retorno_VentiladorF,
                    'ValorConsumidoNoMesVideoGame': valor_mes_VideoF,
                    'ValorConsumidoNoMesVideoGameSugerido': valor_mes_Video_escolhidoF,
                    'TempoRetornoValorInvestidoVideoGame': tempo_em_anos_retorno_VideoF,
                    'ValorConsumidoNoMesAbajur': valor_mes_AbajurF,
                    'ValorConsumidoNoMesAbajurSugerido': valor_mes_Abajur_escolhidoF,
                    'TempoRetornoValorInvestidoAbajur': tempo_em_anos_retorno_AbajurF,
                    'ValorConsumidoNoMesAquecedor': valor_mes_AquecedorF,
                    'ValorConsumidoNoMesAquecedorSugerido': valor_mes_Aquecedor_escolhidoF,
                    'TempoRetornoValorInvestidoAquecedor': tempo_em_anos_retorno_AquecedorF,
                    'ValorConsumidoNoMesNebulizador': valor_mes_NebulizadorF,
                    'ValorConsumidoNoMesNebulizadorSugerido': valor_mes_Nebulizador_escolhidoF,
                    'TempoRetornoValorInvestidoNebulizador': tempo_em_anos_retorno_NebulizadorF,
                    'ValorConsumidoNoMesRadio': valor_mes_RadioF,
                    'ValorConsumidoNoMesRadioSugerido': valor_mes_Radio_escolhidoF,
                    'TempoRetornoValorInvestidoRadio': tempo_em_anos_retorno_RadioF,
                    'ValorConsumidoNoMesApirador': valor_mes_ApiradorF,
                    'ValorConsumidoNoMesApiradorSugerido': valor_mes_Apirador_escolhidoF,
                    'TempoRetornoValorInvestidoApirador': tempo_em_anos_retorno_ApiradorF,
                    'ValorConsumidoNoMesDesumidificador': valor_mes_DesumidificadorF,
                    'ValorConsumidoNoMesDesumidificadorSugerido': valor_mes_Desumidificador_escolhidoF,
                    'TempoRetornoValorInvestidoDesumidificador': tempo_em_anos_retorno_DesumidificadorF,
                    'ValorConsumidoNoMesFerro': valor_mes_FerroF,
                    'ValorConsumidoNoMesFerroSugerido': valor_mes_Ferro_escolhidoF,
                    'TempoRetornoValorInvestidoFerro': tempo_em_anos_retorno_FerroF,
                    'ValorConsumidoNoMesMaquinaDeLavar': valor_mes_MaquinaF,
                    'ValorConsumidoNoMesMaquinaDeLavarSugerido': valor_mes_Maquina_escolhidoF,
                    'TempoRetornoValorInvestidoMaquinaDeLavar': tempo_em_anos_retorno_MaquinaF,
                    'ValorConsumidoNoMesMaquinaDeSecar': valor_mes_secarF,
                    'ValorConsumidoNoMesMaquinaDeSecarSugerido': valor_mes_secar_escolhidoF,
                    'TempoRetornoValorInvestidoMaquinaDeSecar': tempo_em_anos_retorno_secarF,
                    'ValorConsumidoNoMesMaquinaDeCostura': valor_mes_costuraF,
                    'ValorConsumidoNoMesMaquinaDeCosturaSugerido': valor_mes_costura_escolhidoF,
                    'TempoRetornoValorInvestidoMaquinaDeCostura': tempo_em_anos_retorno_costuraF,
                    'ValorConsumidoNoMesAlarme': valor_mes_AlarmeF,
                    'ValorConsumidoNoMesAlarmeSugerido': valor_mes_Alarme_escolhidoF,
                    'TempoRetornoValorInvestidoAlarme': tempo_em_anos_retorno_AlarmeF,
                    'ValorConsumidoNoMesPortao': valor_mes_PortaoF,
                    'ValorConsumidoNoMesPortaoSugerido': valor_mes_Portao_escolhidoF,
                    'TempoRetornoValorInvestidoPortao': tempo_em_anos_retorno_PortaoF,
                    'ValorConsumidoNoMesSensor': valor_mes_SensorF,
                    'ValorConsumidoNoMesSensorSugerido': valor_mes_Sensor_escolhidoF,
                    'TempoRetornoValorInvestidoSensor': tempo_em_anos_retorno_SensorF,
                    'ValorConsumidoNoMesComputador': valor_mes_ComputadorF,
                    'ValorConsumidoNoMesComputadorSugerido': valor_mes_Computador_escolhidoF,
                    'TempoRetornoValorInvestidoComputador': tempo_em_anos_retorno_ComputadorF,
                    'ValorConsumidoNoMesImpressora': valor_mes_ImpressoraF,
                    'ValorConsumidoNoMesImpressoraSugerido': valor_mes_Impressora_escolhidoF,
                    'TempoRetornoValorInvestidoImpressora': tempo_em_anos_retorno_ImpressoraF,
                    'ValorConsumidoNoMesMoldem': valor_mes_MoldemF,
                    'ValorConsumidoNoMesMoldemSugerido': valor_mes_Moldem_escolhidoF,
                    'TempoRetornoValorInvestidoMoldem': tempo_em_anos_retorno_MoldemF,
                    'ValorConsumidoNoMesMonitor': valor_mes_MonitorF,
                    'ValorConsumidoNoMesMonitorSugerido': valor_mes_Monitor_escolhidoF,
                    'TempoRetornoValorInvestidoMonitor': tempo_em_anos_retorno_MonitorF,
                    'ValorConsumidoNoMesMultifuncional': valor_mes_MultifuncionalF,
                    'ValorConsumidoNoMesMultifuncionalSugerido': valor_mes_Multifuncional_escolhidoF,
                    'TempoRetornoValorInvestidoMultifuncional': tempo_em_anos_retorno_MultifuncionalF,
                    'ValorConsumidoNoMesNotebook': valor_mes_NotebookF,
                    'ValorConsumidoNoMesNotebookSugerido': valor_mes_Notebook_escolhidoF,
                    'TempoRetornoValorInvestidoNotebook': tempo_em_anos_retorno_NotebookF,
                    'ValorConsumidoNoMesScaner': valor_mes_ScanerF,
                    'ValorConsumidoNoMesScanerSugerido': valor_mes_Scaner_escolhidoF,
                    'TempoRetornoValorInvestidoScaner': tempo_em_anos_retorno_ScanerF,
                    'ValorConsumidoNoMesBatedeira': valor_mes_BatedeiraF,
                    'ValorConsumidoNoMesBatedeiraSugerido': valor_mes_Batedeira_escolhidoF,
                    'TempoRetornoValorInvestidoBatedeira': tempo_em_anos_retorno_BatedeiraF,
                    'ValorConsumidoNoMesCafeteira': valor_mes_CafeteiraF,
                    'ValorConsumidoNoMesCafeteiraSugerido': valor_mes_Cafeteira_escolhidoF,
                    'TempoRetornoValorInvestidoCafeteira': tempo_em_anos_retorno_CafeteiraF,
                    'ValorConsumidoNoMesExaustor': valor_mes_ExaustorF,
                    'ValorConsumidoNoMesExaustorSugerido': valor_mes_Exaustor_escolhidoF,
                    'TempoRetornoValorInvestidoExaustor': tempo_em_anos_retorno_ExaustorF,
                    'ValorConsumidoNoMesFogao': valor_mes_FogaoF,
                    'ValorConsumidoNoMesFogaoSugerido': valor_mes_Fogao_escolhidoF,
                    'TempoRetornoValorInvestidoFogao': tempo_em_anos_retorno_FogaoF,
                    'ValorConsumidoNoMesForno': valor_mes_FornoF,
                    'ValorConsumidoNoMesFornoSugerido': valor_mes_Forno_escolhidoF,
                    'TempoRetornoValorInvestidoForno': tempo_em_anos_retorno_FornoF,
                    'ValorConsumidoNoMesFreezer': valor_mes_FreezerF,
                    'ValorConsumidoNoMesFreezerSugerido': valor_mes_Freezer_escolhidoF,
                    'TempoRetornoValorInvestidoFreezer': tempo_em_anos_retorno_FreezerF,
                    'ValorConsumidoNoMesGeladeira': valor_mes_GeladeiraF,
                    'ValorConsumidoNoMesGeladeiraSugerido': valor_mes_Geladeira_escolhidoF,
                    'TempoRetornoValorInvestidoGeladeira': tempo_em_anos_retorno_GeladeiraF,
                    'ValorConsumidoNoMesLavaLouca': valor_mes_LoucaF,
                    'ValorConsumidoNoMesLavaLoucaSugerido': valor_mes_Louca_escolhidoF,
                    'TempoRetornoValorInvestidoLavaLouca': tempo_em_anos_retorno_LoucaF,
                    'ValorConsumidoNoMesMicroondas': valor_mes_MicroondasF,
                    'ValorConsumidoNoMesMicroondasSugerido': valor_mes_Microondas_escolhidoF,
                    'TempoRetornoValorInvestidoMicroondas': tempo_em_anos_retorno_MicroondasF,
                    'ValorConsumidoNoMesProcessador': valor_mes_ProcessadorF,
                    'ValorConsumidoNoMesProcessadorSugerido': valor_mes_Processador_escolhidoF,
                    'TempoRetornoValorInvestidoProcessador': tempo_em_anos_retorno_ProcessadorF,
                    'ValorConsumidoNoMesPurificador': valor_mes_PurificadorF,
                    'ValorConsumidoNoMesPurificadorSugerido': valor_mes_Purificador_escolhidoF,
                    'TempoRetornoValorInvestidoPurificador': tempo_em_anos_retorno_PurificadorF,
                    'ValorConsumidoNoMesSanduicheira': valor_mes_SanduicheiraF,
                    'ValorConsumidoNoMesSanduicheiraSugerido': valor_mes_Sanduicheira_escolhidoF,
                    'TempoRetornoValorInvestidoSanduicheira': tempo_em_anos_retorno_SanduicheiraF,
                    'ValorConsumidoNoMesTorneira': valor_mes_TorneiraF,
                    'ValorConsumidoNoMesTorneiraSugerido': valor_mes_Torneira_escolhidoF,
                    'TempoRetornoValorInvestidoTorneira': tempo_em_anos_retorno_TorneiraF,
                    'ValorConsumidoNoMesTorradeira': valor_mes_TorradeiraF,
                    'ValorConsumidoNoMesTorradeiraSugerido': valor_mes_Torradeira_escolhidoF,
                    'TempoRetornoValorInvestidoTorradeira': tempo_em_anos_retorno_TorradeiraF,
                    'ValorConsumidoNoMesBarbeador': valor_mes_BarbeadorF,
                    'ValorConsumidoNoMesBarbeadorSugerido': valor_mes_Barbeador_escolhidoF,
                    'TempoRetornoValorInvestidoBarbeador': tempo_em_anos_retorno_BarbeadorF,
                    'ValorConsumidoNoMesChapinha': valor_mes_ChapinhaF,
                    'ValorConsumidoNoMesChapinhaSugerido': valor_mes_Chapinha_escolhidoF,
                    'TempoRetornoValorInvestidoChapinha': tempo_em_anos_retorno_ChapinhaF,
                    'ValorConsumidoNoMesChuveiro': valor_mes_ChuveiroF,
                    'ValorConsumidoNoMesChuveiroSugerido': valor_mes_Chuveiro_escolhidoF,
                    'TempoRetornoValorInvestidoChuveiro': tempo_em_anos_retorno_ChuveiroF,
                    'ValorConsumidoNoMesSecador': valor_mes_SecadorF,
                    'ValorConsumidoNoMesSecadorSugerido': valor_mes_Secador_escolhidoF,
                    'TempoRetornoValorInvestidoSecador': tempo_em_anos_retorno_SecadorF,
                    'ValorConsumidoNoMesEscovaEletrica': valor_mes_EscovaF,
                    'ValorConsumidoNoMesEscovaEletricaSugerido': valor_mes_Escova_escolhidoF,
                    'TempoRetornoValorInvestidoEscovaEletrica': tempo_em_anos_retorno_EscovaF,
                    'ValorConsumidoNoMesBombaDeAgua': valor_mes_BombaF,
                    'ValorConsumidoNoMesBombaDeAguaSugerido': valor_mes_Bomba_escolhidoF,
                    'TempoRetornoValorInvestidoBombaDeAgua': tempo_em_anos_retorno_BombaF,
                    'ValorConsumidoNoMesCercaEletrica': valor_mes_CercaF,
                    'ValorConsumidoNoMesCercaEletricaSugerido': valor_mes_Cerca_escolhidoF,
                    'TempoRetornoValorInvestidoCercaEletrica': tempo_em_anos_retorno_CercaF,
                    'ValorConsumidoNoMesChurrasqueiraEletrica': valor_mes_ChurrasqueiraF,
                    'ValorConsumidoNoMesChurrasqueiraEletricaSugerido': valor_mes_Churrasqueira_escolhidoF,
                    'TempoRetornoValorInvestidoChurrasqueiraEletrica': tempo_em_anos_retorno_ChurrasqueiraF,
                    'ValorConsumidoNoMesCortadorDeGrama': valor_mes_CortadorF,
                    'ValorConsumidoNoMesCortadorDeGramaSugerido': valor_mes_Cortador_escolhidoF,
                    'TempoRetornoValorInvestidoCortadorDeGrama': tempo_em_anos_retorno_CortadorF,
                    'ValorConsumidoNoMesIrrigador': valor_mes_IrrigadorF,
                    'ValorConsumidoNoMesIrrigadorSugerido': valor_mes_Irrigador_escolhidoF,
                    'TempoRetornoValorInvestidoIrrigador': tempo_em_anos_retorno_IrrigadorF}
    return saidaMedio

@app.route('/calculoLongoPrazo', methods=['POST'])
def calculoLongoPrazo():
    body = request.get_json()

    dadosLongo = informeDadosLongo(body["valor_conta_mes"])
    valor_conta_mes = float(dadosLongo["valor_conta_mes"])

    # Média do valor dos painéis solares
    media_kit_paineis = 18753.33
    # Média do preço de instalação
    instalacao_paineis = 1500
    # Soma da instalação com o valor dos painéis
    valor_total_investido = media_kit_paineis + instalacao_paineis
    # Calculando o valor anual gasto hoje pelo usuário
    valor_de_conta_em_1_ano = valor_conta_mes * 12
    # Descobrindo em quanto tempo o usuário terá o retorno do seu investimento
    valor_final = valor_total_investido / valor_de_conta_em_1_ano
    valor_finalF = int(f'''{valor_final:.0f}''')
    saidaLongo = {'TempoDeRetornoInvestido': valor_finalF}

    return saidaLongo


if __name__=="__main__":
    app.run(debug = True)

