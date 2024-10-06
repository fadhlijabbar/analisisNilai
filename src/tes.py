# import pandas as pd
# from generaterule import find_rules_within_limits

# def avgNilaiCounter(file_path):
#     data = pd.read_excel(file_path)
#     numeric_data = data.select_dtypes(include=['number'])
#     all_values = numeric_data.values.flatten()
#     all_values = all_values[~pd.isnull(all_values)]
#     rata_rata_total = all_values.mean()
#     avgNilai = round(rata_rata_total)

#     return avgNilai


# file_path = 'files/data_latih.xlsx'
# avgNilai = avgNilaiCounter(file_path)

# # Ambil Data CSV
# df = pd.read_excel('files/data_latih.xlsx')


# def to_binary(val):
#     try:
#         return 1 if float(val) >= avgNilai else 0
#     except ValueError:
#         return val

# binary_df = df.applymap(to_binary)

# result = []

# for index, row in binary_df.iterrows():
#     row_result = [binary_df.columns[i] for i in range(len(row)) if row[i] == 1]
#     if row_result:
#         result.append(row_result)

# result_df = pd.DataFrame(result)
# # End Ambil Data CSV

# target_rule_count = 10

# min_support_range = (0.2, 0.8)
# min_confidence_range = (0.2, 0.8)

# association_rules = find_rules_within_limits(result_df, target_rule_count, min_support_range, min_confidence_range)

# # for rule in association_rules:
# #     antecedent, consequent, confidence, lift, support = rule
# #     print(f"Rule: {antecedent} -> {consequent}, Confidence: {round(confidence, 5)}, Support: {round(support, 5)}, Lift: {round(lift, 5)}")

# import pandas as pd

# def analyze_interest(new_data_instance, association_rules):
#     interests = set()
#     results = []
    
#     for rule in association_rules:
#         antecedent, consequent, confidence, lift, support = rule
#         if all(item in new_data_instance for item in antecedent):
#             print(f"Rule: {antecedent} -> {consequent}, Confidence: {round(confidence, 5)}, Support: {round(support, 5)}, Lift: {round(lift, 5)}")
#             interests.update(consequent)
            
#             # Append rule details to results
#             results.append([antecedent, consequent, round(support, 5), round(confidence, 5), round(lift, 5)])
    
#     return interests, results

# def save_results_to_excel(results_list, filename='files/association_rules.xlsx'):
#     # Create a DataFrame from results_list
#     df = pd.DataFrame(results_list, columns=['Antecedent', 'Consequent', 'Support', 'Confidence', 'Lift'])
    
#     # Save the DataFrame to an Excel file
#     df.to_excel(filename, index=False)
#     print(f"Association rules saved to {filename}")

# # Example usage
# dataUji = pd.read_excel('files/data_ujiBaru2.xlsx')
# binary_dataUji = dataUji.applymap(to_binary)

# # List to store all results
# all_results = []

# for _, dataNilaiRow in binary_dataUji.iterrows():
#     new_data_instance = [binary_dataUji.columns[i] for i in range(len(dataNilaiRow)) if dataNilaiRow[i] == 1]
#     analyzed_interests, results = analyze_interest(new_data_instance, association_rules)
#     filtered_analyzed_interests = list(set(analyzed_interests) | set(new_data_instance))
    
#     # Add results to all_results
#     all_results.extend(results)
    
#     # Add a blank row to separate different sets of results
#     all_results.append([''] * 5)

# # Save all results to an Excel file
# save_results_to_excel(all_results)

from analysisresult import analysisProcess

analisis = analysisProcess("BIN")

print(analisis)