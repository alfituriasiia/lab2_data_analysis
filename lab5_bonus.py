import numpy as np
import dash
from dash import dcc, html, Output, Input
import plotly.graph_objs as go
from scipy.signal import butter, filtfilt

# Константи
TIME = np.linspace(0, 2 * np.pi, 1000)

# Функція гармоніки
def generate_harmonic(amplitude, frequency, phase):
    return amplitude * np.sin(frequency * TIME + phase)

# Функція шуму
def generate_noise(mean, std):
    return np.random.normal(mean, std, TIME.shape)

# Фільтрація
def filter_signal(signal, cutoff):
    b, a = butter(N=3, Wn=cutoff)
    return filtfilt(b, a, signal)

# Dash-додаток
app = dash.Dash(__name__)
app.title = "Додаткове завдання Lab 5"

app.layout = html.Div([
    html.H2("Інтерактивна гармоніка з шумом та фільтрацією (додаткове завдання)", style={'textAlign': 'center'}),

    # Слайдери параметрів
    html.Div([
        html.Label("Амплітуда"), dcc.Slider(0.1, 2.0, 0.1, value=1.0, id='amplitude'),
        html.Label("Частота"), dcc.Slider(0.5, 10.0, 0.1, value=2.0, id='frequency'),
        html.Label("Фаза"), dcc.Slider(0, 2*np.pi, 0.1, value=0.0, id='phase'),
        html.Label("Середнє шуму"), dcc.Slider(-1.0, 1.0, 0.1, value=0.0, id='noise_mean'),
        html.Label("Дисперсія шуму"), dcc.Slider(0.0, 1.0, 0.1, value=0.3, id='noise_std'),
        html.Label("Частота зрізу (фільтр)"), dcc.Slider(0.01, 0.3, 0.01, value=0.05, id='cutoff')
    ], style={'width': '60%', 'margin': 'auto'}),

    # Чекбокси
    html.Div([
        dcc.Checklist(['Показати шум'], id='show_noise', value=['Показати шум']),
        dcc.Checklist(['Показати фільтр'], id='show_filter', value=['Показати фільтр']),
    ], style={'margin': '20px'}),

    # Графік
    dcc.Graph(id='harmonic_graph')
])


@app.callback(
    Output('harmonic_graph', 'figure'),
    Input('amplitude', 'value'),
    Input('frequency', 'value'),
    Input('phase', 'value'),
    Input('noise_mean', 'value'),
    Input('noise_std', 'value'),
    Input('cutoff', 'value'),
    Input('show_noise', 'value'),
    Input('show_filter', 'value')
)
def update_graph(amplitude, frequency, phase, noise_mean, noise_std, cutoff, show_noise, show_filter):
    y_clean = generate_harmonic(amplitude, frequency, phase)
    noise = generate_noise(noise_mean, noise_std)
    y_noisy = y_clean + noise
    y_filtered = filter_signal(y_noisy, cutoff)

    traces = [
        go.Scatter(x=TIME, y=y_clean, mode='lines', name='Чиста гармоніка', line=dict(color='blue', dash='dash'))
    ]

    if 'Показати шум' in show_noise:
        traces.append(go.Scatter(x=TIME, y=y_noisy, mode='lines', name='Гармоніка з шумом', line=dict(color='orange')))

    if 'Показати фільтр' in show_filter:
        traces.append(go.Scatter(x=TIME, y=y_filtered, mode='lines', name='Відфільтрований сигнал', line=dict(color='green')))

    layout = go.Layout(title='Інтерактивна гармоніка',
                       xaxis=dict(title='Час'),
                       yaxis=dict(title='Значення'),
                       height=600)

    return {'data': traces, 'layout': layout}

if __name__ == '__main__':
    app.run(debug=True)

