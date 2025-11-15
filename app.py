from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

app = Flask(__name__)

# Load dataset
df = pd.read_csv("weather.csv")

# Clean and prepare data
df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')
df['Temp Max'] = pd.to_numeric(df['Temp Max'], errors='coerce')
df['Temp Min'] = pd.to_numeric(df['Temp Min'], errors='coerce')
df['Rain'] = pd.to_numeric(df['Rain'], errors='coerce')
df = df.dropna(subset=['Date', 'Temp Max', 'Temp Min'])
df['AvgTemperature'] = (df['Temp Max'] + df['Temp Min']) / 2
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.strftime('%B')

# --- Function to filter data ---
def get_filtered_data(year=None, month=None):
    filtered = df.copy()
    if year and year != "All":
        filtered = filtered[filtered['Year'] == int(year)]
    if month and month != "All":
        filtered = filtered[filtered['Month'] == month]
    return filtered

@app.route('/', methods=['GET', 'POST'])
def dashboard():
    selected_year = request.form.get('year', 'All')
    selected_month = request.form.get('month', 'All')
    filtered_df = get_filtered_data(selected_year, selected_month)

    # Summary stats
    avg_temp = round(filtered_df['AvgTemperature'].mean(), 2)
    max_temp = round(filtered_df['Temp Max'].max(), 2)
    min_temp = round(filtered_df['Temp Min'].min(), 2)
    total_rain = round(filtered_df['Rain'].sum(), 2)

    # --- Main Plots ---
    fig_temp = px.line(filtered_df, x='Date', y='AvgTemperature',
                       title='Average Temperature Over Time',
                       template='plotly_white')

    fig_rain = px.bar(filtered_df, x='Date', y='Rain',
                      title='Rainfall Over Time',
                      color='Rain', color_continuous_scale='Blues',
                      template='plotly_white')

    fig_max_min = go.Figure()
    fig_max_min.add_trace(go.Scatter(x=filtered_df['Date'], y=filtered_df['Temp Max'],
                                     mode='lines', name='Max Temp', line=dict(color='red')))
    fig_max_min.add_trace(go.Scatter(x=filtered_df['Date'], y=filtered_df['Temp Min'],
                                     mode='lines', name='Min Temp', line=dict(color='blue')))
    fig_max_min.update_layout(title='Max vs Min Temperature',
                              xaxis_title='Date', yaxis_title='Temperature (°C)',
                              template='plotly_white')

    # --- Extra Analysis 1: Rain vs Temperature Correlation ---
    fig_corr = px.scatter(filtered_df, x='Rain', y='AvgTemperature',
                          title='Correlation between Rainfall and Avg Temperature',
                          template='plotly_white', color='AvgTemperature',
                          color_continuous_scale='RdYlBu')

    # --- Extra Analysis 2: Monthly Average Temperature (Bar Chart) ---
    monthly_avg = filtered_df.groupby('Month', as_index=False)['AvgTemperature'].mean()
    monthly_avg = monthly_avg.sort_values(by='AvgTemperature', ascending=False)
    fig_monthly_avg = px.bar(monthly_avg, x='Month', y='AvgTemperature',
                             title='Average Temperature by Month',
                             color='AvgTemperature', color_continuous_scale='sunset',
                             template='plotly_white')

    # --- Extra Analysis 3: Rainfall Distribution by Month (Pie Chart) ---
    monthly_rain = filtered_df.groupby('Month', as_index=False)['Rain'].sum()
    fig_rain_pie = px.pie(monthly_rain, names='Month', values='Rain',
                          title='Rainfall Distribution by Month',
                          template='plotly_white')

    return render_template(
        'dashboard.html',
        years=sorted(df['Year'].dropna().unique()),
        months=sorted(df['Month'].dropna().unique()),
        selected_year=selected_year,
        selected_month=selected_month,
        avg_temp=avg_temp,
        max_temp=max_temp,
        min_temp=min_temp,
        total_rain=total_rain,
        temp_plot=fig_temp.to_html(full_html=False),
        rain_plot=fig_rain.to_html(full_html=False),
        maxmin_plot=fig_max_min.to_html(full_html=False),
        corr_plot=fig_corr.to_html(full_html=False),
        monthly_avg_plot=fig_monthly_avg.to_html(full_html=False),
        rain_pie_plot=fig_rain_pie.to_html(full_html=False)
    )

if __name__ == '__main__':
    app.run(debug=True)
