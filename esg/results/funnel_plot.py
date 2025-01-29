import logging

logger = logging.getLogger(__name__)

import plotly.express as px
import plotly.graph_objects as go

import cm_dashboards.esg.db_helper as db_helper
import cm_dashboards.esg.helpers as helpers


def get_table_data(wvr_path, report_date, plot_variable, group, max_date, threshold):
    """
    Get table data from df
    :param wvr_path: path to WVR file
    :param report_date: report date
    :param plot_variable: variable name to select cenrtain data for plotting
    :param group: filter by group name
    :param senario: filter by senario value
    :param max_date: max report date period
    :param threshold: filter by threshold value
    :return: tuple (data, columns, conditional_style) for dash_table.DataTable
    """
    # Initialize DB instance
    chart_data = db_helper.GetChartData(
        plot_variable=plot_variable,
        group=group,
        # senario=senario,
        max_date=max_date,
    )
    timeline = db_helper.ReportDate(max_date=max_date)

    # Get output as DF
    model_name = helpers.get_date_dropdown_options(report_date=report_date)
    df = helpers.get_df(chart_data, wvr_path, model_name)
    logger.info("Found data length: {}".format(len(df.index)))

    # Get available distinct report dates
    report_dates = helpers.get_df(timeline, wvr_path, model_name)
    report_dates = report_dates.values.tolist()

    # Calculate and add required percentage values
    df = helpers.calculate_percentile(df, plot_variable, report_dates)

    # Check if max date is set to auto calculation within the threshold range
    if max_date == "AutoCalculate":
        df = helpers.apply_threshold(df, threshold)

    # Get chart
    chart = create_chart(plot_variable, df)

    # # Prepare table data
    # df_rotated = helpers.pivot_df(df)
    # data, colum, style_data = helpers.prepare_table_data(df_rotated)

    return chart


