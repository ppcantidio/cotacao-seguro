from fastapi import HTTPException

from src.schemas import CotarSeguroPayload, CotarSeguroResponse


def cotar_seguro_service(request: CotarSeguroPayload):
    tempo_total_vigencia = request.dt_fim_vigencia - request.dt_inicio_vigencia
    if tempo_total_vigencia.days > 365:
        raise HTTPException(status_code=400, detail="Vigencia maxima de 1 ano")

    if request.idade < 18:
        raise HTTPException(status_code=400, detail="Idade minima de 18 anos")

    if request.idade > 65:
        raise HTTPException(status_code=400, detail="Idade maxima de 65 anos")

    if request.vl_importancia_segurada < 10000:
        raise HTTPException(status_code=400, detail="Valor minimo de 10 mil reais")

    if request.vl_importancia_segurada > 1000000:
        raise HTTPException(status_code=400, detail="Valor maximo de 1 milhao de reais")

    if request.genero_biologico == "M":
        valor_bruto = int(
            request.vl_importancia_segurada
            * 0.0000010
            * request.idade
            * tempo_total_vigencia.days
        )

    if request.genero_biologico == "F":
        valor_bruto = int(
            request.vl_importancia_segurada
            * 0.0000008
            * request.idade
            * tempo_total_vigencia.days
        )

    vl_iof = int(valor_bruto * 0.05)
    vl_corretagem = int(valor_bruto * 0.10)
    vl_liquido = int(valor_bruto - vl_iof - vl_corretagem)

    response = CotarSeguroResponse(
        vl_premio_bruto=valor_bruto,
        vl_iof=vl_iof,
        vl_corretagem=vl_corretagem,
        vl_premio_liquido=vl_liquido,
    )
    return response
