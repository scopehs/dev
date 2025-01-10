import pandas as pd
from lightweight_charts import Chart

def calculate_sma(df, period: int = 50):
    return pd.DataFrame({
        'time': df['date'],
        f'SMA {period}': df['close'].rolling(window=period).mean()
    }).dropna()

def on_search(chart, string):
    print(f'Search Text: "{string}" | Chart/SubChart ID: "{chart.id}"')

def on_button_press(chart):
    new_button_value = 'On' if chart.topbar['my_button'].value == 'Off' else 'Off'
    chart.topbar['my_button'].set(new_button_value)
    print(f'Turned something {new_button_value.lower()}.')

def on_timeframe_selection(chart):
    print(f'Getting data with a {chart.topbar["my_switcher"].value} timeframe.')


if __name__ == '__main__':
    chart = Chart()
    line = chart.create_line(name='SMA 50')

    df = pd.read_csv('ohlcv.csv')
    sma_df = calculate_sma(df, period=50)

    # Subscribe the function above to search event
    chart.events.search += on_search  

    chart.topbar.button('my_button', 'Off', func=on_button_press)

    chart.topbar.switcher(
        name='my_switcher',
        options=('1min', '5min', '30min'),
        default='5min',
        func=on_timeframe_selection)
    
    chart.set(df)
    line.set(sma_df)
    
    chart.show(block=True)



