from datetime import date

from fastapi import HTTPException

from src.schemas import CotarSeguroPayload, CotarSeguroResponse
from src.service import cotar_seguro_service


def test_cotar_seguro_service_vigencia_maior_que_1_ano():
    cotacao = CotarSeguroPayload(
        nome="Teste",
        cpf="12345678901",
        email="teste@teste.com",
        dt_inicio_vigencia=date(2021, 1, 1),
        dt_fim_vigencia=date(2022, 12, 31),
        idade=18,
        vl_importancia_segurada=10000,
        genero_biologico="M",
    )
    try:
        cotar_seguro_service(cotacao)
        assert False
    except HTTPException as e:
        assert e.status_code == 400
        assert e.detail == "Vigencia maxima de 1 ano"


def test_cotar_seguro_service_idade_menor_que_18():
    cotacao = CotarSeguroPayload(
        nome="Teste",
        cpf="12345678901",
        email="teste@teste.com",
        dt_inicio_vigencia=date(2021, 1, 1),
        dt_fim_vigencia=date(2021, 12, 31),
        idade=17,
        vl_importancia_segurada=10000,
        genero_biologico="M",
    )
    try:
        cotar_seguro_service(cotacao)
        assert False
    except HTTPException as e:
        assert e.status_code == 400
        assert e.detail == "Idade minima de 18 anos"


def test_cotar_seguro_service_idade_maior_que_65():
    cotacao = CotarSeguroPayload(
        dt_inicio_vigencia=date(2021, 1, 1),
        dt_fim_vigencia=date(2021, 12, 31),
        idade=66,
        vl_importancia_segurada=10000,
        genero_biologico="M",
        nome="Teste",
        cpf="12345678901",
        email="aaaaaa@gmail.com",
    )
    try:
        cotar_seguro_service(cotacao)
        assert False
    except HTTPException as e:
        assert e.status_code == 400
        assert e.detail == "Idade maxima de 65 anos"


def test_cotar_seguro_service_vl_importancia_segurada_menor_que_10_mil():
    cotacao = CotarSeguroPayload(
        dt_inicio_vigencia=date(2021, 1, 1),
        dt_fim_vigencia=date(2021, 12, 31),
        idade=18,
        vl_importancia_segurada=9999,
        genero_biologico="M",
        nome="Teste",
        cpf="12345678901",
        email="aaaaaa@gmail.com",
    )
    try:
        cotar_seguro_service(cotacao)
        assert False
    except HTTPException as e:
        assert e.status_code == 400
        assert e.detail == "Valor minimo de 10 mil reais"


def test_cotar_seguro_service_vl_importancia_segurada_maior_que_1_milhao():
    cotacao = CotarSeguroPayload(
        dt_inicio_vigencia=date(2021, 1, 1),
        dt_fim_vigencia=date(2021, 12, 31),
        idade=18,
        vl_importancia_segurada=1000001,
        genero_biologico="M",
        nome="Teste",
        cpf="12345678901",
        email="aaaaa@gmail.com",
    )
    try:
        cotar_seguro_service(cotacao)
        assert False
    except HTTPException as e:
        assert e.status_code == 400
        assert e.detail == "Valor maximo de 1 milhao de reais"


def test_cotar_seguro_service_genero_biologico_feminino():
    cotacao = CotarSeguroPayload(
        dt_inicio_vigencia=date(2021, 1, 1),
        dt_fim_vigencia=date(2021, 12, 31),
        idade=18,
        vl_importancia_segurada=10000,
        genero_biologico="F",
        nome="Teste",
        cpf="12345678901",
        email="aaaa@gmail.com",
    )
    result = cotar_seguro_service(cotacao)
    assert result.vl_premio_bruto == 52
    assert result.vl_iof == 2
    assert result.vl_corretagem == 5
    assert result.vl_premio_liquido == 45


def test_cotar_seguro_service_genero_biologico_masculino():
    cotacao = CotarSeguroPayload(
        dt_inicio_vigencia=date(2023, 1, 11),
        dt_fim_vigencia=date(2023, 12, 11),
        idade=18,
        vl_importancia_segurada=100000,
        genero_biologico="M",
        nome="Teste",
        cpf="12345678901",
        email="aaa@gmail.com",
    )
    result = cotar_seguro_service(cotacao)
    assert result.vl_premio_bruto == 601
    assert result.vl_iof == 30
    assert result.vl_corretagem == 60
    assert result.vl_premio_liquido == 511
