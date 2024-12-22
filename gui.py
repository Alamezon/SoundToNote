import customtkinter as ctk
from tkinter import filedialog, messagebox
from musicXML_creator import MusicXmlCreator
import os
import subprocess
import tempfile
from librosa import get_duration
from pydub import AudioSegment


class SoundToNotesApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SoundToNote")
        self.geometry("500x300")
        ctk.set_appearance_mode("System")  # Настройка темной/светлой темы
        ctk.set_default_color_theme("blue")  # Цветовая схема

        self.audio_file = None  # Выбранный аудиофайл
        self.notes = None       # Сгенерированные ноты

        self.create_widgets()

    def create_widgets(self):
        # Заголовок
        self.label = ctk.CTkLabel(
            self, text="Конвертация аудио в ноты", font=ctk.CTkFont(size=20, weight="bold")
        )
        self.label.pack(pady=20)

        # Кнопка "Выбрать аудиофайл"
        self.select_button = ctk.CTkButton(
            self, text="Выбрать аудиофайл", command=self.select_audio_file
        )
        self.select_button.pack(pady=10)

        # Кнопка "Сгенерировать ноты"
        self.generate_button = ctk.CTkButton(
            self, text="Сгенерировать ноты", command=self.generate_notes
        )
        self.generate_button.pack(pady=10)

        # Кнопка "Конвертировать в pdf"
        self.generate_button = ctk.CTkButton(
            self, text="Конвертировать в pdf", command=self.convert_to_pdf
        )
        self.generate_button.pack(pady=10)

    def select_audio_file(self):
        # Выбор аудиофайла через диалоговое окно
        file_path = filedialog.askopenfilename(
            filetypes=[("Audio Files", "*.mp3 *.m4a *.wav")]
        )

        if file_path and self.is_audio_file_valid(file_path):
            self.audio_file = file_path
            messagebox.showinfo("Файл выбран", f"Выбран файл: {file_path}")

    def generate_notes(self):
        if not self.audio_file:
            messagebox.showerror("Ошибка", "Сначала выберите аудиофайл!")
            return

        try:
            # Генерация нот
            self.notes = MusicXmlCreator(self.audio_file).create_mxml()
            if not self.notes:
                messagebox.showinfo("Пустой файл", "Ноты не распознаны.")
                return

            # Сохранение в выбранном формате
            save_path = filedialog.asksaveasfilename(
                filetypes=[("MusicXML File", "*.musicxml")]
            )
            if save_path:
                # Если пользователь не указал расширение, добавляем его автоматически
                if not save_path.endswith(".musicxml"):
                    #if "MusicXML File" in save_path
                    save_path += ".musicxml"

                # Сохранение в правильном формате
                if save_path.endswith(".musicxml"):
                    with open(save_path, 'w') as file:
                        file.write(self.notes)
                else:
                    raise ValueError("Формат файла не поддерживается.")

                messagebox.showinfo("Успех", f"Ноты сохранены в: {save_path}")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def convert_to_pdf(self):

        if not self.audio_file:
            messagebox.showerror("Ошибка", "Сначала выберите аудиофайл!")
            return

        musescore_path = "C:\\Program Files\\MuseScore 4\\bin\\MuseScore4.exe"

        if not os.path.isfile(musescore_path):
            messagebox.showerror("MuseScore не найден", "Для генерации pdf файла требуется программа MuseScore 4.")
            return

        musicxml_data = MusicXmlCreator(self.audio_file).create_mxml()
        if not musicxml_data:
            messagebox.showinfo("Пустой файл", "Ноты не распознаны.")
            return
        #save_path = filedialog.askdirectory(title="Выберите папку для сохранения.")
        save_path = filedialog.asksaveasfilename(
            filetypes=[("Portable Document Format", "*.pdf")]
        )

        # Создаем временный файл
        with tempfile.NamedTemporaryFile(suffix=".musicxml", delete=False) as temp_musicxml_file:
            # Записываем данные в файл
            temp_musicxml_file.write(musicxml_data.encode('utf-8'))
            temp_musicxml_path = temp_musicxml_file.name  # Получаем путь к временному файлу

        # Генерируем имя PDF файла на основе исходного временного файла
        output_pdf_name = os.path.basename(temp_musicxml_path).replace(os.path.basename(temp_musicxml_path), f"{save_path}.pdf")

        # Формируем команду
        command = [
            musescore_path,
            temp_musicxml_path,
            "-o", output_pdf_name
        ]
        try:
            if save_path:
                # Запускаем процесс конвертации
                subprocess.run(command, check=True)
                messagebox.showinfo("Успех", f"Ноты сохранены в: {output_pdf_name}")
            else:
                return
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при создании PDF: {str(e)}")
        finally:
            # Удаляем временный файл
            os.remove(temp_musicxml_path)

    def is_audio_file_valid(self, filepath):
        try:
            # Попытка загрузить файл
            audio = AudioSegment.from_file(filepath)

            # Проверка на пустоту
            if get_duration(filename=filepath) < 1:
                messagebox.showerror("Ошибка", "Файл пустой.")
                return False

            if get_duration(filename=filepath) > 480:
                messagebox.showerror("Ошибка", "Длительность файла превышает 8 минут.")
                return False
            return True

        except:
            messagebox.showerror("Ошибка", "Файл повреждён.")
            return False

if __name__ == "__main__":
    app = SoundToNotesApp()
    app.mainloop()
