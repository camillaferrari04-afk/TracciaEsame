import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff

        #DROPDOWN
        self._ddrating1 = ft.Dropdown(label="Voto", hint_text="Rating")
        self._controller.fillDDsRating()

        #BUTTON
        self._btnCreaGrafo = ft.ElevatedButton(text="Crea Grafo", on_click=self._controller.handleCreaGrafo)
        self._btnCammino = ft.ElevatedButton(text="Trova Cammino", on_click=self._controller.handleCammino,
                                             disabled=True)

        #ROWS
        row1 = ft.Row([self._ddrating1,self._ddrating2, self._btnCreaGrafo], alignment=ft.MainAxisAlignment.CENTER,
                      vertical_alignment=ft.CrossAxisAlignment.END)
        row2 = ft.Row([self._btnCammino],
                      alignment=ft.MainAxisAlignment.CENTER)

        self._page.controls.append(row1)
        self._page.controls.append(row2)


        # SPAZIO PER OUTPUT
        self.txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self.txt_result)

        #RICORDATI DI AGGIORNARE LA PAGINA
        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()
