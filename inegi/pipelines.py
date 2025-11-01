from itemadapter import ItemAdapter
import json
import os

class InegiPipeline:
    def open_spider(self, spider):
        self.data = []
        spider.logger.info("Pipeline started (ready to collect data)")

    def process_item(self, item, spider):
        self.data.append(dict(item))
        spider.logger.debug(f"Pipeline item received: {item['Entity_name']}")
        return item

    def close_spider(self, spider):
        output_file = getattr(spider, "output_file", "sanctions.json")
        output_path = os.path.abspath(output_file)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

        spider.logger.info(f"✅ {len(self.data)} profile(s) saved: {output_path}")

