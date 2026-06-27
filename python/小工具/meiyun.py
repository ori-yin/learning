import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import os

# ==================== 数据处理函数 ====================
def run_analysis(path_df1, path_df2, path_df3):
    # 读取数据
    df1 = pd.read_excel(path_df1)
    df2 = pd.read_excel(path_df2)
    df3 = pd.read_excel(path_df3)

    # df1 透视
    df_pivot1 = df1[
        (df1['审核状态'] == '审核通过') &
        (df1['是否报名'] == '已报名')
    ].pivot_table(
        index='dp_shop_id',
        columns='子活动名称',
        values='new_product_id',
        aggfunc='count',
        fill_value=0
    ).reset_index()

    # df2 透视
    df_pivot2 = df2.pivot_table(
        index='dp_shop_id',
        columns='product_name',
        values='new_product_id',
        aggfunc='count',
        fill_value=0
    ).reset_index()

    pivot1_cols = df_pivot1.columns.drop('dp_shop_id').tolist()
    pivot2_cols = df_pivot2.columns.drop('dp_shop_id').tolist()

    # df3 保留列并合并
    df3_selected = df3[['点评商户ID', '商户类型', 'CPS销售员工ID', 'CPS销售姓名',
                         'CPS销售5级架构', 'CPS销售6级架构', 'CPS销售7级架构',
                         'CPS销售8级架构', '阿波罗品牌名称']]

    result = df3_selected \
        .merge(df_pivot1, left_on='点评商户ID', right_on='dp_shop_id', how='left') \
        .merge(df_pivot2, left_on='点评商户ID', right_on='dp_shop_id', how='left') \
        .drop(columns=['dp_shop_id_x', 'dp_shop_id_y'])

    result[pivot1_cols + pivot2_cols] = result[pivot1_cols + pivot2_cols].fillna(0)

    result['大促是否报名'] = result[pivot1_cols].apply(
        lambda row: '已报名' if row.sum() > 0 else '未报名', axis=1
    )
    result['超团是否报名'] = result[pivot2_cols].apply(
        lambda row: '已报名' if row.sum() > 0 else '未报名', axis=1
    )

    final_cols = ['点评商户ID', '商户类型', 'CPS销售员工ID', 'CPS销售姓名',
                  'CPS销售5级架构', 'CPS销售6级架构', 'CPS销售7级架构',
                  'CPS销售8级架构', '阿波罗品牌名称',
                  '大促是否报名', '超团是否报名'] + pivot1_cols + pivot2_cols
    result = result[final_cols]

    # 筛选KA/CKA
    result_filtered = result[result['CPS销售6级架构'].isin(['KA大区', 'CKA大区'])].copy()
    all_product_cols = pivot1_cols + pivot2_cols


    def build_report(row_cols):
        # 一次groupby拿到所有商品的已报名/未报名
        agg_dict = {}
        for col in all_product_cols:
            agg_dict[(col, '已报名')] = (col, lambda x: (x > 0).sum())
            agg_dict[(col, '未报名')] = (col, lambda x: (x == 0).sum())

        grp = result_filtered.groupby(row_cols, dropna=False).agg(
            **{f"{col}__已报名": (col, lambda x: (x > 0).sum())
               for col in all_product_cols},
            **{f"{col}__未报名": (col, lambda x: (x == 0).sum())
               for col in all_product_cols}
        ).reset_index()

        # 构建多级列
        tuples = [(c, '') for c in row_cols]
        for col in all_product_cols:
            已 = grp[f"{col}__已报名"]
            未 = grp[f"{col}__未报名"]
            总 = 已 + 未
            grp[f"{col}__总计"] = 总
            grp[f"{col}__渗透率"] = (已 / 总 * 100).round(2).astype(str) + '%'
            tuples += [(col, '已报名'), (col, '未报名'), (col, '总计'), (col, '渗透率')]

        # 重排列顺序
        ordered_cols = row_cols.copy()
        for col in all_product_cols:
            ordered_cols += [f"{col}__已报名", f"{col}__未报名",
                             f"{col}__总计", f"{col}__渗透率"]
        grp = grp[ordered_cols]
        grp.columns = pd.MultiIndex.from_tuples(tuples)
        return grp

    final_report = build_report(['CPS销售6级架构', 'CPS销售7级架构', 'CPS销售8级架构', 'CPS销售姓名'])
    final_report2 = build_report(['CPS销售6级架构', 'CPS销售7级架构', 'CPS销售8级架构'])

    # final_report3
    final_report3 = result_filtered.groupby(
        ['CPS销售6级架构', 'CPS销售8级架构'], dropna=False
    ).agg(
        货架大促已报名=('大促是否报名', lambda x: (x == '已报名').sum()),
        超团已报名=('超团是否报名', lambda x: (x == '已报名').sum()),
        总门店数=('点评商户ID', 'count')
    ).reset_index()

    final_report3['货架大促渗透率'] = (
        final_report3['货架大促已报名'] / final_report3['总门店数'] * 100
    ).round(2).astype(str) + '%'
    final_report3['超团渗透率'] = (
        final_report3['超团已报名'] / final_report3['总门店数'] * 100
    ).round(2).astype(str) + '%'
    final_report3 = final_report3[['CPS销售6级架构', 'CPS销售8级架构', '货架大促渗透率', '超团渗透率']]

    return final_report, final_report2, final_report3


