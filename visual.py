import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from datetime import datetime, timedelta

plt.ion()

df = pd.read_excel("TWTR.xlsx")

df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values(by='Date')

def filter_data(period):
    end_date = df['Date'].max()
    
    if period == "1M":
        start_date = end_date - timedelta(days=30)
    elif period == "6M":
        start_date = end_date - timedelta(days=182)
    elif period == "1Y":
        start_date = end_date - timedelta(days=365)
    elif period == "5Y":
        start_date = end_date - timedelta(days=5*365)
    else:  # MAX
        start_date = df['Date'].min()
    
    return df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

fig, ax = plt.subplots(figsize=(15, 7))
plt.subplots_adjust(bottom=0.3)

fig.patch.set_facecolor("#fca5a5")
ax.set_facecolor("#3D3D3D")

filtered_df = filter_data("MAX")
line, = ax.plot(filtered_df['Date'], filtered_df['Close'], color="#37FF29", linewidth=2.5)

# Improve visuals
ax.set_title("Twitter Stock Price Timeline", fontsize=16, fontweight='bold', color="#050000")
ax.set_xlabel("Date", fontsize=12, color="#080000")
ax.set_ylabel("Closing Price (USD)", fontsize=12, color="#000000")
ax.grid(True, linestyle='--', alpha=0.5)

ax.tick_params(colors="#000700", labelsize=10)

def update(event):
    label = event.inaxes.get_label()
    filtered_df = filter_data(label)
    
    line.set_xdata(filtered_df['Date'])
    line.set_ydata(filtered_df['Close'])
    
    ax.set_xlim(filtered_df['Date'].min(), filtered_df['Date'].max())
    ax.set_ylim(filtered_df['Close'].min(), filtered_df['Close'].max())
    ax.set_title(f"Twitter Stock Price - {label} Period", fontsize=16, fontweight='bold', color='#333333')
    
    fig.canvas.draw_idle()

button_labels = ["1M", "6M", "1Y", "5Y", "MAX"]
positions = [0.1, 0.25, 0.4, 0.55, 0.7]
buttons = []

for i, label in enumerate(button_labels):
    ax_button = plt.axes([positions[i], 0.1, 0.1, 0.05])
    button = Button(ax_button, label, color="#f7b21c", hovercolor="#f6d621")
    button.ax.set_label(label)
    button.on_clicked(update)
    buttons.append(button)

plt.show(block=True)
