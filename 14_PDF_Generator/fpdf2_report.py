from fpdf import FPDF
from fpdf.enums import XPos, YPos
from matplotlib.ticker import MaxNLocator
import json
import matplotlib.pyplot as plt
import pandas as pd

website_link = "www.prepbox.io"


def generate_graph(sessions, graph_file_path):
    df = pd.DataFrame(sessions)
    fig, ax = plt.subplots(figsize=(12, 7.5), dpi=96)

    ax.bar(
        df["date"],
        df["correct_session"],
        width=0.6,
        color="#00B0F0",
        label="Correct In session",
    )
    ax.bar(
        df["date"],
        df["correct_nosession"],
        width=0.6,
        color="#DEEBF7",
        bottom=df["correct_session"],
        label="Correct Outside of Session",
    )
    ax.bar(
        df["date"],
        df["incorrect_session"],
        width=0.6,
        color="#D0CECE",
        bottom=df["correct_session"] + df["correct_nosession"],
        label="Incorrect In session",
    )
    ax.bar(
        df["date"],
        df["incorrect_nosession"],
        width=0.6,
        color="#EDEDED",
        bottom=df["correct_session"]
        + df["correct_nosession"]
        + df["incorrect_session"],
        label="Incorrect Outside of Session",
    )

    ax.set_xlabel("", fontsize=14, labelpad=10)  # No need for an axis label
    ax.xaxis.set_label_position("bottom")
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.xaxis.set_tick_params(
        pad=2, labelbottom=True, bottom=True, labelsize=12, labelrotation=90
    )
    plt.xticks(df["date"])

    for c in ax.containers:
        # Optional: if the segment is small or 0, customize the labels
        labels = [v.get_height() if v.get_height() > 0 else "" for v in c]

        # remove the labels parameter if it's not needed for customized labels
        ax.bar_label(c, labels=labels, label_type="center", fontsize=12)

    ax.set_ylabel("Problems solved", fontsize=14, labelpad=10)
    ax.yaxis.set_label_position("left")
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.yaxis.set_tick_params(
        pad=2, labeltop=False, labelbottom=True, bottom=False, labelsize=12
    )

    # Remove the spines
    ax.spines[["top", "right"]].set_visible(False)

    # Make the left spine thicker
    ax.spines["right"].set_linewidth(1.1)

    # Color axis
    ax.spines["left"].set_color("#398FE5")
    ax.spines["bottom"].set_color("#398FE5")

    # Add in title and subtitle
    ax.text(
        x=0.12,
        y=0.93,
        s="Questions Solved in the Past 10 Sessions",
        transform=fig.transFigure,
        ha="left",
        fontsize=16,
        weight="bold",
        alpha=0.8,
    )
    ax.legend(loc="upper left", fontsize=12)

    # Adjust the margins around the plot area
    plt.subplots_adjust(
        left=None, bottom=0.2, right=None, top=0.85, wspace=None, hspace=None
    )

    # Set a white background
    fig.patch.set_facecolor("white")

    plt.savefig(graph_file_path)


class Report:
    def __init__(self, json):
        self.course = json["course"]
        self.title = json["title"]
        self.progress = int(json["progress"])
        self.sessions = json["sessions"]
        self.parent_name = json["parent_name"]
        self.student_name = json["student_name"]
        self.report_date = json["report_date"]
        self.student_id = json["student_id"]
        self.total_questions = json["total_questions"]
        self.join_date = json["join_date"]
        self.session_questions = json["session_questions"]
        self.session_minutes = int(json["session_minutes"])
        self.session_data = pd.DataFrame(json["session_data"])
        self.question_count = len(json["session_data"])


