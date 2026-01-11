import flet as ft
import time
import threading


def main(page: ft.Page):
    # === 1. 📱 手机屏幕设置 ===
    page.title = "粉紫计时器"
    page.window_width = 390
    page.window_height = 844
    page.bgcolor = "#FFF0F5"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START

    # === 🎨 颜色定义 ===
    COLOR_PURPLE = "#9370DB"
    COLOR_DEEP_PURPLE = "#4B0082"
    COLOR_PINK = "#FF69B4"

    # ==========================================
    # 2. ⏱️ 秒表功能
    # ==========================================
    stopwatch_running = False
    stopwatch_seconds = 0

    txt_stopwatch = ft.Text("00:00.00", size=60, weight="bold", color=COLOR_DEEP_PURPLE, font_family="monospace")

    def update_stopwatch_thread():
        nonlocal stopwatch_seconds
        while True:
            if stopwatch_running:
                stopwatch_seconds += 0.01
                mins, secs = divmod(int(stopwatch_seconds), 60)
                frac = int((stopwatch_seconds - int(stopwatch_seconds)) * 100)
                txt_stopwatch.value = f"{mins:02d}:{secs:02d}.{frac:02d}"
                page.update()
                time.sleep(0.01)
            else:
                time.sleep(0.1)

    threading.Thread(target=update_stopwatch_thread, daemon=True).start()

    def toggle_stopwatch(e):
        nonlocal stopwatch_running
        stopwatch_running = not stopwatch_running
        if stopwatch_running:
            btn_stopwatch_start.bgcolor = COLOR_PINK
            btn_stopwatch_text.value = "暂停"
            btn_stopwatch_icon.name = ft.icons.PAUSE
        else:
            btn_stopwatch_start.bgcolor = COLOR_PURPLE
            btn_stopwatch_text.value = "开始"
            btn_stopwatch_icon.name = ft.icons.PLAY_ARROW
        page.update()

    def reset_stopwatch(e):
        nonlocal stopwatch_running, stopwatch_seconds
        stopwatch_running = False
        stopwatch_seconds = 0
        txt_stopwatch.value = "00:00.00"
        btn_stopwatch_start.bgcolor = COLOR_PURPLE
        btn_stopwatch_text.value = "开始"
        btn_stopwatch_icon.name = ft.icons.PLAY_ARROW
        page.update()

    # --- 秒表组件 ---
    btn_stopwatch_icon = ft.Icon(ft.icons.PLAY_ARROW, color="white")
    btn_stopwatch_text = ft.Text("开始", color="white", size=18, weight="bold")
    btn_stopwatch_start = ft.Container(
        content=ft.Row([btn_stopwatch_icon, btn_stopwatch_text], alignment=ft.MainAxisAlignment.CENTER),
        bgcolor=COLOR_PURPLE,
        border_radius=30, width=140, height=50,
        on_click=toggle_stopwatch,
        shadow=ft.BoxShadow(blur_radius=10, color=ft.colors.with_opacity(0.5, COLOR_PURPLE), offset=ft.Offset(0, 5))
    )

    btn_stopwatch_reset = ft.Container(
        content=ft.Row(
            [ft.Icon(ft.icons.REFRESH, color=COLOR_PINK), ft.Text("重置", color=COLOR_PINK, size=18)],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        bgcolor="white", border=ft.border.all(2, COLOR_PINK),
        border_radius=30, width=140, height=50,
        on_click=reset_stopwatch
    )

    view_stopwatch = ft.Container(
        padding=20,
        content=ft.Column(
            [
                ft.Container(height=30),
                ft.Text("专注秒表", size=24, color=COLOR_DEEP_PURPLE, weight="bold"),
                ft.Container(height=40),
                ft.Container(
                    content=txt_stopwatch,
                    bgcolor="white", padding=20, border_radius=20,
                    shadow=ft.BoxShadow(blur_radius=10, color="#E6E6FA", offset=ft.Offset(0, 5))
                ),
                ft.Container(height=150),
                ft.Row(
                    [btn_stopwatch_reset, ft.Text("✨", size=30), btn_stopwatch_start],
                    alignment=ft.MainAxisAlignment.CENTER, spacing=15
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

    # ==========================================
    # 3. ⏳ 倒计时功能
    # ==========================================
    timer_running = False
    timer_seconds_left = 0

    input_minutes = ft.TextField(value="25", label="设置分钟", width=100, text_align=ft.TextAlign.CENTER,
                                 border_color=COLOR_PINK, color=COLOR_DEEP_PURPLE, text_size=20)
    txt_timer = ft.Text("00:00", size=50, color=COLOR_DEEP_PURPLE, weight="bold")
    timer_ring = ft.ProgressRing(width=220, height=220, stroke_width=20, color=COLOR_PINK, bgcolor="#FFE4E1", value=0)

    def update_timer_thread():
        nonlocal timer_seconds_left, timer_running
        while True:
            if timer_running and timer_seconds_left > 0:
                time.sleep(1)
                timer_seconds_left -= 1
                mins, secs = divmod(timer_seconds_left, 60)
                txt_timer.value = f"{mins:02d}:{secs:02d}"
                total_time = int(input_minutes.value) * 60
                if total_time > 0:
                    timer_ring.value = timer_seconds_left / total_time
                page.update()
                if timer_seconds_left == 0:
                    timer_running = False
                    btn_timer_container.bgcolor = COLOR_PURPLE
                    btn_timer_text.value = "完成"
                    input_minutes.disabled = False
                    page.update()
            else:
                time.sleep(0.1)

    threading.Thread(target=update_timer_thread, daemon=True).start()

    def toggle_timer(e):
        nonlocal timer_running, timer_seconds_left
        if timer_running:
            timer_running = False
            btn_timer_container.bgcolor = COLOR_PURPLE
            btn_timer_text.value = "继续"
            page.update()
            return

        try:
            if timer_seconds_left == 0:
                mins = int(input_minutes.value)
                timer_seconds_left = mins * 60

            timer_running = True
            btn_timer_container.bgcolor = COLOR_PINK
            btn_timer_text.value = "暂停"
            input_minutes.disabled = True
            page.update()
        except ValueError:
            input_minutes.error_text = "数字"
            input_minutes.update()

    def reset_timer(e):
        nonlocal timer_running, timer_seconds_left
        timer_running = False
        timer_seconds_left = 0
        txt_timer.value = "00:00"
        timer_ring.value = 0
        btn_timer_container.bgcolor = COLOR_PURPLE
        btn_timer_text.value = "开始"
        input_minutes.disabled = False
        page.update()

    # --- 倒计时组件 ---
    btn_timer_text = ft.Text("开始", color="white", size=18, weight="bold")
    btn_timer_container = ft.Container(
        content=ft.Row([ft.Icon(ft.icons.PLAY_ARROW, color="white"), btn_timer_text],
                       alignment=ft.MainAxisAlignment.CENTER),
        bgcolor=COLOR_PURPLE,
        border_radius=30, width=140, height=50,
        alignment=ft.alignment.center,
        on_click=toggle_timer,
        shadow=ft.BoxShadow(blur_radius=10, color=ft.colors.with_opacity(0.5, COLOR_PURPLE), offset=ft.Offset(0, 5))
    )

    btn_timer_reset = ft.Container(
        content=ft.Row(
            [ft.Icon(ft.icons.REFRESH, color=COLOR_PINK), ft.Text("重置", color=COLOR_PINK, size=18)],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        bgcolor="white", border=ft.border.all(2, COLOR_PINK),
        border_radius=30, width=140, height=50,
        on_click=reset_timer
    )

    view_timer = ft.Container(
        padding=20,
        content=ft.Column(
            [
                ft.Container(height=20),
                ft.Text("倒计时", size=24, color=COLOR_DEEP_PURPLE, weight="bold"),
                ft.Container(height=30),
                ft.Row([ft.Text("时长(分):", color=COLOR_DEEP_PURPLE, size=16), input_minutes],
                       alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(height=30),
                ft.Stack([
                    timer_ring,
                    ft.Container(content=txt_timer, alignment=ft.alignment.center, width=220, height=220)
                ], width=220, height=220),
                ft.Container(height=60),
                ft.Row(
                    [btn_timer_reset, ft.Text("⏳", size=30), btn_timer_container],
                    alignment=ft.MainAxisAlignment.CENTER, spacing=15
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

    # === 4. 底部导航栏 -> 顶部标签栏 ===
    # 🌟 修复点：改成了 tab_alignment=ft.TabAlignment.CENTER
    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        indicator_color=COLOR_PINK,
        label_color=COLOR_DEEP_PURPLE,
        unselected_label_color="grey",
        divider_color="transparent",
        # 这里改好了！
        tab_alignment=ft.TabAlignment.CENTER,
        tabs=[
            ft.Tab(text="秒表", icon=ft.icons.TIMER, content=view_stopwatch),
            ft.Tab(text="倒计时", icon=ft.icons.HOURGLASS_BOTTOM, content=view_timer),
        ],
        expand=True
    )

    page.add(tabs)


ft.app(target=main, view=ft.AppView.WEB_BROWSER)