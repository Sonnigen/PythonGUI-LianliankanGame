
# 常用组件示例：

import tkinter as tk
import tkinter.messagebox as msg

class MainWindow():
    def __init__(self):
        # 创建主窗口
        self.window = tk.Tk()
        self.window.minsize(300, 300)
        self.window.title('示例')
        # 定义listbox初始化列表
        self.list_data = ['性感', '可爱', '御姐', '萝莉']
        self.list_data2 = [('性感', 0), ('可爱', 1), ('御姐', 2), ('萝莉', 3)]
        self.radio_selected = tk.IntVar()
        self.scale_value = tk.IntVar()
        # 添加组件
        self.addComponents()
        # 进入消息循环
        self.window.mainloop()

    def addComponents(self):
        my_frame = tk.Frame(self.window)
        my_frame.pack(side=tk.TOP)

        # 创建spinbox
        self.my_spinbox = tk.Spinbox(my_frame, from_=0, to=150)
        self.my_spinbox.pack()
        self.my_spinbox2 = tk.Spinbox(my_frame, values=("苹果", "粒子", "葡萄", "西瓜"))
        self.my_spinbox2.pack()
        # 创建pandedwindow
        my_panedwindow = tk.PanedWindow(orient=tk.VERTICAL)
        my_panedwindow.pack(fill=tk.BOTH)
        my_label = tk.Label(my_panedwindow, text='One paned window')
        my_panedwindow.add(my_label)
        my_text = tk.Text(my_panedwindow, width=20,height=10)
        for i in range(0, 100):
            my_text.insert(tk.END, "我是个帅哥\n")
            my_text.pack()
        my_panedwindow.add(my_text)
        # 创建labelframe
        my_frame4 = tk.LabelFrame(self.window, text="请选择你喜欢的女人")
        my_frame4.pack(side=tk.BOTTOM)
        # 创建messagebox
        msg.showinfo("提示", "人生苦短")
        if msg.askyesno("询问", "你喜欢美女吗"):
            print("是的")
        else:
            print("我是正人君子")

        # # 创建radiobutton
        # for label, value in self.list_data2:
        #     tk.Radiobutton(my_frame, text=label, value=value, variable=self.radio_selected, command=self.radio_clicked).pack()
        #
        # # 创建scale
        # my_scale = tk.Scale(my_frame, from_= 0, to= 100, resolution= 1, orient=tk.HORIZONTAL, variable=self.scale_value)
        # my_scale.pack(side=tk.RIGHT)
        # # 创建scrollbar
        # my_frame3 = tk.Frame(self.window)
        # my_frame3.pack()
        # my_scrollbar = tk.Scrollbar(my_frame3)
        # my_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        # mylistbox = tk.Listbox(my_frame3, yscrollcommand=my_scrollbar.set)
        # for i in range (0, 100):
        #     mylistbox.insert("end", i)
        # mylistbox.pack()
        # my_scrollbar.config(command=mylistbox.yview)
        # # 创建text
        # my_text = tk.Text(my_frame3, width=20, height=3)
        # for i in range(0, 100):
        #     my_text.insert(tk.END, "我是个吃货\n")
        # my_text.pack()



        # # 创建label
        # name = tk.Label(my_frame, text='请选择老婆')
        # name.pack(side=tk.TOP)
        # # 创建listbox
        # self.my_listbox = tk.Listbox(my_frame)
        # self.my_listbox.pack(side=tk.LEFT)
        # for item in self.list_data:
        #     self.my_listbox.insert("end", item)
        # my_button = tk.Button(my_frame, text='选择', command=self.button_clicked)
        # my_button.pack(side=tk.RIGHT)
        # #创建菜单
        # self.menubar = tk.Menu(self.window, bg="lightgrey", fg="black")
        # self.file_new = tk.Menu(self.menubar, bg="lightgrey", fg="black")
        # self.menubar.add_cascade(labe="文件", menu=self.file_new) #添加层级关系
        # self.file_new.add_command(label="新建", command=self.file_new_command, accelerator="Ctrl+N")
        # self.window.config(menu=self.menubar)
        # # 创建菜单按钮
        # my_frame2 = tk.Frame(self.window)
        # my_frame2.pack(side=tk.BOTTOM)
        # menubutton = tk.Menubutton(my_frame2, text='菜单按钮', relief=tk.RAISED)
        # menubutton.pack(side=tk.TOP)
        # filemenu = tk.Menu(menubutton)
        # filemenu.add_command(label="新建", command=self.file_new_command)
        # menubutton.configure(menu=filemenu)
        # # 创建message消息
        # my_message= tk.Message(my_frame2, text='这是一组可以自动换行的文本消息', width=150)
        # my_message.pack()

        # #创建按钮
        # my_button = tk.Button(my_frame, text='点我', command=self.button_clicked)
        # my_button.pack(side=tk.LEFT)
        # #创建canvas
        # my_canvas = tk.Canvas(my_frame, bg='white')
        # my_canvas.create_rectangle(50, 50, 150, 150, outline='red', fill='yellow', width=5)
        # my_canvas.pack(side=tk.RIGHT)
        # # 创建复选框
        # flutter = tk.Checkbutton(my_frame, text='Flutter')
        # flutter.pack(side=tk.TOP)
        # # 创建单行文本
        # name = tk.Label(my_frame, text='姓名')
        # name.pack(side=tk.LEFT)
        # name_value = tk.Entry(my_frame, bd=5)
        # name_value.pack(side=tk.RIGHT)

    def button_clicked(self):
        index = self.my_listbox.curselection()
        if index:
            print(self.list_data[index[0]])
        else:
            print("未选择")

    def radio_clicked(self):
        for item in self.list_data2:
            if self.radio_selected.get() == item[1]:
                print("你喜欢：{}".format(item[0]))

        #  创建顶层窗口
        top = tk.Toplevel()
        top.title('新窗口')
        message = tk.Message(top, text='i loveyou')
        message.pack()

    def file_new_command(self):
        print("新建文件")

if __name__ == '__main__':
    MainWindow()