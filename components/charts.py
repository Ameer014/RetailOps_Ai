import plotly.express as px


def create_category_chart(df):

    if not {"product_category_name", "price"}.issubset(df.columns):
        return None

    category_sales = (
        df.groupby("product_category_name")["price"]
        .sum()
        .nlargest(10)
        .reset_index()
    )

    fig = px.bar(
        category_sales,
        x="product_category_name",
        y="price",
        title="Top 10 Product Categories by Revenue",
        labels={
            "product_category_name": "Category",
            "price": "Revenue"
        }
    )

    return fig