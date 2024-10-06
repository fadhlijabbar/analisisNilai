import pandas as pd
from generaterule import find_rules_within_limits

# Ambil Data CSV
df = pd.read_excel('files/data_latih.xlsx')

def to_binary(val):
    try:
        return 1 if float(val) >= 84 else 0
    except ValueError:
        return val

binary_df = df.applymap(to_binary)

result = []

for index, row in binary_df.iterrows():
    row_result = [binary_df.columns[i] for i in range(len(row)) if row[i] == 1]
    if row_result:
        result.append(row_result)

result_df = pd.DataFrame(result)
# End Ambil Data CSV

# Proses Analisis
def analysisProcess(new_data_instance):
    target_rule_count = 10

    min_support_range = (0.2, 0.8)
    min_confidence_range = (0.2, 0.8)

    association_rules = find_rules_within_limits(result_df, target_rule_count, min_support_range, min_confidence_range)

    def analyze_interest(new_data_instance, association_rules):
        print("Data Ins: ", new_data_instance)
        interests = set()
        for rule in association_rules:
            antecedent, consequent, confidence, support = rule
            print(f"Rule: If {antecedent} then {consequent} with confidence {confidence} and support {support}")
            if all(item in new_data_instance for item in antecedent):
                interests.update(consequent)
        return interests

    analyzed_interests = analyze_interest(new_data_instance, association_rules)
    print(analyzed_interests)

    filtered_analyzed_interests =   list(set(analyzed_interests) | set(new_data_instance))

    return filtered_analyzed_interests
# End Process Analisis


