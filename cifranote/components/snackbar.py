import flet as ft

class CustomSnackBar(ft.SnackBar):
    def popup(self, text, action="Ok"):
        self.content.value = text
        self.action = action
        self.open = True
        self.update()

def create_page_snackbar(page: ft.Page):
    snack_bar = CustomSnackBar(
        content=ft.Text(""),
        action="Ok!"
    )
    page.snack_bar = snack_bar