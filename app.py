# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import os
from datetime import datetime

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV価格変更ツール")
        self.root.geometry("500x400")

        self.file_path = ""

        # CSV選択
        tk.Button(root, text="CSV選択", command=self.select_file).pack(pady=5)
        self.label = tk.Label(root, text="未選択")
        self.label.pack()

        # 最低価格
        tk.Label(root, text="最低価格（例：800）").pack()
        self.min_price = tk.Entry(root)
        self.min_price.insert(0, "800")
        self.min_price.pack()

        # 割引率
        tk.Label(root, text="割引率（％）").pack()
        self.discount = tk.Entry(root)
        self.discount.insert(0, "10")
        self.discount.pack()

        # 分割件数
        tk.Label(root, text="分割件数（例：50000）").pack()
        self.split_size = tk.Entry(root)
        self.split_size.insert(0, "50000")
        self.split_size.pack()

        # 実行ボタン
        tk.Button(root, text="実行", command=self.run).pack(pady=10)

        # ログ
        self.log = tk.Text(root, height=10)
        self.log.pack()

    def log_msg(self, msg):
        self.log.insert(tk.END, msg + "\n")
        self.log.see(tk.END)

    def select_file(self):
        path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if path:
            self.file_path = path
            self.label.config(text=path)

    def run(self):
        if not self.file_path:
            messagebox.showerror("エラー", "CSVを選択してください")
            return

        try:
            min_price = int(self.min_price.get())
            discount = float(self.discount.get())
            split_size = int(self.split_size.get())
        except:
            messagebox.showerror("エラー", "数値を正しく入力してください")
            return

        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)

        results = []

        with open(self.file_path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                price = int(row["価格"])
                if price >= min_price:
                    new_price = int(price * (1 - discount / 100))
                else:
                    new_price = price

                row["変更後価格"] = new_price
                results.append(row)

        self.log_msg(f"処理件数: {len(results)}件")

        # 分割出力
        for i in range(0, len(results), split_size):
            chunk = results[i:i+split_size]
            filename = f"output_{i//split_size + 1}.csv"
            path = os.path.join(output_dir, filename)

            with open(path, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.DictWriter(f, fieldnames=chunk[0].keys())
                writer.writeheader()
                writer.writerows(chunk)

            self.log_msg(f"出力: {filename}")

        messagebox.showinfo("完了", "処理が完了しました")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()