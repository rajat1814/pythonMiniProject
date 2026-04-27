"""
Mini Project: Student Performance Analysis using Pandas & Matplotlib
Author: Rajat Kumar | Roll No: 03014803123 | Group: ABC-VI-B
Subject: Programming in Python
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os

# ─────────────────────────────────────────
# 1. SAMPLE DATASET
# ─────────────────────────────────────────
data = {
    "Student": [
        "Alice", "Bob", "Charlie", "Diana", "Eve",
        "Frank", "Grace", "Hank", "Ivy", "Jack"
    ],
    "Math":    [88, 72, 95, 60, 78, 85, 91, 55, 76, 83],
    "Science": [75, 68, 90, 58, 82, 79, 88, 62, 71, 80],
    "English": [80, 74, 85, 65, 70, 88, 92, 60, 77, 84],
    "History": [70, 65, 80, 72, 68, 75, 85, 58, 73, 78],
}

df = pd.DataFrame(data)

# ─────────────────────────────────────────
# 2. ANALYSIS
# ─────────────────────────────────────────
subjects = ["Math", "Science", "English", "History"]

df["Total"]   = df[subjects].sum(axis=1)
df["Average"] = df[subjects].mean(axis=1).round(2)
df["Grade"]   = df["Average"].apply(
    lambda x: "A" if x >= 85 else ("B" if x >= 70 else ("C" if x >= 55 else "F"))
)

print("=" * 60)
print("   STUDENT PERFORMANCE ANALYSIS REPORT")
print("=" * 60)
print(df.to_string(index=False))
print("\n--- Subject-wise Statistics ---")
print(df[subjects].describe().round(2))
print(f"\nClass Topper : {df.loc[df['Average'].idxmax(), 'Student']} "
      f"({df['Average'].max():.2f}%)")
print(f"Needs Improvement: {df.loc[df['Average'].idxmin(), 'Student']} "
      f"({df['Average'].min():.2f}%)")

# ─────────────────────────────────────────
# 3. VISUALIZATIONS
# ─────────────────────────────────────────
os.makedirs("output", exist_ok=True)

fig = plt.figure(figsize=(16, 12), facecolor="#f7f9fc")
fig.suptitle("Student Performance Analysis Dashboard",
             fontsize=18, fontweight="bold", color="#2c3e50", y=0.98)

gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.45, wspace=0.35)

colors = ["#3498db", "#e74c3c", "#2ecc71", "#f39c12"]

# ── Plot 1: Bar Chart – Average Score per Student ──
ax1 = fig.add_subplot(gs[0, 0])
bar_colors = ["#27ae60" if g == "A" else "#f39c12" if g == "B" else "#e74c3c"
              for g in df["Grade"]]
bars = ax1.bar(df["Student"], df["Average"], color=bar_colors, edgecolor="white",
               linewidth=0.8)
ax1.set_title("Average Score per Student", fontweight="bold", color="#2c3e50")
ax1.set_xlabel("Student")
ax1.set_ylabel("Average Score (%)")
ax1.set_ylim(0, 100)
ax1.tick_params(axis='x', rotation=45)
for bar, val in zip(bars, df["Average"]):
    ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
             f"{val:.1f}", ha="center", va="bottom", fontsize=8)
ax1.set_facecolor("#fdfdfd")

# ── Plot 2: Line Chart – Subject Trends ──
ax2 = fig.add_subplot(gs[0, 1])
for i, subject in enumerate(subjects):
    ax2.plot(df["Student"], df[subject], marker="o", label=subject,
             color=colors[i], linewidth=2, markersize=5)
ax2.set_title("Subject-wise Score Trends", fontweight="bold", color="#2c3e50")
ax2.set_xlabel("Student")
ax2.set_ylabel("Marks")
ax2.tick_params(axis='x', rotation=45)
ax2.legend(loc="lower right", fontsize=8)
ax2.set_facecolor("#fdfdfd")

# ── Plot 3: Pie Chart – Grade Distribution ──
ax3 = fig.add_subplot(gs[1, 0])
grade_counts = df["Grade"].value_counts()
pie_colors = {"A": "#27ae60", "B": "#f39c12", "C": "#e74c3c", "F": "#95a5a6"}
ax3.pie(grade_counts.values,
        labels=[f"Grade {g}" for g in grade_counts.index],
        autopct="%1.0f%%",
        colors=[pie_colors.get(g, "#bdc3c7") for g in grade_counts.index],
        startangle=90,
        wedgeprops={"edgecolor": "white", "linewidth": 2})
ax3.set_title("Grade Distribution", fontweight="bold", color="#2c3e50")

# ── Plot 4: Horizontal Bar – Subject Averages ──
ax4 = fig.add_subplot(gs[1, 1])
subject_avg = df[subjects].mean().sort_values()
h_bars = ax4.barh(subject_avg.index, subject_avg.values,
                  color=colors, edgecolor="white", linewidth=0.8)
ax4.set_title("Subject-wise Class Average", fontweight="bold", color="#2c3e50")
ax4.set_xlabel("Average Score (%)")
ax4.set_xlim(0, 100)
for bar, val in zip(h_bars, subject_avg.values):
    ax4.text(val + 0.5, bar.get_y() + bar.get_height() / 2,
             f"{val:.1f}", va="center", fontsize=9, fontweight="bold")
ax4.set_facecolor("#fdfdfd")

plt.savefig("output/dashboard.png", dpi=150, bbox_inches="tight")
plt.show()
print("\n✅ Dashboard saved to output/dashboard.png")

# ─────────────────────────────────────────
# 4. EXPORT TO CSV
# ─────────────────────────────────────────
df.to_csv("output/results.csv", index=False)
print("✅ Results exported to output/results.csv")
