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

# ------------------------------------------
# Teacher Daily Trend
# ------------------------------------------
def generate_teacher_daily_graph(daily_df):
    plt.figure()

    plt.plot(daily_df["Date"], daily_df["attendance_percent"], marker='o')
    plt.xticks(rotation=45)

    plt.title("Daily Attendance Trend")
    plt.xlabel("Date")
    plt.ylabel("Attendance %")

    buffer = BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format="png")
    plt.close()

    buffer.seek(0)
    return buffer


# ------------------------------------------
# Batch Distribution Graph
# ------------------------------------------
def generate_batch_graph(batch_df):
    plt.figure()

    plt.pie(
        batch_df["Students"],
        labels=batch_df["Batch"],
        autopct='%1.1f%%'
    )

    plt.title("Batch Distribution")

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    plt.close()

    buffer.seek(0)
    return buffer