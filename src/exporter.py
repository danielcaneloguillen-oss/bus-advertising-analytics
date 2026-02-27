import pandas as pd

class ReportExporter:
    def __init__(self, data):
        self.data = data

    def export_to_excel(self, filename):
        df = pd.DataFrame(self.data)
        df.to_excel(filename, index=False)
