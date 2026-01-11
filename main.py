import flet as ft
import time
import threading

def main(page: ft.Page):
    # --- 1. 页面基础设置 ---
    page.title = "粉紫计时器"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    # 设置手机端的窗口大小适配（可选，打包时会自动全屏）
    page.window_width = 390
    page.window_height = 844
    
    # 定义一些颜色变量，还原你的截图风格
    THEME_COLOR = ft.colors.PURPLE
    BG_COLOR = ft.colors.PINK_50
    RING_COLOR = ft.colors.PINK_300
    
    page.bgcolor = BG_COLOR

    # --- 2. 倒计时功能的逻辑与组件 (Tab 1) ---
    
    # 状态变量
    countdown_seconds = 30 * 60  # 默认30分钟
    is_countdown_running = False

    # 倒计时显示文本
    countdown_text = ft.Text(
        value="30:00",
        size=50,
        weight=ft.FontWeight.BOLD,
        color=ft.colors.PURPLE_900
    )

    # 进度圆环
    progress_ring = ft.ProgressRing(
        width=250,
        height=250,
        stroke_width=20,
        value=1.0, # 初始满格
        color=RING_COLOR,
        bgcolor=ft.colors.WHITE
    )

    # 输入框（设置分钟）
    input_minutes = ft.TextField(
        label="设置分钟",
        value="30",
        width=100,
        text_align=ft.TextAlign.CENTER,
        keyboard_type=ft.KeyboardType.NUMBER
    )

    # 倒计时核心函数
    def run_countdown():
        nonlocal countdown_seconds, is_countdown_running
        total_time = int(input_minutes.value) * 60
        current_time = total_time
        
        while current_time > 0 and is_countdown_running:
            mins, secs = divmod(current_time, 60)
            countdown_text.value = "{:02d}:{:02d}".format(mins, secs)
            # 更新进度条 (倒着走)
            progress_ring.value = current_time / total_time
            page.update()
            time.sleep(1)
            current_time -= 1
        
        if is_countdown_running: # 如果是自然结束
            countdown_text.value = "00:00"
            progress_ring.value = 0
            start_btn.text = "开始专注"
            is_countdown_running = False
            # 发个通知或震动（手机端支持）
            page.snack_bar = ft.SnackBar(ft.Text("专注结束！"))
            page.snack_bar.open = True
            page.update()

    def toggle_countdown(e):
        nonlocal is_countdown_running
        if not is_countdown_running:
            # 开始
            try:
                mins = int(input_minutes.value)
                countdown_seconds = mins * 60
            except ValueError:
                input_minutes.value = "30"
                return
            
            is_countdown_running = True
            start_btn.text = "停止"
            start_btn.bgcolor = ft.colors.RED_300
            # 开启线程运行倒计时，防止卡死界面
            threading.Thread(target=run_countdown, daemon=True).start()
        else:
            # 停止
            is_countdown_running = False
            start_btn.text = "开始专注"
            start_btn.bgcolor = ft.colors.PURPLE_300
        
        page.update()

    start_btn = ft.ElevatedButton(
        text="开始专注",
        width=150,
        height=50,
        style=ft.ButtonStyle(
            bgcolor=ft.colors.PURPLE_300,
            color=ft.colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=20),
        ),
        on_click=toggle_countdown
    )

    # 倒计时页面的布局容器
    tab1_content = ft.Column(
        [
            ft.Text("倒计时", size=24, weight="bold", color=THEME_COLOR),
            ft.Container(height=20),
            ft.Row([ft.Text("时长(分):"), input_minutes], alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(height=30),
            # 堆叠布局：把文字放在圆环中间
            ft.Stack(
                [
                    progress_ring,
                    ft.Container(
                        content=countdown_text,
                        alignment=ft.alignment.center,
                        width=250,
                        height=250
                    )
                ],
                width=250,
                height=250,
            ),
            ft.Container(height=40),
            start_btn
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO
    )

    # --- 3. 秒表功能的逻辑与组件 (Tab 2) ---

    stopwatch_running = False
    elapsed_time = 0.0

    stopwatch_text = ft.Text(
        value="00:00.00",
        size=60,
        weight=ft.FontWeight.BOLD,
        color=ft.colors.INDIGO_900,
        font_family="monospace" # 等宽字体防止数字跳动
    )

    def run_stopwatch():
        nonlocal elapsed_time
        start_time = time.time() - elapsed_time
        while stopwatch_running:
            elapsed_time = time.time() - start
