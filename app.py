from pathlib import Path
import streamlit as st
from src.db import consultar

st.set_page_config(
    page_title="Brasa & Pão",
    page_icon="🍔",
    layout="wide"
)

BASE_DIR = Path(__file__).parent
IMAGEM = BASE_DIR / "banner_brasa_pao.png"

st.image(str(IMAGEM), use_container_width=True)

st.write("Consultas do banco de dados")



consultas = {

    "Q1 - Clientes do bairro Centro": """
        SELECT COUNT(*) AS QuantidadeClientes
        FROM Clientes
        WHERE Bairro = 'Centro';
    """,

    "Q2 - Hambúrgueres acima de R$ 30": """
        SELECT
            NomeProduto,
            Preco
        FROM Produtos
        WHERE Categoria = 'Hambúrguer'
          AND Preco > 30
        ORDER BY Preco DESC;
    """,

    "Q3 - Pedidos entregues e cancelados": """
        SELECT
            Status,
            COUNT(*) AS Quantidade
        FROM Pedidos
        WHERE Status IN ('Entregue', 'Cancelado')
        GROUP BY Status;
    """,

    "Q4 - Avaliação dos pedidos entregues": """
        SELECT
            COUNT(*) AS TotalPedidosEntregues,
            COUNT(Avaliacao) AS PedidosAvaliados,
            COUNT(*) - COUNT(Avaliacao) AS PedidosSemAvaliacao,
            AVG(CAST(Avaliacao AS DECIMAL(4,2))) AS NotaMedia
        FROM Pedidos
        WHERE Status = 'Entregue';
    """,

    "Q5 - Delivery x Retirada": """
        SELECT
            MONTH(DataPedido) AS Mes,
            TipoEntrega,
            COUNT(*) AS QuantidadePedidos
        FROM Pedidos
        WHERE Status = 'Entregue'
        GROUP BY
            MONTH(DataPedido),
            TipoEntrega
        ORDER BY
            MONTH(DataPedido),
            TipoEntrega;
    """,

    "Q6 - Pedidos de janeiro de 2026": """
        SELECT
            p.IdPedido,
            p.DataPedido,
            c.Nome,
            c.Bairro,
            p.Status
        FROM dbo.Pedidos AS p
        INNER JOIN dbo.Clientes AS c
            ON p.IdCliente = c.IdCliente
        WHERE p.DataPedido >= '2026-01-01'
          AND p.DataPedido < '2026-02-01'
        ORDER BY p.DataPedido ASC;
    """,

    "Q7 - Entregas por entregador": """
        SELECT
            IdEntregador,
            COUNT(*) AS QuantidadeEntregas
        FROM dbo.Pedidos
        WHERE Status = 'Entregue'
        GROUP BY IdEntregador
        ORDER BY QuantidadeEntregas DESC;
    """,

    "Q8 - Produtos vendidos e faturamento": """
        SELECT
            pr.NomeProduto,
            SUM(ip.Quantidade) AS UnidadesVendidas,
            SUM(ip.Quantidade * ip.PrecoUnitario) AS Faturamento
        FROM dbo.ItensPedido AS ip
        INNER JOIN dbo.Produtos AS pr
            ON ip.IdProduto = pr.IdProduto
        INNER JOIN dbo.Pedidos AS p
            ON ip.IdPedido = p.IdPedido
        WHERE p.Status = 'Entregue'
        GROUP BY pr.NomeProduto
        ORDER BY UnidadesVendidas DESC;
    """,

    "Q9 - Faturamento por categoria": """
        SELECT
            p.Categoria,
            SUM(ip.Quantidade * ip.PrecoUnitario) AS Faturamento
        FROM dbo.ItensPedido AS ip
        INNER JOIN dbo.Produtos AS p
            ON ip.IdProduto = p.IdProduto
        GROUP BY p.Categoria
        ORDER BY Faturamento DESC;
    """,

    "Q10 - Bairros com pelo menos 7 pedidos": """
        SELECT
            c.Bairro,
            COUNT(*) AS QuantidadePedidos
        FROM dbo.Pedidos AS p
        INNER JOIN dbo.Clientes AS c
            ON p.IdCliente = c.IdCliente
        WHERE p.Status = 'Entregue'
        GROUP BY c.Bairro
        HAVING COUNT(*) >= 7;
    """,

    "Q11 - Preços do X-Bacon": """
        SELECT
            ip.PrecoUnitario,
            SUM(ip.Quantidade) AS UnidadesVendidas,
            SUM(ip.Quantidade * ip.PrecoUnitario) AS Faturamento
        FROM dbo.ItensPedido AS ip
        INNER JOIN dbo.Produtos AS p
            ON ip.IdProduto = p.IdProduto
        WHERE p.NomeProduto = 'X-Bacon'
        GROUP BY ip.PrecoUnitario
        ORDER BY ip.PrecoUnitario;
    """,

    "Q12 - 3 clientes que mais gastaram": """
        SELECT TOP 3
            c.Nome,
            COUNT(DISTINCT p.IdPedido) AS QuantidadePedidos,
            SUM(ip.Quantidade * ip.PrecoUnitario) AS TotalGasto
        FROM dbo.Clientes AS c
        INNER JOIN dbo.Pedidos AS p
            ON c.IdCliente = p.IdCliente
        INNER JOIN dbo.ItensPedido AS ip
            ON p.IdPedido = ip.IdPedido
        GROUP BY c.Nome
        ORDER BY TotalGasto DESC;
    """,

    "Q13 - Faturamento por mês": """
        SELECT
            MONTH(p.DataPedido) AS Mes,
            COUNT(DISTINCT p.IdPedido) AS QuantidadePedidos,
            SUM(ip.Quantidade * ip.PrecoUnitario) AS Faturamento
        FROM dbo.Pedidos AS p
        INNER JOIN dbo.ItensPedido AS ip
            ON p.IdPedido = ip.IdPedido
        WHERE p.Status = 'Entregue'
        GROUP BY MONTH(p.DataPedido)
        ORDER BY Mes;
    """,

    "Q14 - Melhores entregadores": """
        SELECT
            IdEntregador,
            COUNT(*) AS Entregas,
            AVG(CAST(Avaliacao AS DECIMAL(4,2))) AS NotaMedia
        FROM dbo.Pedidos
        WHERE Status = 'Entregue'
        GROUP BY IdEntregador
        HAVING COUNT(*) >= 4
           AND AVG(CAST(Avaliacao AS DECIMAL(4,2))) >= 4
        ORDER BY NotaMedia DESC;
    """,

    "Q15 - Pedidos de março": """
        SELECT
            p.IdPedido,
            c.Nome,
            SUM(ip.Quantidade * ip.PrecoUnitario)
                + p.TaxaEntrega AS ValorTotal
        FROM dbo.Pedidos AS p
        INNER JOIN dbo.Clientes AS c
            ON p.IdCliente = c.IdCliente
        INNER JOIN dbo.ItensPedido AS ip
            ON p.IdPedido = ip.IdPedido
        WHERE p.Status = 'Entregue'
          AND MONTH(p.DataPedido) = 3
        GROUP BY
            p.IdPedido,
            c.Nome,
            p.TaxaEntrega
        ORDER BY ValorTotal DESC;
    """,

    "Q16 - Clientes sem pedidos": """
        SELECT
            c.Nome,
            c.Bairro
        FROM dbo.Clientes AS c
        LEFT JOIN dbo.Pedidos AS p
            ON c.IdCliente = p.IdCliente
        WHERE p.IdPedido IS NULL;
    """,

    "Q17 - Produtos nunca vendidos": """
        SELECT
            p.NomeProduto
        FROM dbo.Produtos AS p
        LEFT JOIN dbo.ItensPedido AS ip
            ON p.IdProduto = ip.IdProduto
        WHERE ip.IdProduto IS NULL;
    """
}


st.sidebar.header("📋 Consultas")

questao = st.sidebar.selectbox(
    "Escolha uma questão:",
    list(consultas.keys())
)



st.subheader(questao)

sql = consultas[questao]

with st.expander("🔎 Ver consulta SQL"):
    st.code(sql, language="sql")


try:

    resultado = consultar(sql)

    st.dataframe(
        resultado,
        use_container_width=True,
        hide_index=True
    )

except Exception as erro:

    st.error("❌ Erro ao executar a consulta.")

    st.code(str(erro))