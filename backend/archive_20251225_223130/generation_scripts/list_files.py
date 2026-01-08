#!/usr/bin/env python3
import os
import json

drawings_dir = r"c:\Users\larochej3\Desktop\raven-shop-automation\backend\drawings"
output_file = r"c:\Users\larochej3\Desktop\raven-shop-automation\backend\files_list.json"

files_info = {
    "total_pdfs": 0,
    "test_1_pdfs": [],
    "all_files": []
}

if os.path.exists(drawings_dir):
    for fname in os.listdir(drawings_dir):
        fpath = os.path.join(drawings_dir, fname)
        if os.path.isfile(fpath):
            fsize = os.path.getsize(fpath)
            files_info["all_files"].append({
                "name": fname,
                "size_bytes": fsize,
                "size_kb": fsize / 1024
            })
            
            if fname.endswith('.pdf'):
                files_info["total_pdfs"] += 1
                if 'Test_1' in fname or 'test_1' in fname.lower():
                    files_info["test_1_pdfs"].append(fname)

with open(output_file, 'w') as f:
    json.dump(files_info, f, indent=2)

print(f"Files listed to: {output_file}")
print(f"Total PDFs: {files_info['total_pdfs']}")
print(f"Test_1 PDFs: {len(files_info['test_1_pdfs'])}")
