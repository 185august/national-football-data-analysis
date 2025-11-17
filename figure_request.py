class figure_request:
    def __init__(self, figure_name, figure_data):
        self.figure_name = figure_name
        self.figure_data = figure_data

    def to_dict(self):
        return {
            "figure_name": self.figure_name,
            "figure_data": self.figure_data
        }