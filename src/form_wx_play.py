import os
import wx
import pygame
from player import AudioPlayer

class MyFrame(wx.Frame):
    """
    Класс для создания основного окна приложения.
    """
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        panel = wx.Panel(self)

        self.player = AudioPlayer()

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        # Загрузка иконок для кнопок
        stop_icon = wx.Bitmap("icons/stop.png", wx.BITMAP_TYPE_PNG)
        browse_icon = wx.Bitmap("icons/browse.png", wx.BITMAP_TYPE_PNG)
        play_icon = wx.Bitmap("icons/play.png", wx.BITMAP_TYPE_PNG)
        pause_icon = wx.Bitmap("icons/pause.png", wx.BITMAP_TYPE_PNG)
        resume_icon = wx.Bitmap("icons/resume.png", wx.BITMAP_TYPE_PNG)
        volume_up_icon = wx.Bitmap("icons/volume_up.png", wx.BITMAP_TYPE_PNG)
        volume_down_icon = wx.Bitmap("icons/volume_down.png", wx.BITMAP_TYPE_PNG)
        seek_forward_icon = wx.Bitmap("icons/seek_forward.png", wx.BITMAP_TYPE_PNG)
        seek_backward_icon = wx.Bitmap("icons/seek_backward.png", wx.BITMAP_TYPE_PNG)

        self.play_button = wx.BitmapButton(panel, bitmap=play_icon)
        self.play_button.SetToolTip("Воспроизведение (Ctrl + Enter)")
        self.play_button.SetName("play_button")
        self.play_button.SetLabel("Воспроизведение (Space)")
        self.play_button.Bind(wx.EVT_BUTTON, self.on_play_file)
        self.play_button.Disable()  # Деактивировать кнопку "Воспроизведение"

        self.pause_button = wx.BitmapButton(panel, bitmap=pause_icon)
        self.pause_button.SetToolTip("Пауза (Space)")
        self.pause_button.SetName("pause_button")
        self.pause_button.SetLabel("Пауза (Space)")
        self.pause_button.Bind(wx.EVT_BUTTON, self.on_pause_file)
        self.pause_button.Hide()

        self.resume_button = wx.BitmapButton(panel, bitmap=resume_icon)
        self.resume_button.SetToolTip("Продолжить (Space)")
        self.resume_button.SetName("resume_button")
        self.resume_button.SetLabel("Продолжить (Space)")
        self.resume_button.Bind(wx.EVT_BUTTON, self.on_resume_file)
        self.resume_button.Hide()

        self.stop_button = wx.BitmapButton(panel, bitmap=stop_icon)
        self.stop_button.SetToolTip("Стоп (Ctrl + Space)")
        self.stop_button.SetName("stop_button")
        self.stop_button.SetLabel("Стоп (Ctrl + Space)")
        self.stop_button.Bind(wx.EVT_BUTTON, self.on_stop_file)
        self.stop_button.Disable()  # Деактивировать кнопку "Стоп"

        self.volume_up_button = wx.BitmapButton(panel, bitmap=volume_up_icon)
        self.volume_up_button.SetToolTip("Громче (Ctrl + Up)")
        self.volume_up_button.SetName("volume_up_button")
        self.volume_up_button.SetLabel("Громче (Ctrl + Up)")
        self.volume_up_button.Bind(wx.EVT_BUTTON, self.on_volume_up)
        self.volume_up_button.Disable()  # Деактивировать кнопку "Громче"

        self.volume_down_button = wx.BitmapButton(panel, bitmap=volume_down_icon)
        self.volume_down_button.SetToolTip("Тише (Ctrl + Down)")
        self.volume_down_button.SetName("volume_down_button")
        self.volume_down_button.SetLabel("Тише (Ctrl + Down)")
        self.volume_down_button.Bind(wx.EVT_BUTTON, self.on_volume_down)
        self.volume_down_button.Disable()  # Деактивировать кнопку "Тише"

        self.seek_forward_button = wx.BitmapButton(panel, bitmap=seek_forward_icon)
        self.seek_forward_button.SetToolTip("Перемотка вперёд (Ctrl + Right)")
        self.seek_forward_button.SetName("seek_forward_button")
        self.seek_forward_button.SetLabel("Перемотка вперёд (Ctrl + Right)")
        self.seek_forward_button.Bind(wx.EVT_BUTTON, self.on_seek_forward)
        self.seek_forward_button.Disable()  # Деактивировать кнопку "Перемотка вперёд"

        self.seek_backward_button = wx.BitmapButton(panel, bitmap=seek_backward_icon)
        self.seek_backward_button.SetToolTip("Перемотка назад (Ctrl + Left)")
        self.seek_backward_button.SetName("seek_backward_button")
        self.seek_backward_button.SetLabel("Перемотка назад (Ctrl + Left)")
        self.seek_backward_button.Bind(wx.EVT_BUTTON, self.on_seek_backward)
        self.seek_backward_button.Disable()  # Деактивировать кнопку "Перемотка назад"

        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer.Add(self.play_button, 0, wx.LEFT, 2)
        button_sizer.Add(self.pause_button, 0, wx.ALL, 2)
        button_sizer.Add(self.resume_button, 0, wx.ALL, 2)
        button_sizer.Add(self.stop_button, 0, wx.ALL, 2)
        button_sizer.Add(self.volume_up_button, 0, wx.ALL, 2)
        button_sizer.Add(self.volume_down_button, 0, wx.ALL, 2)
        button_sizer.Add(self.seek_forward_button, 0, wx.ALL, 2)
        button_sizer.Add(self.seek_backward_button, 0, wx.ALL, 2)

        self.sizer.Add(button_sizer, 0, wx.ALL | wx.LEFT, 5)

        self.label = wx.StaticText(
            panel,
            label="Нажмите кнопку для выбора папки или воспроизведения файла"
        )
        self.sizer.Add(self.label, 0, wx.ALL | wx.CENTER, 40)  # Разместить текст на 40 пикселей ниже

        self.listbox = wx.ListBox(panel)
        self.sizer.Add(self.listbox, 1, wx.ALL | wx.EXPAND, 10)

        self.browse_button = wx.BitmapButton(panel, bitmap=browse_icon)
        self.browse_button.SetToolTip("Обзор (Ctrl + B)")
        self.browse_button.SetName("browse_button")
        self.browse_button.SetLabel("Обзор (Ctrl + B)")
        self.browse_button.Bind(wx.EVT_BUTTON, self.on_browse_folder)
        self.sizer.Add(self.browse_button, 0, wx.ALL | wx.CENTER, 5)

        panel.SetSizer(self.sizer)

        # Инициализация pygame для воспроизведения аудио
        pygame.mixer.init()

        self.folder_path = ""
        self.current_file = None

        # Привязка быстрой клавиши "Пробел", "Ctrl + Enter", "Ctrl + Space", "Ctrl + Up", "Ctrl + Down", "Ctrl + Right" и "Ctrl + Left" к кнопкам
        self.Bind(wx.EVT_CHAR_HOOK, self.on_key_press)

    def on_browse_folder(self, event):
        """
        Обработчик события нажатия кнопки для открытия диалогового окна выбора папки.
        """
        with wx.DirDialog(self, "Выберите папку", style=wx.DD_DEFAULT_STYLE) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                self.folder_path = dialog.GetPath()
                self.label.SetLabel(f"Выбранная папка: {self.folder_path}")
                self.listbox.Clear()
                for file_name in os.listdir(self.folder_path):
                    if file_name.endswith(('.mp3', '.wav', '.ogg')):  # Фильтр аудиофайлов
                        self.listbox.Append(file_name)
                if self.listbox.GetCount() > 0:
                    self.listbox.SetSelection(0)  # Перенос фокуса на первый файл списка
                self.play_button.Enable()  # Активировать кнопку "Воспроизведение"
                self.play_button.Show()  # Показать кнопку "Воспроизведение"
                self.listbox.SetFocus()  # Перенос фокуса на listbox
                self.Layout()

    def on_play_file(self, event):
        """
        Обработчик события нажатия кнопки для воспроизведения выбранного аудиофайла.
        """
        selection = self.listbox.GetSelection()
        if selection != wx.NOT_FOUND:
            file_name = self.listbox.GetString(selection)
            self.current_file = os.path.join(self.folder_path, file_name)
            self.player.play(self.current_file)
            self.play_button.Hide()
            self.pause_button.Show()
            self.stop_button.Enable()  # Активировать кнопку "Стоп"
            self.volume_up_button.Enable()  # Активировать кнопку "Громче"
            self.volume_down_button.Enable()  # Активировать кнопку "Тише"
            self.seek_forward_button.Enable()  # Активировать кнопку "Перемотка вперёд"
            self.seek_backward_button.Enable()  # Активировать кнопку "Перемотка назад"
            self.Layout()

    def on_pause_file(self, event):
        """
        Обработчик события нажатия кнопки для паузы воспроизведения аудиофайла.
        """
        self.player.pause()
        self.pause_button.Hide()
        self.resume_button.Show()
        self.Layout()

    def on_resume_file(self, event):
        """
        Обработчик события нажатия кнопки для продолжения воспроизведения аудиофайла.
        """
        self.player.pause()
        self.resume_button.Hide()
        self.pause_button.Show()
        self.Layout()

    def on_stop_file(self, event):
        """
        Обработчик события нажатия кнопки для остановки воспроизведения аудиофайла.
        """
        self.player.stop()
        self.play_button.Show()
        self.pause_button.Hide()
        self.resume_button.Hide()
        self.stop_button.Disable()  # Деактивировать кнопку "Стоп"
        self.volume_up_button.Disable()  # Деактивировать кнопку "Громче"
        self.volume_down_button.Disable()  # Деактивировать кнопку "Тише"
        self.seek_forward_button.Disable()  # Деактивировать кнопку "Перемотка вперёд"
        self.seek_backward_button.Disable()  # Деактивировать кнопку "Перемотка назад"
        self.Layout()

    def on_volume_up(self, event):
        """
        Обработчик события нажатия кнопки для увеличения уровня громкости.
        """
        self.player.volume_up()

    def on_volume_down(self, event):
        """
        Обработчик события нажатия кнопки для уменьшения уровня громкости.
        """
        self.player.volume_down()

    def on_seek_forward(self, event):
        """
        Обработчик события нажатия кнопки для перемотки вперёд.
        """
        self.player.seek(2)  # Перемотка на 2 секунды вперёд

    def on_seek_backward(self, event):
        """
        Обработчик события нажатия кнопки для перемотки назад.
        """
        self.player.seek(-2)  # Перемотка на 2 секунды назад

    def on_key_press(self, event):
        """
        Обработчик события нажатия клавиши.
        """
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_SPACE and not event.ControlDown():
            if self.play_button.IsShown():
                self.on_play_file(None)
            elif self.pause_button.IsShown():
                self.on_pause_file(None)
            elif self.resume_button.IsShown():
                self.on_resume_file(None)
        elif keycode in (wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER) and event.ControlDown():
            self.on_play_file(None)
        elif keycode == ord('B') and event.ControlDown():
            self.on_browse_folder(None)
        elif keycode == wx.WXK_SPACE and event.ControlDown():
            if self.stop_button.IsEnabled():
                self.on_stop_file(None)
        elif keycode == wx.WXK_UP and event.ControlDown():
            self.on_volume_up(None)
        elif keycode == wx.WXK_DOWN and event.ControlDown():
            self.on_volume_down(None)
        elif keycode == wx.WXK_RIGHT and event.ControlDown():
            self.on_seek_forward(None)
        elif keycode == wx.WXK_LEFT and event.ControlDown():
            self.on_seek_backward(None)
        else:
            event.Skip()

def create_window():
    """
    Функция для создания и запуска основного окна приложения.
    """
    app = wx.App(False)
    frame = MyFrame(None, title="Пример с wxPython", size=(400, 400))
    frame.Show(True)
    frame.listbox.SetFocus()  # Переместить фокус на listbox после запуска окна
    app.MainLoop()

# Запуск окна формы
create_window()