import matplotlib.pyplot as plt
from io import BytesIO

def generate_daily_trend_graph(df):
    fig, ax = plt.subplots()
    ax.plot(df["Date"], df["attendance_percent"], marker='o')
    ax.set_title("Daily Attendance Trend")
    ax.tick_params(axis='x', rotation=45)

    buffer = BytesIO()
    plt.savefig(buffer, format="png", bbox_inches="tight")
    buffer.seek(0)
    plt.close()

    return buffer


def generate_subject_graph(df):
    fig, ax = plt.subplots()
    ax.bar(df["Subject Code"], df["attendance_percent"])
    ax.set_title("Subject Attendance")
    ax.tick_params(axis='x', rotation=45)

    buffer = BytesIO()
    plt.savefig(buffer, format="png", bbox_inches="tight")
    buffer.seek(0)
    plt.close()

    return buffer