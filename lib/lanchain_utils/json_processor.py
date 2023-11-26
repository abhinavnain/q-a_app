import json, uuid, csv, os
class JSONProcessor:
    def __init__(self, json_bytes: bytes, col_list: list) -> None:
        data = json.loads(json_bytes.decode('utf-8'))
        self.file_path = os.path.join('/','tmp', str(uuid.uuid4())+".csv")
        with open(self.file_path, 'w', encoding='utf8',newline='') as csv_file_object:
            csv_writer = csv.writer(csv_file_object)
            csv_writer.writerow(col_list)
            for json_content in data:
                csv_writer.writerow([json_content[cell] for cell in col_list])
            
            


