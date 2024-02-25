class ControlObject:
    tabs = None
    new_dialog = None

    def add_new_note(self, text):
        self.tabs.add_tab(text, "")
        #Cria no banco de dados


Control = ControlObject()