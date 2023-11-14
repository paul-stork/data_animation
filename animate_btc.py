import pandas as pd

from datetime import date
from dateutil.relativedelta import relativedelta
from datetime import datetime

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as tick

import pynimate as nim
from pynimate.utils import human_readable

start_time = datetime.now()
# print(f'Start time: {start_time}')

past_date = datetime.today() - relativedelta(months=1)

df = pd.read_csv('BTC data.csv')

df['time_close_format'] = pd.to_datetime(df['time_close']).dt.strftime('%Y/%m/%d %H:%M')

df =  df.query(f"time_close >= '{past_date}'")

working_df = df.filter(['rate_close', 'time_close_format'], axis=1)

working_df = working_df.set_index("time_close_format")

for side in ["left", "right", "top", "bottom"]:
    mpl.rcParams[f"axes.spines.{side}"] = False
mpl.rcParams["figure.facecolor"] = "#001219"
mpl.rcParams["axes.facecolor"] = "#001219"
mpl.rcParams["savefig.facecolor"] = "#001219"

def post(self, i):
    self.ax.yaxis.set_major_formatter(
        tick.FuncFormatter(lambda x, pos: human_readable(x))
    )
    
cnv = nim.Canvas()
dfr = nim.LineDatafier(working_df, "%Y/%m/%d %H:%M", "24H")

plot = nim.Lineplot(
    dfr,
    post_update=post,
    palettes=['Set3'],
    scatter_markers=False,
    legend=True,
    fixed_ylim=True,
    grid=False,
)

plot.set_column_linestyles({"rate_close": "solid"})
plot.set_title("Bitcoin Prices ($)", y=1.05, color="w", weight=600)

plot.set_xlabel("date", color="w", size=11)
plot.set_time(
    callback=lambda i, datafier: datafier.data.index[i].strftime("%Y/%m/%d %H:%M:%S"),
    color="w",
    size=13,
)

plot.set_line_annots(lambda col, val: f"({human_readable(val)})", color="w")
plot.set_legend(labelcolor="w")

plot.set_xticks(colors="w", length=0, labelsize=10)
plot.set_yticks(colors="w", labelsize=10)
cnv.add_plot(plot)
cnv.animate(interval=20)
cnv.save("Bitcoin Price activity 1 month", 24)

finish_time = datetime.now()
# print(f"Run Finished: {finish_time}")

total_time = finish_time - start_time
print(f"Total time required to run: {total_time}")

plt.show()