from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

file = r"cs_students.csv"
df = pd.read_csv(file)

dfGPA = df["GPA"]
figGpaViolin = go.Figure(
    data=go.Violin(
        y=dfGPA,
        box_visible=True,
        line_color="black",
        meanline_visible=True,
        fillcolor="lightseagreen",
        opacity=0.6,
        x0="GPA Distribution",
    )
)

dfBoxPlot = df["Age"]
figAgeBoxPlot = go.Figure()
figAgeBoxPlot.add_trace(
    go.Box(y=dfBoxPlot, name="Age of students", marker_color="seagreen")
)

dfHistogram = df["Gender"]
figHistogram = px.histogram(
    dfHistogram,
    x="Gender",
    title="Distribution of Gender",
)

dfProjects = df["Projects"]
figProjectsViolin = go.Figure(
    data=go.Violin(
        y=dfProjects,
        box_visible=True,
        line_color="black",
        meanline_visible=True,
        fillcolor="orchid",
        opacity=0.6,
        x0="Projects Distribution",
    )
)

dfPythonHist = df["Python"]
figPythonHistogram = px.histogram(
    dfPythonHist,
    x="Python",
    title="Distribution of Python Scores",
    color_discrete_sequence=["indianred"],
)

dfDomainHist = df["Interested Domain"]
figDomainHistogram = px.histogram(
    dfDomainHist,
    x="Interested Domain",
    title="Distribution of Interested Domains",
    color_discrete_sequence=["goldenrod"],
)

app = Dash(__name__)

box_style = {
    "margin": "10px",
    "text-align": "center",
    "border": "1px solid #ddd",
    "padding": "10px",
}

app.layout = html.Div(
    [
        html.H1(
            children="CS Student Dashboard",
        ),
        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "1fr 1fr",
                "gap": "20px",
                "padding": "20px",
            },
            children=[
                # Row 1
                html.Div(
                    children=[
                        html.H2("Violin Plot of GPA's", style={"textAlign": "center"}),
                        dcc.Graph(id="Graph1", figure=figGpaViolin),
                    ],
                    style=box_style,
                ),
                html.Div(
                    children=[
                        html.H2(
                            "Violin Plot of Projects", style={"textAlign": "center"}
                        ),
                        dcc.Graph(id="Graph2", figure=figProjectsViolin),
                    ],
                    style=box_style,
                ),
                # Row 2
                html.Div(
                    children=[
                        html.H2("Box Plot of Ages", style={"textAlign": "center"}),
                        dcc.Graph(id="Graph3", figure=figAgeBoxPlot),
                    ],
                    style=box_style,
                ),
                html.Div(
                    children=[
                        html.H2(
                            "Histogram of Python Scores", style={"textAlign": "center"}
                        ),
                        dcc.Graph(id="Graph4", figure=figPythonHistogram),
                    ],
                    style=box_style,
                ),
                # Row 3
                html.Div(
                    children=[
                        html.H2("Histogram of Genders", style={"textAlign": "center"}),
                        dcc.Graph(id="Graph5", figure=figHistogram),
                    ],
                    style=box_style,
                ),
                html.Div(
                    children=[
                        html.H2("Histogram of Domains", style={"textAlign": "center"}),
                        dcc.Graph(id="Graph6", figure=figDomainHistogram),
                    ],
                    style=box_style,
                ),
            ],
        ),
    ]
)

if __name__ == "__main__":
    app.run(debug=True)