# ==================== GUI ====================
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("顽皮小鳄鱼爱洗澡")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        self.root.configure(bg='white')

        self.file_paths = {}
        self.results = None

        tk.Label(root, text="洗呀洗呀", font=("微软雅黑", 14, "bold"),
                 bg='white', fg='black').pack(pady=20)

        self.btn_upload = tk.Button(root, text="上传文件", font=("微软雅黑", 11),
                                    bg='black', fg='white', width=20,
                                    command=self.upload_files)
        self.btn_upload.pack(pady=8)

        self.label_status = tk.Label(root, text="请上传文件", font=("微软雅黑", 9),
                                     bg='white', fg='gray')
        self.label_status.pack()

        self.btn_run = tk.Button(root, text="运行", font=("微软雅黑", 11),
                                 bg='black', fg='white', width=20,
                                 command=self.run)

        self.btn_download = tk.Button(root, text="下载结果", font=("微软雅黑", 11),
                                      bg='black', fg='white', width=20,
                                      command=self.download)

    def upload_files(self):
        files = filedialog.askopenfilenames(
            title="请选择文件",
            filetypes=[("Excel文件", "*.xlsx")]
        )
        if not files:
            return

        name_map = {
            '招商货架原表': 'df1',
            '超级团购原表': 'df2',
            'KACKA商户明细': 'df3'
        }
        self.file_paths = {}
        unrecognized = []
        for f in files:
            basename = os.path.basename(f)
            matched = False
            for key, val in name_map.items():
                if key in basename:
                    self.file_paths[val] = f
                    matched = True
                    break
            if not matched:
                unrecognized.append(basename)

        if unrecognized:
            messagebox.showerror("文件名错误",
                f"以下文件无法识别：\n{chr(10).join(unrecognized)}\n\n"
                f"上传文件名须包含：招商货架原表、超级团购原表、KACKA商户明细")
            self.file_paths = {}
            return

        missing = [k for k in ['df1', 'df2', 'df3'] if k not in self.file_paths]
        if missing:
            missing_names = {'df1': '招商货架原表', 'df2': '超级团购原表', 'df3': 'KACKA商户明细'}
            messagebox.showerror("文件不完整",
                "以下文件未上传：\n" + "\n".join([missing_names[m] for m in missing]))
            return

        self.label_status.config(
            text="✅ 已识别：招商货架原表 / 超级团购原表 / KACKA商户明细",
            fg='green'
        )
        self.btn_run.pack(pady=8)
        self.btn_download.pack_forget()

    def run(self):
        self.btn_run.config(state='disabled')
        self.btn_upload.config(state='disabled')
        self.label_status.config(text="⏳ 运行中，请勿关闭程序...", fg='orange')

        def task():
            try:
                self.results = run_analysis(
                    self.file_paths['df1'],
                    self.file_paths['df2'],
                    self.file_paths['df3']
                )
                self.root.after(0, self.on_run_success)
            except KeyError as e:
                col = str(e).strip("'")
                if 'CPS销售姓名' in col:
                    msg = "KACKA商户明细未找到CPS销售姓名，请检查。"
                else:
                    msg = f"文件列名不匹配，未找到列：{col}，请检查文件内容。"
                self.root.after(0, lambda: self.on_run_error(msg))
            except Exception as e:
                msg = f"运行出错，请联系开发者殷文峰。\n\n错误信息：{str(e)}"
                self.root.after(0, lambda: self.on_run_error(msg))

        threading.Thread(target=task, daemon=True).start()

    def on_run_success(self):
        self.label_status.config(text="✅ 运行完成，请下载结果", fg='green')
        self.btn_run.config(state='normal')
        self.btn_upload.config(state='normal')
        self.btn_download.pack(pady=8)

    def on_run_error(self, msg):
        self.label_status.config(text="❌ 运行出错", fg='red')
        self.btn_run.config(state='normal')
        self.btn_upload.config(state='normal')
        messagebox.showerror("运行错误", msg)

    def download(self):
        if self.results is None:
            return
        save_path = filedialog.asksaveasfilename(
            title="保存文件",
            defaultextension=".xlsx",
            filetypes=[("Excel文件", "*.xlsx")],
            initialfile="跑完啦.xlsx"
        )
        if not save_path:
            return
        try:
            final_report, final_report2, final_report3 = self.results

            def flatten_columns(df):
                df = df.copy()
                df.columns = [
                    f"{a}-{b}" if b else str(a)
                    for a, b in df.columns
                ] if isinstance(df.columns, pd.MultiIndex) else df.columns
                return df

            with pd.ExcelWriter(save_path, engine='openpyxl') as writer:
                flatten_columns(final_report).to_excel(writer, sheet_name='销售明细', index=False)
                flatten_columns(final_report2).to_excel(writer, sheet_name='大区商品明细', index=False)
                final_report3.to_excel(writer, sheet_name='大区渗透率', index=False)
            messagebox.showinfo("下载成功", f"文件已保存至：\n{save_path}")
        except Exception as e:
            messagebox.showerror("下载失败", f"保存失败，请联系殷文峰。\n\n错误信息：{str(e)}")


# ==================== 启动 ====================
if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()