class PDF(FPDF):
    def header(self):
        self.set_xy(0, 0)
        self.set_fill_color(57, 143, 229)
        self.cell(300, 2, "", align="C", fill=True)

    def add_sub_header(self, student_name, report_date):
        self.ln(5)
        self.image("./prepbox_logo.png", x=77, y=11, w=60, h=0, link=website_link)
        self.set_text_color(162, 162, 162)
        self.ln(30)
        self.set_font("helvetica", "B", 14)
        self.add_new_cell(0, 8, f"{student_name} | Date: {report_date}")
        self.ln(1)

    def footer(self):
        self.set_text_color(169, 169, 169)
        self.set_font("helvetica", "", 8)
        self.set_y(-19)
        self.cell(
            0,
            10,
            website_link,
            new_x=XPos.LMARGIN,
            new_y=YPos.NEXT,
            align="C",
            link=website_link,
        )
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.cell(0, 10, f"     Page {self.page_no()}/{{nb}}", align="C")

    def add_progress(self, course, progress):
        self.set_fill_color(162, 162, 162)
        self.cell(10)
        self.add_new_cell(165, 0.2, "", "C", True)
        self.set_fill_color(0, 176, 240)
        self.set_text_color(0, 0, 0)
        self.set_font("helvetica", "B", 12)
        self.ln(3)
        self.add_new_cell(0, 8, f"{course} Mastery Level")
        self.ln(3)
        self.set_font("helvetica", "", 12)
        self.cell(10)
        self.cell(35, 10, "", align="L")

        for i in range(0, 99):
            if i == 0 and i + 1 <= progress:
                self.cell(1, 10, "", "L,B,T", align="C", fill=True)
            elif i > 0 and i + 1 <= progress:
                self.cell(1, 10, "", "B,T", align="C", fill=True)
            elif i > 0 and i + 1 <= progress:
                self.cell(1, 10, "", "B,T", align="C")
            else:
                self.cell(1, 10, "", "B,T", align="C")

        if progress == 100:
            self.cell(
                1,
                10,
                "",
                "R,B,T",
                new_x=XPos.LMARGIN,
                new_y=YPos.NEXT,
                align="C",
                fill=True,
            )
        else:
            self.cell(
                1,
                10,
                "",
                "R,B,T",
                new_x=XPos.LMARGIN,
                new_y=YPos.NEXT,
                align="C",
            )

        self.set_fill_color(57, 143, 229)
        self.cell(45)
        self.cell(progress - 4, 10, "", align="C")
        self.add_new_cell(10, 10, f"${progress}%", "L")
        self.ln(3)

    def add_line(self, r, g, b):
        self.set_fill_color(r, g, b)
        self.cell(10)
        self.add_new_cell(165, 0.2, "", "C", True)

    def add_new_cell(self, width, height, text, align="C", fill=False):
        self.cell(
            width,
            height,
            text,
            new_x=XPos.LMARGIN,
            new_y=YPos.NEXT,
            align=align,
            fill=fill,
        )

    def add_stats(self, student_name, session_questions, session_minutes):
        stats = f"${session_questions} problems in {session_minutes} minutes"
        self.set_font("helvetica", "B", 12)
        self.add_new_cell(0, 10, f"Hi! {student_name} has just solved")
        self.set_font("helvetica", "", 12)
        self.add_new_cell(0, 7, stats)
        self.ln()
        self.ln(3)

    def add_performance(self, join_date, total_questions):
        self.set_font("helvetica", "B", 12)
        self.add_new_cell(0, 10, "Overall Performance Trends")
        self.set_font("helvetica", "", 12)
        self.add_new_cell(0, 7, f"Join Date:  {join_date}")
        self.add_new_cell(0, 7, f"Questions Solved to Date:  {total_questions}")
        self.ln()
        self.ln(3)

    def add_graph(self, sessions):
        graph_file_path = "/tmp/graph.png"
        generate_graph(sessions, graph_file_path)
        img_width = 200
        doc_width = self.w
        x_width = (doc_width - img_width) / 2
        self.image(graph_file_path, x=x_width, y=145, w=img_width, h=0, link="")

    def add_images(self, imgl, report):
        img_width = 150
        img_height = 109.489
        doc_width = self.w
        x_width = (doc_width - img_width) / 2
        for i in range(0, len(imgl)):
            if i % 2 == 1:
                self.set_xy(x_width, 150)
                self.ln(1)
                self.cell(x_width)
                self.cell(44, 7, f" Question Solved {i + 1}", align="L")
                if report.session_data.accuracy[i] == 1:
                    self.add_new_cell(10, 7, " - Correct", "L")
                else:
                    self.cell(10, 7, " - Incorrect", align="L")
                self.image(
                    report.session_data.image[i],
                    x=x_width,
                    y=165,
                    w=img_width,
                    h=img_height,
                )
            else:
                self.add_page()
                self.ln(5)
                self.set_font("helvetica", "B", 13)
                self.cell(7)
                self.cell(44, 7, f" Question Solved {i + 1}", align="L")
                if report.session_data.accuracy[i] == 1:
                    self.add_new_cell(10, 7, " - Correct", "L")
                else:
                    self.cell(10, 7, " - Incorrect", align="L")
                self.image(
                    report.session_data.image[i],
                    x=x_width,
                    y=28,
                    w=img_width,
                    h=img_height,
                )
                self.ln(60)


def generate_report(report_data):
    r = Report(report_data)
    pdf = PDF()

    pdf.set_author("PrepBox")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("helvetica", "B", 14)
    pdf.set_title(r.title)
    pdf.add_page()

    pdf.add_sub_header(r.student_name, r.report_date)
    pdf.add_progress(r.course, r.progress)
    pdf.add_line(162, 162, 162)  # gray
    pdf.add_stats(r.student_name, r.session_questions, r.session_minutes)
    pdf.add_line(162, 162, 162)  # gray
    pdf.add_performance(r.join_date, r.total_questions)
    pdf.add_line(57, 143, 229)  # blue
    pdf.add_graph(r.sessions)

    pdf.add_images(r.session_data["image"].tolist(), r)

    pdf.output(f"{r.student_id}_{r.title}.pdf")


f = open("data.json")
ev = json.load(f)

generate_report(ev)