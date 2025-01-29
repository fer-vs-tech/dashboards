import networkx as nx
import pandas as pd
import plotly.graph_objs as go

import cm_dashboards.alchemy_db as db

node_type_colour = {
    "projected data source": "Grey",
    "assumption set": "Grey",
    "program": "Green",
    "data process": "Blue",
    "RuntimeParameters": "Grey",
    "model": "LightSkyBlue",
    "projected data process": "Yellow",
    "data source": "Grey",
    "projection process": "Yellow",
    "stochastic process": "Grey",
}


def do_positioning_calc(G):
    """
    Calculate path distances to decide on tree layout
    """
    positioning = pd.DataFrame(index=G.nodes(), columns=G.nodes())
    for row, data in nx.shortest_path_length(G):
        for col, dist in data.items():
            positioning.loc[row, col] = dist

    return positioning.fillna(positioning.max().max())


def network_graph(schema, execution_id, db_url):
    """
    Construct network graph of model components
    """
    node1 = None
    edge1 = None
    if execution_id:
        # Get nodes from components
        node_query = 'select "ComponentID", "Name", "Type" from "T_Components" where "ExecutionID" = {0}'.format(
            execution_id
        )
        # Get edges from parent-child relationships
        edge_query = 'select "ParentID", "ComponentID" from "T_Components" where "ExecutionID" = {0}'.format(
            execution_id
        )

        if schema:
            node_query = 'select "ComponentID", "Name", "Type" from "{0}"."T_Components" where "ExecutionID" = {1}'.format(
                schema, execution_id
            )
            edge_query = 'select "ParentID", "ComponentID" from "{0}"."T_Components" where "ExecutionID" = {1}'.format(
                schema, execution_id
            )
        else:
            schema = "public"

        node1 = db.query_to_dataframe(db.get_db_connection(db_url), node_query)
        edge1 = db.query_to_dataframe(db.get_db_connection(db_url), edge_query).fillna(
            0
        )
    else:
        node1 = pd.DataFrame(columns=["ComponentID", "Name", "Type"])
        edge1 = pd.DataFrame(columns=["ParentID", "ComponentID"])

    G = nx.from_pandas_edgelist(
        edge1,
        "ComponentID",
        "ParentID",
        create_using=nx.DiGraph(),
    )
    print(node1)
    nx.set_node_attributes(G, node1.set_index("ComponentID")["Name"].to_dict(), "Name")
    nx.set_node_attributes(G, node1.set_index("ComponentID")["Type"].to_dict(), "Type")

    positioning = do_positioning_calc(G)

    pos = nx.layout.kamada_kawai_layout(G, dist=positioning.to_dict())

    for node in G.nodes:
        G.nodes[node]["pos"] = list(pos[node])
        G.nodes[node]["ComponentID"] = node

    traceRecode = []  # contains edge_trace, node_trace, middle_node_trace

    # Plot edges on the graph
    index = 0
    for edge in G.edges:
        x0, y0 = G.nodes[edge[0]]["pos"]
        x1, y1 = G.nodes[edge[1]]["pos"]
        trace = go.Scatter(
            x=tuple([x0, x1, None]),
            y=tuple([y0, y1, None]),
            mode="lines",
            marker=dict(color="grey"),
            line_shape="spline",
            opacity=1,
        )
        traceRecode.append(trace)
        index = index + 1

    # Plot nodes on the graph
    index = 0
    for node in G.nodes():
        x, y = G.nodes[node]["pos"]
        hovertext = (
            "Name: "
            + str(G.nodes[node]["Name"])
            + "<br>"
            + "Type: "
            + str(G.nodes[node]["Type"])
        )
        component_id = G.nodes[node]
        node_trace = go.Scatter(
            x=tuple([x]),
            y=tuple([y]),
            marker=dict(
                size=35,
                color=node_type_colour[G.nodes[node]["Type"]],
                line=dict(width=2, color="DarkSlateGrey"),
            ),
            hovertext=tuple([hovertext]),
            customdata=tuple([component_id]),
            text=node1["Name"][index],
            mode="markers+text",
            textposition="bottom center",
            hoverinfo="text",
        )
        traceRecode.append(node_trace)
        index = index + 1

    # Plot graph
    figure = {
        "data": traceRecode,
        "layout": go.Layout(
            title="Model Structure",
            showlegend=False,
            hovermode="closest",
            margin={"b": 40, "l": 40, "r": 40, "t": 40},
            xaxis={"showgrid": False, "zeroline": False, "showticklabels": False},
            yaxis={"showgrid": False, "zeroline": False, "showticklabels": False},
            height=600,
            clickmode="event+select",
            annotations=[
                # Configure length of edges, etc.
                dict(
                    x=(G.nodes[edge[1]]["pos"][0] * 3 + G.nodes[edge[0]]["pos"][0]) / 4,
                    y=(G.nodes[edge[1]]["pos"][1] * 3 + G.nodes[edge[0]]["pos"][1]) / 4,
                    xref="x",
                    yref="y",
                    text="",
                    showarrow=False,
                    arrowhead=1,
                    arrowsize=2,
                    arrowwidth=1,
                    opacity=1,
                )
                for edge in G.edges
            ],
        ),
    }
    return figure
