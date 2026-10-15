"""Gera as imagens SVG do README (versões clara e escura).

Para mudar cores ou textos, edite TEMAS / PROJETOS e rode:
    python scripts/gerar_svgs.py
"""
from pathlib import Path

SAIDA = Path(__file__).resolve().parents[1] / "assets"
FONTE = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, monospace"

# Paleta suave: sálvia, lavanda e pêssego sobre fundo neutro.
TEMAS = {
    "light": {
        "fundo_a": "#F4F1F8", "fundo_b": "#EDF4EF", "card": "#FBFAF8", "borda": "#E6E2DC",
        "texto": "#3B4250", "texto_suave": "#6E7480", "linha": "#CFCAD8",
        "salvia": "#9DBFAE", "lavanda": "#B7AEDB", "pessego": "#EDB99A",
        "salvia_bg": "#E3EFE8", "lavanda_bg": "#ECE8F7", "pessego_bg": "#FBEADF",
    },
    "dark": {
        "fundo_a": "#22212B", "fundo_b": "#1F2725", "card": "#1C2026", "borda": "#30353D",
        "texto": "#E7E9ED", "texto_suave": "#A4AAB4", "linha": "#454356",
        "salvia": "#8DB4A1", "lavanda": "#A99FD3", "pessego": "#E2A988",
        "salvia_bg": "#26332D", "lavanda_bg": "#2C2A3B", "pessego_bg": "#3A2D26",
    },
}

PROJETOS = [
    {
        "arquivo": "projeto-1", "numero": "01", "cor": "salvia",
        "nome": "fuel-price-warehouse",
        "pergunta": "Onde e quanto o combustível pesa no custo da frota?",
        "descricao": "Data warehouse em star schema com os preços da ANP e 5 análises SQL.",
        "stack": ["SQL", "PostgreSQL", "Modelagem dimensional", "Docker"],
    },
    {
        "arquivo": "projeto-2", "numero": "02", "cor": "lavanda",
        "nome": "economic-indicators-etl",
        "pergunta": "Como manter IPCA, Selic e dólar sempre atualizados e confiáveis?",
        "descricao": "ETL incremental e idempotente da API do Banco Central, com testes.",
        "stack": ["Python", "Pandas", "pytest", "CI"],
    },
    {
        "arquivo": "projeto-3", "numero": "03", "cor": "pessego",
        "nome": "fleet-cost-pipeline",
        "pergunta": "O combustível subiu de verdade ou só acompanhou a inflação?",
        "descricao": "Airflow orquestra os dois projetos e publica um índice de preço real.",
        "stack": ["Airflow", "Assets", "SQL", "Docker"],
    },
]


def pill(x, y, texto, bg, fg, tamanho=12):
    largura = int(len(texto) * tamanho * 0.62) + 22
    return largura, (
        f'<rect x="{x}" y="{y}" width="{largura}" height="24" rx="12" fill="{bg}"/>'
        f'<text x="{x + largura / 2}" y="{y + 16.5}" font-size="{tamanho}" fill="{fg}" '
        f'text-anchor="middle" font-family="{FONTE}">{texto}</text>'
    )


def svg(largura, altura, corpo, titulo):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{largura}" height="{altura}" '
        f'viewBox="0 0 {largura} {altura}" role="img" aria-label="{titulo}">'
        f"<title>{titulo}</title>{corpo}</svg>\n"
    )


