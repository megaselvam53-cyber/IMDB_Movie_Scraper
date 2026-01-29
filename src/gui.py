import tkinter as tk
from tkinter import ttk
import pandas as pd
import os
import scrape

CSV_PATH = "csv/imdb_top_250_movies.csv"


def load_data():
    if not os.path.exists(CSV_PATH):
        scrape.scrape_imdb()
    return pd.read_csv(CSV_PATH)


class IMDbGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("IMDb Top 250 Movies")
        self.root.geometry("800x550")

        self.df = load_data()

        title = tk.Label(
            root,
            text="IMDb Top 250 Movies",
            font=("Arial", 16, "bold")
        )
        title.pack(pady=10)

        # 🔍 Search section
        search_frame = tk.Frame(root)
        search_frame.pack(pady=5)

        tk.Label(search_frame, text="Search Movie:").pack(side=tk.LEFT)

        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            width=30
        )
        self.search_entry.pack(side=tk.LEFT, padx=5)

        tk.Button(
            search_frame,
            text="Search",
            command=self.search_movie
        ).pack(side=tk.LEFT)

        tk.Button(
            search_frame,
            text="Reset",
            command=self.reset_table
        ).pack(side=tk.LEFT, padx=5)

        # ⭐ Sort button
        tk.Button(
            root,
            text="Sort by Rating (High → Low)",
            command=self.sort_rating
        ).pack(pady=5)

        # 📋 Table
        frame = tk.Frame(root)
        frame.pack(fill=tk.BOTH, expand=True)

        columns = ("Rank", "Movie", "IMDb Rating")
        self.tree = ttk.Treeview(
            frame,
            columns=columns,
            show="headings"
        )

        for col in columns:
            self.tree.heading(col, text=col)

        self.tree.column("Rank", width=60, anchor="center")
        self.tree.column("Movie", width=480)
        self.tree.column("IMDb Rating", width=120, anchor="center")

        scrollbar = ttk.Scrollbar(
            frame,
            orient=tk.VERTICAL,
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.populate_table(self.df)

    def populate_table(self, data):
        self.tree.delete(*self.tree.get_children())
        for _, row in data.iterrows():
            self.tree.insert(
                "",
                tk.END,
                values=(row["Rank"], row["Movie"], row["IMDb Rating"])
            )

    def search_movie(self):
        keyword = self.search_var.get().lower()
        filtered = self.df[
            self.df["Movie"].str.lower().str.contains(keyword)
        ]
        self.populate_table(filtered)

    def sort_rating(self):
        self.df["IMDb Rating"] = self.df["IMDb Rating"].astype(float)
        sorted_df = self.df.sort_values(
            by="IMDb Rating",
            ascending=False
        )
        self.populate_table(sorted_df)

    def reset_table(self):
        self.populate_table(self.df)


if __name__ == "__main__":
    root = tk.Tk()
    app = IMDbGUI(root)
    root.mainloop()

       