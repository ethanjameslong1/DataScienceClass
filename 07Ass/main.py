import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
from sklearn.preprocessing import MinMaxScaler, StandardScaler, QuantileTransformer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

source_file = "archive/starbucks_ny_broadway.csv"

try:
    df = pd.read_csv(source_file)
except:
    df = pd.DataFrame(
        {
            "text": ["coffee is great", "slow", "tasty coffee", "bad"] * 200,
            "rating": [5, 2, 4, 1] * 200,
        }
    )

df["mentions_coffee"] = (
    df["text"].str.contains("coffee", case=False, na=False).astype(int)
)


def get_len_category(x):
    length = len(str(x))
    if length < 50:
        return "Short"
    if length < 150:
        return "Medium"
    return "Long"


df["review_length_type"] = df["text"].apply(get_len_category)
df["word_count"] = df["text"].apply(lambda x: len(str(x).split()))

sentiment_map = {1: "Poor", 2: "Poor", 3: "Average", 4: "Great", 5: "Great"}
df["sentiment_label"] = df["rating"].map(sentiment_map)

dummies = pd.get_dummies(df["sentiment_label"], prefix="sent")
df = pd.concat([df, dummies], axis=1)

df["sentiment_count_enc"] = df["sentiment_label"].map(
    df["sentiment_label"].value_counts()
)
df["sentiment_target_enc"] = df["sentiment_label"].map(
    df.groupby("sentiment_label")["word_count"].mean()
)

df = df.dropna().copy()
df = df[df["word_count"] > 0]

df["word_count_minmax"] = MinMaxScaler().fit_transform(df[["word_count"]])
df["word_count_bin_id"] = pd.cut(
    df["word_count"], bins=[0, 20, 100, 100000], labels=[1, 2, 3]
).astype(int)
df["rating_std"] = StandardScaler().fit_transform(df[["rating"]])

n_samples = len(df)
qt = QuantileTransformer(
    output_distribution="uniform", n_quantiles=min(n_samples, 1000)
)
df["word_count_quantile"] = qt.fit_transform(df[["word_count"]])

df["is_great"] = (df["rating"] >= 4).astype(int)
features = ["mentions_coffee", "word_count_quantile", "sentiment_target_enc"]
X = df[features]
y = df["is_great"]

xtrain, xtest, ytrain, ytest = train_test_split(X, y, test_size=0.2, random_state=42)

lr = LogisticRegression().fit(xtrain, ytrain)
acc_lr = accuracy_score(ytest, lr.predict(xtest))

rf = RandomForestClassifier().fit(xtrain, ytrain)
acc_rf = accuracy_score(ytest, rf.predict(xtest))

app = Dash(__name__)

app.layout = html.Div(
    [
        html.H1("Starbucks Broadway Analysis Dashboard"),
        html.Div(
            f"LogReg Accuracy: {acc_lr:.2%}, RF Accuracy: {acc_rf:.2%}",
            style={"color": "navy", "fontWeight": "bold"},
        ),
        html.Hr(),
        html.Div(
            [
                html.H3("Feature Correlation Explorer"),
                dcc.Dropdown(
                    id="dropdown-selection",
                    options=[
                        {"label": c, "value": c}
                        for c in [
                            "rating",
                            "word_count",
                            "word_count_bin_id",
                            "sentiment_target_enc",
                        ]
                    ],
                    value=["rating", "word_count", "sentiment_target_enc"],
                    multi=True,
                ),
                dcc.Graph(id="heatmap-graph"),
            ]
        ),
        html.Div(
            [
                html.H3("Rating vs. Review Depth"),
                dcc.Checklist(
                    id="scatter-check",
                    options=[{"label": "Show Trendline", "value": "trend"}],
                    value=["trend"],
                ),
                dcc.Graph(id="scatter-graph"),
            ]
        ),
        html.Div(
            [
                html.H3("Distribution by Word Count Range"),
                dcc.RangeSlider(
                    id="range-slider",
                    min=df["word_count"].min(),
                    max=df["word_count"].max(),
                    value=[df["word_count"].min(), df["word_count"].max()],
                    step=1,
                    marks={
                        i: str(i) for i in range(0, int(df["word_count"].max()), 50)
                    },
                ),
                dcc.Graph(id="bubble-graph"),
            ]
        ),
        html.Div(
            [
                html.H3("Classification Model Tester"),
                html.Div(
                    [
                        html.Span("Word Count: "),
                        dcc.Input(id="input-wc", type="number", value=30),
                        html.Span(" Mentions Coffee: ", style={"marginLeft": "20px"}),
                        dcc.RadioItems(
                            id="input-cf",
                            options=[
                                {"label": " Yes ", "value": 1},
                                {"label": " No ", "value": 0},
                            ],
                            value=1,
                            inline=True,
                            style={"display": "inline-block"},
                        ),
                    ],
                    style={"marginBottom": "20px"},
                ),
                dcc.Graph(id="prediction-graph", style={"marginTop": "15px"}),
            ],
            style={"paddingBottom": "50px"},
        ),
    ]
)


@app.callback(Output("heatmap-graph", "figure"), Input("dropdown-selection", "value"))
def update_heatmap(cols):
    if not cols:
        return go.Figure()

    c_matrix = df[cols].corr()
    return go.Figure(
        data=go.Heatmap(
            z=c_matrix.values,
            x=c_matrix.columns,
            y=c_matrix.columns,
            colorscale="Viridis",
            text=np.round(c_matrix.values, 2),
            texttemplate="%{text}",
        )
    )


@app.callback(Output("scatter-graph", "figure"), Input("scatter-check", "value"))
def update_scatter(check):
    mode = "ols" if "trend" in check else None
    fig = px.scatter(
        df,
        x="rating",
        y="word_count",
        trendline=mode,
        color_discrete_sequence=["navy"],
    )
    fig.update_traces(marker=dict(size=10))
    return fig


@app.callback(Output("bubble-graph", "figure"), Input("range-slider", "value"))
def update_bubble(rng):
    filtered = df[(df["word_count"] >= rng[0]) & (df["word_count"] <= rng[1])]
    return px.scatter(
        filtered,
        x="rating",
        y="word_count",
        size="word_count_quantile",
        color="sentiment_label",
        color_discrete_map={"Great": "green", "Poor": "pink", "Average": "orange"},
    )


@app.callback(
    Output("prediction-graph", "figure"),
    Input("input-wc", "value"),
    Input("input-cf", "value"),
)
def update_prediction(wc, cf):
    wc = wc or 0

    test_pt = pd.DataFrame(
        [[cf, wc / df["word_count"].max(), df["sentiment_target_enc"].mean()]],
        columns=features,
    )

    prob = rf.predict_proba(test_pt)[0][1]

    return go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=prob * 100,
            title={"text": "Probability of 'Great' Experience (%)"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "green" if prob > 0.5 else "red"},
            },
        )
    )


if __name__ == "__main__":
    app.run(debug=True)