def cabecalho(t):
    w, h = 830, 210
    corpo = [
        '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="{t["fundo_a"]}"/><stop offset="1" stop-color="{t["fundo_b"]}"/>'
        "</linearGradient></defs>",
        f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="18" fill="url(#g)" stroke="{t["borda"]}"/>',
        f'<text x="40" y="78" font-size="38" font-weight="600" fill="{t["texto"]}" font-family="{FONTE}">Gustavo Cabral</text>',
        f'<text x="40" y="112" font-size="17" fill="{t["texto_suave"]}" font-family="{FONTE}">'
        f'Analista de Dados <tspan fill="{t["lavanda"]}">→</tspan> Engenharia de Dados</text>',
    ]
    x = 40
    for texto, cor in [("SQL", "salvia"), ("Python", "lavanda"), ("Airflow", "pessego"), ("PostgreSQL", "salvia")]:
        largura, el = pill(x, 140, texto, t[f"{cor}_bg"], t["texto"])
        corpo.append(el)
        x += largura + 8

    # Ilustração: um pequeno pipeline (fontes -> transformação -> destino)
    cx = [560, 650, 740]
    cores = ["salvia", "lavanda", "pessego"]
    rotulos = ["ingestão", "modelagem", "orquestração"]
    corpo.append(
        f'<path d="M{cx[0]} 95 L{cx[2]} 95" stroke="{t["linha"]}" stroke-width="2" stroke-dasharray="4 6"/>'
    )
    for c, cor, rotulo in zip(cx, cores, rotulos):
        corpo.append(f'<circle cx="{c}" cy="95" r="26" fill="{t[f"{cor}_bg"]}" stroke="{t[cor]}" stroke-width="2"/>')
        corpo.append(f'<circle cx="{c}" cy="95" r="7" fill="{t[cor]}"/>')
        corpo.append(
            f'<text x="{c}" y="146" font-size="12" fill="{t["texto_suave"]}" text-anchor="middle" '
            f'font-family="{FONTE}">{rotulo}</text>'
        )
    return svg(w, h, "".join(corpo), "Gustavo Cabral, Analista de Dados em transição para Engenharia de Dados")


