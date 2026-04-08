import matplotlib.pyplot as plt
from io import BytesIO

def generate_attendance_graph(df):
    """
    Generates bar chart for attendance %
    """

    fig, ax = plt.subplots(figsize=(8, 4))

    names = df["Name"]
    attendance = df["attendance_percent"]

    ax.bar(names, attendance)

    ax.set_title("Attendance Percentage")
    ax.set_xlabel("Students")
    ax.set_ylabel("Percentage")

    ax.tick_params(axis='x', rotation=45)

    buffer = BytesIO()
    plt.savefig(buffer, format="png", bbox_inches="tight")
    buffer.seek(0)

    plt.close()

    return buffer