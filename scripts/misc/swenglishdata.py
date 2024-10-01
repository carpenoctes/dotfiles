import json

def merge_json(file1, file2):
    with open(file1, 'r') as f1:
        data1 = json.load(f1)
    with open(file2, 'r') as f2:
        data2 = json.load(f2)
    
    def merge_dicts(d1, d2):
        merged = {}
        i=0;
        for key in d1.keys():
            i +=1
            if key in d2.keys():
                if isinstance(d1[key], dict) and isinstance(d2[key], dict):
                    merged[key] = merge_dicts(d1[key], d2[key])
                elif isinstance(d1[key], (int, float)) and isinstance(d2[key], (int, float)):
                    if i<24:
                        merged[key] = (d1[key] + d2[key])/2
                        #print(key)
                    else: 
                        merged[key] = d1[key] + d2[key]
                        #print(key)
                else:
                    merged[key] = d1[key]
            else:
                merged[key] = d1[key]
        for key in d2.keys():
            if key not in d1.keys():
                merged[key] = d2[key]
        return merged
    
    merged_data = merge_dicts(data1, data2)
    return merged_data

def save_to_file(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

file1 = '/home/saddaf/Documents/oxeylyzer/static/language_data/swedish.json'
file2 = '/home/saddaf/Documents/oxeylyzer/static/language_data/english.json'
merged_data = merge_json(file1, file2)
output_file = '/home/saddaf/Documents/oxeylyzer/static/language_data/swenglish.json'
save_to_file(merged_data, output_file)