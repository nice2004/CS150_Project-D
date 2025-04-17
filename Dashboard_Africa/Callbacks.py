from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from Datasets import dataset_agriculture, dataset_conflicts, conflict_columns, agri_value_col


def callbacks(app):
    @app.callback(
        Output('conflict-bar-chart', 'figure'),
        [Input('conflict-dropdown', 'value')]
    )
    def update_conflict(selected_conflict):
        conflict_column = conflict_columns[selected_conflict]
        filter_data = dataset_conflicts.dropna(subset=[conflict_column])

        global_data = filter_data.groupby('Year')[conflict_column].sum().reset_index()

        # Create bar chart
        fig = px.bar(
            global_data,
            x='Year',
            y=conflict_column,
            title=f'Global Trend of {selected_conflict.replace("_", " ").title()} Conflicts',
            labels={conflict_column: 'Number of Conflicts', 'Year': 'Year'},
            template='plotly_white'
        )

        fig.update_layout(
            transition_duration=500,
            xaxis_title='Year',
            yaxis_title='Number of Conflicts',
            plot_bgcolor='rgba (0,0,0,0)',
            margin=dict(l=40, r=20, t=40, b=40)
        )

        return fig

    @app.callback(
        Output('agriculture-line-chart', 'figure'),
        Input('year-range-slider', 'value')
    )
    def update_agriculture_chart(year_range):
        global_agri_data = dataset_agriculture.groupby('Year')[agri_value_col].sum().reset_index()
        fig = px.line(
            global_agri_data,
            x='Year',
            y=agri_value_col,
            title=f'Global Agricultural Production Value Over Time',
            labels={agri_value_col: 'Production Value (thousand US$)', 'Year': 'Year'},
            template='plotly_white'

        )

        fig.update_layout(
            transition_duration=500,
            xaxis_title='Year',
            yaxis_title='Production Value (thousand US$)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=40, r=20, t=40, b=40)
        )

        return fig

    @app.callback(
        Output('comparison-line-chart', 'figure'),
        Input('year-range-slider', 'value'),
        Input('comparison-conflict-dropdown', 'value')
    )
    def update_comparison_chart(year_range, selected_conflict):
        # Get selected column for conflict
        conflict_col = conflict_columns[selected_conflict]

        # Filter data based on selected year range
        min_year, max_year = year_range
        filtered_conflicts = dataset_conflicts[(dataset_conflicts['Year'] >= min_year) &
                                               (dataset_conflicts['Year'] <= max_year)]
        filtered_agriculture = dataset_agriculture[(dataset_agriculture['Year'] >= min_year) &
                                                   (dataset_agriculture['Year'] <= max_year)]

        # Aggregate data globally for each year
        global_conflicts = filtered_conflicts.groupby('Year')[conflict_col].sum().reset_index()
        global_agriculture = filtered_agriculture.groupby('Year')[agri_value_col].sum().reset_index()

        # Create figure with two y-axes
        fig = go.Figure()

        # Add conflict data
        fig.add_trace(
            go.Scatter(
                x=global_conflicts['Year'],
                y=global_conflicts[conflict_col],
                name=f'{selected_conflict.replace("_", " ").title()} Conflicts',
                line=dict(color='#E63946', width=3),  # Brighter red, thicker line
                mode='lines+markers',  # Add markers to the line
                marker=dict(size=8)
            )
        )

        # Create a secondary Y axis for agriculture data
        fig.add_trace(
            go.Scatter(
                x=global_agriculture['Year'],
                y=global_agriculture[agri_value_col],
                name='Agricultural Production Value',
                yaxis='y2',
                line=dict(color='#2A9D8F', width=3, dash='dash'),  # Teal color, dashed line
                mode='lines+markers',
                marker=dict(size=8)
            )
        )

        # Update layout for dual y-axes
        fig.update_layout(
            title=f'Comparison: {selected_conflict.replace("_", " ").title()} Conflicts vs Agricultural Production ({min_year}-{max_year})',
            xaxis=dict(
                title='Year',
                gridcolor='#E5E5E5',
                showgrid=True
            ),
            yaxis=dict(
                title='Number of Conflicts',
                title_font=dict(color='black'),
                tickfont=dict(color='black'),
                gridcolor='#E5E5E5'
            ),
            yaxis2=dict(
                title='Production Value (thousand US$)',
                title_font=dict(color='black'),
                tickfont=dict(color='black'),
                anchor='x',
                overlaying='y',
                side='right'
            ),
            legend=dict(
                title='',
                orientation='h',
                yanchor='bottom',
                y=1.02,  # Slightly above the plot
                xanchor='center',
                x=0.5,
                bgcolor='rgba(0,0,0,0)',  # Transparent background
                bordercolor='rgba(0,0,0,0)',  # No border
                font=dict(
                    size=13,
                    color='black',
                    family='Arial'
                )
            ),
            template='plotly_white',
            plot_bgcolor='rgba(255,255,255,1)',
            paper_bgcolor='rgba(255,255,255,1)',
            margin=dict(l=40, r=40, t=80, b=40),  # More top margin for spacing
            hovermode='x unified'
        )

        # Add a vertical rectangle to highlight recent years if desired
        # fig.add_vrect(x0=2015, x1=max_year, fillcolor="rgba(200,200,200,0.2)", layer="below", line_width=0)

        return fig

    # Callback to update the data tables

    @app.callback(
        [Output('conflict-table', 'data'),
         Output('agriculture-table', 'data')],
        [Input('year-range-slider', 'value')]
    )
    def update_tables(year_range):
        min_year, max_year = year_range
        filtered_conflicts = dataset_conflicts[(dataset_conflicts['Year'] >= min_year) &
                                               (dataset_conflicts['Year'] <= max_year)].to_dict('records')
        filtered_agriculture = dataset_agriculture[(dataset_agriculture['Year'] >= min_year) &
                                                   (dataset_agriculture['Year'] <= max_year)].to_dict('records')

        return filtered_conflicts, filtered_agriculture
