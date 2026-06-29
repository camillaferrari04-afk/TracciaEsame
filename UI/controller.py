import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._rat1 = None
        self._rat2 = None


    #RIEMPIRE DROPDOWN
    def fillDD(self):
        self._view._ddrating1.options.clear()
        for r in self._model.ratings():
            self._view._ddrating2.options.append(ft.dropdown.Option(text=r, data=r, on_click=self.memorat2))
        self._view.update_page()

    #STAMPARE INFO GRAFO
    def handleCreaGrafo(self, e):
        self._view.txt_result.controls.clear()
        if self._rat1 is None:
            self._view.txt_result.controls.append(ft.Text("Devi inserire un range di ratings", color="red", size=18))
            self._view.update_page()
            return

        self.caricamentopagina()

        nodi, archi = self._model.creategraph(self._rat1)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato", color="green", size=18))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {nodi}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {archi}"))

        #STAMPARE INFO AGGIUNTIVE
        self._view.txt_result.controls.append(ft.Text(f"Top 5 archi:"))
        for arco in self._model.getarchimaggiori():
            self._view.txt_result.controls.append(ft.Text(f"Arco: {arco[0]} -> {arco[1]} - Peso {arco[2]["weight"]}"))

        numconn, piulunga = self._model.getcompconnessa()
        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {numconn} componenti connesse"))
        self._view.txt_result.controls.append(ft.Text(f"La piu grande componente connessa è lunga {len(piulunga)}"))
        for i in piulunga:
            self._view.txt_result.controls.append(ft.Text(f"{i}"))

        #RIATTIVARE COMANDI SUCCESSIVI
        self._view._btnCammino.disabled=False
        self._view.update_page()


    def handleCammino(self, e):
        self._view.txt_result.controls.clear()

        #HANDLE RICORSIONE
        self.caricamentopagina()
        costo, percorso = self._model.percorsoottimo()

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Percorso piu lungo({costo}) trovato", color="green", size=18))
        for i in percorso:
            self._view.txt_result.controls.append(ft.Text(f"{i}"))
        self._view.update_page()

    #MEMORIZZARE ELEMENTI DROPDOWN
    def memorat1(self, e):
        self._rat1 = e.control.data


    #FUNZIONE DI CARICAMENTO
    def caricamentopagina(self):
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Caricamento..."))
        self._view.update_page()