def mapa(t):
    """Os 3 projetos como um pipeline: é a história do portfólio numa imagem."""
    w, h = 830, 200
    corpo = [f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="18" fill="{t["card"]}" stroke="{t["borda"]}"/>']

    def caixa(x, y, larg, alt, titulo, sub, cor, mono=False):
        fam = MONO if mono else FONTE
        return (
            f'<rect x="{x}" y="{y}" width="{larg}" height="{alt}" rx="12" fill="{t[f"{cor}_bg"]}" stroke="{t[cor]}"/>'
            f'<text x="{x + larg / 2}" y="{y + alt / 2 - 2}" font-size="13" font-weight="600" fill="{t["texto"]}" '
            f'text-anchor="middle" font-family="{fam}">{titulo}</text>'
            f'<text x="{x + larg / 2}" y="{y + alt / 2 + 16}" font-size="11" fill="{t["texto_suave"]}" '
            f'text-anchor="middle" font-family="{FONTE}">{sub}</text>'
        )

    def seta(x1, y1, x2, y2):
        return (
            f'<path d="M{x1} {y1} C{(x1 + x2) / 2} {y1}, {(x1 + x2) / 2} {y2}, {x2} {y2}" fill="none" '
            f'stroke="{t["linha"]}" stroke-width="2"/>'
            f'<circle cx="{x2}" cy="{y2}" r="3.5" fill="{t["linha"]}"/>'
        )

    corpo += [
        caixa(28, 34, 120, 54, "ANP", "preços dos postos", "salvia"),
        caixa(28, 112, 120, 54, "Banco Central", "IPCA · Selic · dólar", "lavanda"),
        seta(148, 61, 196, 61), seta(148, 139, 196, 139),
        caixa(196, 34, 200, 54, "fuel-price-warehouse", "SQL · star schema", "salvia", mono=True),
        caixa(196, 112, 200, 54, "economic-indicators-etl", "Python · ETL incremental", "lavanda", mono=True),
        seta(396, 61, 440, 100), seta(396, 139, 440, 100),
        caixa(440, 73, 190, 54, "fleet-cost-pipeline", "Airflow · orquestração", "pessego", mono=True),
        seta(630, 100, 668, 100),
        caixa(668, 73, 136, 54, "Índice de custo", "preço real da frota", "pessego"),
    ]
    return svg(w, h, "".join(corpo), "Mapa do portfólio: fontes públicas, três projetos e o índice de custo de frota")


def card(t, p):
    w, h = 830, 150
    cor = p["cor"]
    corpo = [
        f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="16" fill="{t["card"]}" stroke="{t["borda"]}"/>',
        f'<clipPath id="c"><rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="16"/></clipPath>',
        f'<rect x="0" y="0" width="8" height="{h}" fill="{t[cor]}" clip-path="url(#c)"/>',
        f'<circle cx="62" cy="60" r="30" fill="{t[f"{cor}_bg"]}"/>',
        f'<text x="62" y="68" font-size="22" font-weight="600" fill="{t[cor]}" text-anchor="middle" '
        f'font-family="{MONO}">{p["numero"]}</text>',
        f'<text x="115" y="42" font-size="20" font-weight="600" fill="{t["texto"]}" font-family="{MONO}">{p["nome"]}</text>',
        f'<text x="115" y="70" font-size="15" font-style="italic" fill="{t["texto"]}" font-family="{FONTE}">'
        f'“{p["pergunta"]}”</text>',
        f'<text x="115" y="93" font-size="13" fill="{t["texto_suave"]}" font-family="{FONTE}">{p["descricao"]}</text>',
        f'<text x="{w - 28}" y="42" font-size="13" fill="{t["texto_suave"]}" text-anchor="end" font-family="{FONTE}">ver projeto <tspan fill="{t[cor]}">→</tspan></text>',
    ]
    x = 115
    for item in p["stack"]:
        largura, el = pill(x, 110, item, t[f"{cor}_bg"], t["texto"], tamanho=11)
        corpo.append(el)
        x += largura + 6
    return svg(w, h, "".join(corpo), f'{p["nome"]}: {p["pergunta"]}')


STACK = [
    ("Linguagens", "salvia", ["SQL", "Python"]),
    ("Dados", "lavanda", ["PostgreSQL", "Pandas", "Databricks", "Modelagem dimensional"]),
    ("Engenharia", "pessego", ["Airflow", "Docker", "pytest"]),
    ("Versionamento", "lavanda", ["Git", "GitHub", "GitHub Actions"]),
    ("BI", "salvia", ["Power BI", "Excel avançado"]),
]


def stack(t):
    w, linha = 830, 44
    h = 36 + linha * len(STACK)
    corpo = [f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="16" fill="{t["card"]}" stroke="{t["borda"]}"/>']
    for i, (grupo, cor, itens) in enumerate(STACK):
        y = 24 + i * linha
        corpo.append(f'<circle cx="34" cy="{y + 12}" r="5" fill="{t[cor]}"/>')
        corpo.append(
            f'<text x="48" y="{y + 17}" font-size="14" font-weight="600" fill="{t["texto"]}" '
            f'font-family="{FONTE}">{grupo}</text>'
        )
        x = 170
        for item in itens:
            largura, el = pill(x, y, item, t[f"{cor}_bg"], t["texto"], tamanho=12)
            corpo.append(el)
            x += largura + 8
    return svg(w, h, "".join(corpo), "Ferramentas: " + ", ".join(i for _, _, itens in STACK for i in itens))


def main():
    SAIDA.mkdir(exist_ok=True)
    for nome, t in TEMAS.items():
        (SAIDA / f"header-{nome}.svg").write_text(cabecalho(t), encoding="utf-8")
        (SAIDA / f"stack-{nome}.svg").write_text(stack(t), encoding="utf-8")
        (SAIDA / f"mapa-{nome}.svg").write_text(mapa(t), encoding="utf-8")
        for p in PROJETOS:
            (SAIDA / f'{p["arquivo"]}-{nome}.svg').write_text(card(t, p), encoding="utf-8")
    print(f"SVGs gerados em {SAIDA}")


if __name__ == "__main__":
    main()
