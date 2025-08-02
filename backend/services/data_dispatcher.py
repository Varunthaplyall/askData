import importlib
import pandas as pd
from typing import Optional
from utils.metric_resolver import resolve_metric

class DataDispatcher:
    def __init__(self, query: dict):
        self.query = query
        self.user_metric = query.get("metric")                     
        self.metric = resolve_metric(self.user_metric)          

    def load_class(self, module_path: str, class_name: str):
        try:
            module = importlib.import_module(module_path)
            return getattr(module, class_name)
        except (ImportError, AttributeError):
            return None

    def try_api(self) -> Optional[pd.DataFrame]:
        module_path = f"backend.data_sources.api.{self.metric}"   
        class_name = f"{self.metric.capitalize()}Fetcher"
        fetcher_class = self.load_class(module_path, class_name)
        if fetcher_class is None:
            return None
        try:
            return fetcher_class().get_data(self.query)
        except Exception:
            return None

    def try_scraper(self) -> Optional[pd.DataFrame]:
        module_path = f"backend.data_sources.scrappers.{self.user_metric}"  
        class_name = f"{self.user_metric.capitalize()}Fetcher"
        fetcher_class = self.load_class(module_path, class_name)
        if fetcher_class is None:
            return None
        try:
            return fetcher_class().get_data(self.query)
        except Exception:
            return None

    def get_data(self) -> Optional[pd.DataFrame]:
        data = self.try_api()
        if data is not None and not data.empty:
            return data
        return None
        # return self.try_scraper()
