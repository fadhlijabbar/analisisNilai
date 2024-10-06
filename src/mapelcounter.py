from fastapi import FastAPI
import pandas as pd
from generaterule import find_rules_within_limits

app = FastAPI()

# Ambil Data Excel
def combine_excel_files(file_paths):
    dataframes = [pd.read_csv(file_path) for file_path in file_paths]
    combined_df = pd.concat(dataframes, ignore_index=True)

    def to_binary(val):
        try:
            return 1 if float(val) >= 84 else 0
        except ValueError:
            return val

    binary_df = combined_df.applymap(to_binary)

    return binary_df

file_paths = [
    'files/data_latih.csv',
]

combined_df = combine_excel_files(file_paths)

result = []

for index, row in combined_df.iterrows():
    row_result = [combined_df.columns[i] for i in range(len(row)) if row[i] == 1]
    if row_result:
        result.append(row_result)

result_df = pd.DataFrame(result)
# End Ambil Data Excel

def generateRule():
    target_rule_count = 10

    min_support_range = (0.2, 0.8)
    min_confidence_range = (0.2, 0.8)

    association_rules = find_rules_within_limits(result_df, target_rule_count, min_support_range, min_confidence_range)

    return association_rules

def analyze_interest(new_data_instance, association_rules):
    interests = set()
    for rule in association_rules:
        antecedent, consequent, confidence, support = rule
        if all(item in new_data_instance for item in antecedent):
            interests.update(consequent)
    return interests

def countMapel(mapel):
    association_rules = generateRule()
    results = {}  # Daftar untuk menyimpan hasil dalam format dictionary

    for mata_pelajaran in mapel:
        analyzed_interests = analyze_interest(mata_pelajaran, association_rules)
        
        # Anggap `new_data_instance` sudah didefinisikan di luar fungsi
        filtered_analyzed_interests = list(set(analyzed_interests))
        
        # Menyimpan hasil ke dalam dictionary dengan nama mata pelajaran sebagai kunci
        results[mata_pelajaran] = filtered_analyzed_interests

    return results

