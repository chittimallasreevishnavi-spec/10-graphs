import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Dataset Visualization Dashboard", layout="wide")

st.title("📊 Universal Dataset Visualization Dashboard")
st.write("Upload any CSV dataset and visualize it with 10 different graph types.")

uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    columns = df.columns.tolist()
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()

    graph_type = st.selectbox(
        "Select Graph Type",
        [
            "Line Chart",
            "Bar Chart",
            "Scatter Plot",
            "Histogram",
            "Box Plot",
            "Pie Chart",
            "Heatmap",
            "Area Chart",
            "Violin Plot",
            "Pair Plot"
        ]
    )

    if graph_type == "Pair Plot":
        if len(numeric_cols) >= 2:
            fig = sns.pairplot(df[numeric_cols])
            st.pyplot(fig)
        else:
            st.warning("Need at least 2 numeric columns.")
    else:

        x_axis = st.selectbox("Select X-axis", columns)

        if graph_type != "Pie Chart":
            y_axis = st.selectbox(
                "Select Y-axis",
                numeric_cols if numeric_cols else columns
            )

        fig, ax = plt.subplots(figsize=(10, 6))

        if graph_type == "Line Chart":
            ax.plot(df[x_axis], df[y_axis])
            ax.set_title("Line Chart")

        elif graph_type == "Bar Chart":
            ax.bar(df[x_axis], df[y_axis])
            ax.set_title("Bar Chart")
            plt.xticks(rotation=45)

        elif graph_type == "Scatter Plot":
            ax.scatter(df[x_axis], df[y_axis])
            ax.set_title("Scatter Plot")

        elif graph_type == "Histogram":
            ax.hist(df[y_axis], bins=20)
            ax.set_title("Histogram")

        elif graph_type == "Box Plot":
            sns.boxplot(y=df[y_axis], ax=ax)
            ax.set_title("Box Plot")

        elif graph_type == "Pie Chart":
            pie_col = st.selectbox("Select Column", columns)
            value_counts = df[pie_col].value_counts()
            ax.pie(
                value_counts.values,
                labels=value_counts.index,
                autopct="%1.1f%%"
            )
            ax.set_title("Pie Chart")

        elif graph_type == "Heatmap":
            corr = df[numeric_cols].corr()
            sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
            ax.set_title("Correlation Heatmap")

        elif graph_type == "Area Chart":
            ax.fill_between(
                range(len(df)),
                df[y_axis],
                alpha=0.5
            )
            ax.set_title("Area Chart")

        elif graph_type == "Violin Plot":
            sns.violinplot(y=df[y_axis], ax=ax)
            ax.set_title("Violin Plot")

        st.pyplot(fig)

    st.subheader("Dataset Statistics")
    st.write(df.describe())

else:
    st.info("Please upload a CSV file.")
    