from Services.Assistant import Assistant
from Domain.Enum import IndicatorSignalChartType
from Domain.Entities import SignalModel
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly
import pandas as pd

class DrawPlot:

    def __init__(self, processor):
        self.fig = None
        self.processor = processor
        self.plot()

    def plot(self):
        self.fig = plotly.subplots.make_subplots(rows=2, cols=1, shared_xaxes=True)

        # DataMain: TF base for analysys (where indicators have to be applied)
        self.plot_candlesticks(self.processor.broker.pricing.data_main, 1)
        self.plot_indicators_signals(self.processor.strategy.indicators)

        # if len(orders) > 0:
        #     self.plot_table(orders)
        # if len(outcomes) > 0:
        #     self.plot_table(outcomes)

        self.fig.layout.update(go.Layout(barmode='overlay',))
        plotly.offline.plot(self.fig)

    def plot_table(self, array):
        columns_name = dict(values=list(array[0].__dict__.keys()))
        array_matrix = Assistant.objects_list_to_matrix(array)
        table_fig = go.Figure(
            data=[
                go.Table(
                    header=columns_name,
                    cells=dict(values=array_matrix)
                )
            ]
        )
        table_fig.show()

    def plot_marker(self, indicator):
        print()
        if type(indicator.signals) is list:
            df = pd.DataFrame.from_records([s.to_dict() for s in indicator.signals])
        else:
            df = indicator.signals
        # pd.set_option('display.max_rows', None)
        # print(df.head(100))
        # exit()
        trace = go.Scatter(
                name=indicator.name,
                x=df.time,
                y=df.marker,
                mode='markers',
                marker=go.Marker(
                    size=20,
                    symbol=df.symbol,
                    color=df.color
                )
            )
        self.fig.append_trace(trace, 1, 1)

    def plot_line(self, line):
        line = go.Scatter(
                name=line.name,
                x=line.line.index,
                y=line.line.Line,
                line=dict(
                    color=line.color,
                    width=1)
                )
        self.fig.append_trace(line, 1, 1)

    def plot_indicators_signals(self, indicators):
        for indicator in indicators:
            if indicator.type_of_indicator_signal == IndicatorSignalChartType.marker:
                self.plot_marker(indicator)
            elif indicator.type_of_indicator_signal == IndicatorSignalChartType.line:
                self.plot_line(indicator)
            else:
                # rimosso todo, va bene gestire il print
                print('Indicator type has been not recognized.')
                self.processor.logger.write_error()

    def plot_candlesticks(self, data, position):
        candle_data = go.Candlestick(
            name="Main",
            x=data.index,
            open=data.Open,
            high=data.High,
            low=data.Low,
            close=data.Close
        )
        self.fig.append_trace(candle_data, position, 1)

    '''
    def plotDataStream(self, data_stream):
        
        #Candle_data_stream: TF used for emulating ticks received as datastream (where the positions will be opened)
        Candle_data_stream = go.Candlestick(
            name = "Ticks",
            x=data_stream.index,
            open=data_stream.Open,
            high=data_stream.High,
            low=data_stream.Low,
            close=data_stream.Close
        )
        self.fig.append_trace(Candle_data_stream,2,1)
        
    def plotDataMain(self, data_main):
        
        #Candle_data_main: TF base for analysys (where indicators have to be applied)
        Candle_data_main = go.Candlestick(
            name = "Main",
            x=data_main.index,
            open=data_main.Open,
            high=data_main.High,
            low=data_main.Low,
            close=data_main.Close
        )
        self.fig.append_trace(Candle_data_main, 1, 1)
    '''