from datetime import datetime

import json
import os


class InegiPipeline:
    def open_spider(self, spider):
        self.data = []
        spider.logger.info("Pipeline started")

    def process_item(self, item, spider):
        self.data.append(dict(item))
        return item

    def close_spider(self, spider):
            output_file = spider.config.get("output_file", "sanctions.json")
            output_path = os.path.abspath(output_file)

            utc_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
            output_data = [{"last_updated": utc_time}] + self.data

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)

            spider.logger.info(f"{len(self.data)} profile(s) saved: {output_path}")