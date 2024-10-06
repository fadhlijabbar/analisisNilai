from pyECLAT import ECLAT
from itertools import combinations, chain

# Analisis  
# Fungsi Bikin Rule
def generate_association_rules(rule_supports, min_confidence):
    rules = []

    for key, support in rule_supports.items():
        if ' & ' in key:
            items = key.split(' & ')
            if len(items) > 1:
                subsets = list(chain.from_iterable(combinations(items, r) for r in range(1, len(items))))
                for subset in subsets:
                    antecedent = subset
                    consequent = tuple(set(items) - set(subset))
                    confidence = support / rule_supports[' & '.join(antecedent)]
                    if confidence >= min_confidence:
                        rules.append((antecedent, consequent, confidence, support))
        else:
            pass
    return rules
# End Fungsi Bikin Rule

# Fungsi Cari Rule
def find_rules_within_limits(data, target_rule_count, min_support_range, min_confidence_range):
    min_support, max_support = min_support_range
    min_confidence, max_confidence = min_confidence_range

    step_support = 0.1
    step_confidence = 0.1

    current_support = max_support
    current_confidence = max_confidence

    eclat_instance = ECLAT(data=data, verbose=True)

    while current_support >= min_support:
        while current_confidence >= min_confidence:
            rule_indices, rule_supports = eclat_instance.fit(min_support=current_support, min_combination=1)
            association_rules = generate_association_rules(rule_supports, current_confidence)
            if len(association_rules) >= target_rule_count:
                return association_rules
            current_confidence -= step_confidence
        current_confidence = max_confidence
        current_support -= step_support

    return []
# End Fungsi Cari Rule