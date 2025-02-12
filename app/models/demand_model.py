class DemandResult:
    def __init__(self, results_df):
        self.results = results_df
        
    def to_dict(self):
        return {
            'results': self.results.to_dict(orient='records')
        }