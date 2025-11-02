from itemadapter import ItemAdapter
from datetime import datetime
from pathlib import Path

import json
import os


class InegiPipeline:
    def open_spider(self, spider):
        self.data = []
        spider.logger.info("Pipeline started")

    def process_item(self, item, spider):
        self.data.append(dict(item))
        return item

    # def close_spider(self, spider):
    #     project_root = Path(__file__).resolve().parents[1]
    #     output_path = project_root / "sanctions.json"
 
    #     result = {
    #         "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    #         "":self.data,
    #     }

    #     with open(output_path, "w", encoding="utf-8") as f:
    #         json.dump(result, f, indent=2, ensure_ascii=False)

    #     spider.logger.info(f"{len(self.data)} profile(s) saved: {output_path}")

    def close_spider(self, spider):
        output_file = spider.config.get("output_file", "sanctions.json")
        output_path = os.path.abspath(output_file)

        # JSON dizisine "last_updated" bilgisi ilk eleman olarak eklenecek
        output_data = [{"last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] + self.data

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)

        spider.logger.info(f"{len(self.data)} profile(s) saved: {output_path}")