def create_chart(plot_variable, df):
    """
    Create dash chart object
    :param plot_variable: Variable name to be used for chart creation
    :param df: data to be used for chart creation
    :return chart: chart object
    """
    # Define title and plot variables
    title = "<b>Funnel plot of {}</b>".format(plot_variable)

    # Create chart object
    chart = px.line(
        title=title,
        height=550,
        template="cloud_manager",
        labels=dict(value=plot_variable, variable="Percentile"),
    )

    # # Update chart parameters
    chart.update_xaxes(type="category")
    chart.update_yaxes(autotypenumbers="strict")
    chart.update_traces(patch=dict(line=dict(dash="solid", width=2)))

    # Manually plot required data points
    chart.add_trace(
        go.Scatter(
            x=df["Report_date"],
            y=df[plot_variable],
            line_color="rgba(0,0,0,0)",
            showlegend=False,
            name="hidden_line",
            mode="lines",
            hoverinfo="none",
        )
    )

    chart.add_trace(
        go.Scatter(
            x=df["Report_date"],
            y=df["100%-99%"]
            + df["97.5%-95%"]
            + df["95%-90%"]
            + df["90%-75%"]
            + df["75%-25%"]
            + df["25%-10%"]
            + df["10%-5%"]
            + df["5%-2.5%"]
            + df["2.5%-1%"]
            + df["1%-0%"]
            + df[plot_variable],
            fill="tonexty",
            fillcolor="rgba(255,255,153, 1)",
            line_color="rgb(255,255,153)",
            showlegend=True,
            name="100%-99%",
            mode="lines",
        )
    )

    chart.add_trace(
        go.Scatter(
            x=df["Report_date"],
            y=df[plot_variable],
            line_color="rgba(0,0,0,0)",
            showlegend=False,
            name="hidden_line",
            mode="lines",
            hoverinfo="none",
        )
    )

    chart.add_trace(
        go.Scatter(
            x=df["Report_date"],
            y=df["97.5%-95%"]
            + df["95%-90%"]
            + df["90%-75%"]
            + df["75%-25%"]
            + df["25%-10%"]
            + df["10%-5%"]
            + df["5%-2.5%"]
            + df["2.5%-1%"]
            + df["1%-0%"]
            + df[plot_variable],
            fill="tonexty",
            fillcolor="rgba(255,255,0, 1)",
            line_color="rgb(255,255,0)",
            showlegend=True,
            name="97.5%-95%",
            mode="lines",
        )
    )

    chart.add_trace(
        go.Scatter(
            x=df["Report_date"],
            y=df[plot_variable],
            line_color="rgba(0,0,0,0)",
            showlegend=False,
            name="hidden_line",
            mode="lines",
            hoverinfo="none",
        )
    )

    chart.add_trace(
        go.Scatter(
            x=df["Report_date"],
            y=df["95%-90%"]
            + df["90%-75%"]
            + df["75%-25%"]
            + df["25%-10%"]
            + df["10%-5%"]
            + df["5%-2.5%"]
            + df["2.5%-1%"]
            + df["1%-0%"]
            + df[plot_variable],
            fill="tonexty",
            fillcolor="rgba(255,153,0, 1)",
            line_color="rgb(255,153,0)",
            showlegend=True,
            name="95%-90%",
            mode="lines",
        )
    )

    chart.add_trace(
        go.Scatter(
            x=df["Report_date"],
            y=df[plot_variable],
            line_color="rgba(0,0,0,0)",
            showlegend=False,
            name="hidden_line",
            mode="lines",
            hoverinfo="none",
        )
    )

    chart.add_trace(
        go.Scatter(
            x=df["Report_date"],
            y=df["90%-75%"]
            + df["75%-25%"]
            + df["25%-10%"]
            + df["10%-5%"]
            + df["5%-2.5%"]
            + df["2.5%-1%"]
            + df["1%-0%"]
            + df[plot_variable],
            fill="tonexty",
            fillcolor="rgba(255,102,1, 1)",
            line_color="rgb(255,102,0)",
            showlegend=True,
            name="90%-75%",
            mode="lines",
        )
    )

    chart.add_trace(
        go.Scatter(
            x=df["Report_date"],
            y=df[plot_variable],
            line_color="rgba(0,0,0,0)",
            showlegend=False,
            name="hidden_line",
            mode="lines",
            hoverinfo="none",
        )
    )

    chart.add_trace(
        go.Scatter(
            x=df["Report_date"],
            y=df["75%-25%"]
            + df["25%-10%"]
            + df["10%-5%"]
            + df["5%-2.5%"]
            + df["2.5%-1%"]
            + df["1%-0%"]
            + df[plot_variable],
            fill="tonexty",
            fillcolor="rgba(255,0,0, 1)",
            line_color="rgb(255,0,0)",
            showlegend=True,
            name="75%-25%",
            mode="lines",
        )
    )
    chart.add_trace(
        go.Scatter(
            x=df["Report_date"],
            y=df[plot_variable],
            line_color="rgba(0,0,0,0)",
            showlegend=False,
            name="hidden_line",
            mode="lines",
            hoverinfo="none",
        )
    )

    chart.add_trace(
        go.Scatter(
            x=df["Report_date"],
            y=df["25%-10%"]
            + df["10%-5%"]
            + df["5%-2.5%"]
            + df["2.5%-1%"]
            + df["1%-0%"]
            + df[plot_variable],
            fill="tonexty",
            fillcolor="rgba(255,102,0, 1)",
            line_color="rgb(255,102,0)",
            showlegend=True,
            name="25%-10%",
            mode="lines",
        )
    )

    chart.add_trace(
        go.Scatter(
            x=df["Report_date"],
            y=df[plot_variable],
            line_color="rgba(0,0,0,0)",
            showlegend=False,
            name="hidden_line",
            mode="lines",
            hoverinfo="none",
        )
    )

    chart.add_trace(
        go.Scatter(
            x=df["Report_date"],
            y=df["10%-5%"]
            + df["5%-2.5%"]
            + df["2.5%-1%"]
            + df["1%-0%"]
            + df[plot_variable],
            fill="tonexty",
            fillcolor="rgba(255,153,0, 1)",
            line_color="rgb(255,153,0)",
            showlegend=True,
            name="10%-5%",
            mode="lines",
        )
    )

    chart.add_trace(
        go.Scatter(
            x=df["Report_date"],
            y=df[plot_variable],
            line_color="rgba(0,0,0,0)",
            showlegend=False,
            name="hidden_line",
            mode="lines",
            hoverinfo="none",
        )
    )

    chart.add_trace(
        go.Scatter(
            x=df["Report_date"],
            y=df["5%-2.5%"] + df["2.5%-1%"] + df["1%-0%"] + df[plot_variable],
            fill="tonexty",
            fillcolor="rgba(255,204,0, 1)",
            line_color="rgb(255,204,0)",
            showlegend=True,
            name="5%-2.5%",
            mode="lines",
        )
    )

    chart.add_trace(
        go.Scatter(
            x=df["Report_date"],
            y=df[plot_variable],
            line_color="rgba(0,0,0,0)",
            showlegend=False,
            name="hidden_line",
            mode="lines",
            hoverinfo="none",
        )
    )

    chart.add_trace(
        go.Scatter(
            x=df["Report_date"],
            y=df["2.5%-1%"] + df["1%-0%"] + df[plot_variable],
            fill="tonexty",
            fillcolor="rgba(255,255,0, 1)",
            line_color="rgb(255,255,0)",
            showlegend=True,
            name="2.5%-1%",
            mode="lines",
        )
    )

    chart.add_trace(
        go.Scatter(
            x=df["Report_date"],
            y=df[plot_variable],
            line_color="rgba(0,0,0,0)",
            showlegend=False,
            name="hidden_line",
            mode="lines",
            hoverinfo="none",
        )
    )

    chart.add_trace(
        go.Scatter(
            x=df["Report_date"],
            y=df["1%-0%"] + df[plot_variable],
            fill="tonexty",
            fillcolor="rgba(255,255,153, 1)",
            line_color="rgb(255,255,153)",
            showlegend=True,
            name="1%-0%",
            mode="lines",
        )
    )

    chart.add_trace(
        go.Scatter(
            x=df["Report_date"],
            y=df[plot_variable],
            line_color="rgba(0,0,0,0)",
            showlegend=False,
            name="hidden_line",
            mode="lines",
            hoverinfo="none",
        )
    )

    chart.add_trace(
        go.Scatter(
            x=df["Report_date"],
            y=df["Median"],
            line_color="rgba(255,0,0)",
            showlegend=True,
            name="Median",
            mode="lines+markers",
            marker=dict(color="black", size=12, symbol="circle-open"),
            meta=dict(line=dict(width=1, color="black")),
        )
    )

    chart.add_trace(
        go.Scatter(
            x=df["Report_date"],
            y=df["Average"],
            line_color="rgba(255,0,0)",
            showlegend=True,
            name="Average",
            mode="lines+markers",
            marker=dict(color="black", size=12, symbol="x-thin-open"),
            meta=dict(line=dict(width=1, color="black")),
        )
    )

    chart.add_trace(
        go.Scatter(
            x=df["Report_date"],
            y=df[plot_variable],
            line_color="rgba(0,0,0,0)",
            showlegend=False,
            name="hidden_line",
            mode="lines",
            hoverinfo="none",
        )
    )

    return chart
