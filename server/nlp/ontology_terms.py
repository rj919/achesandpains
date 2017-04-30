# My NLM API key died the last morning of the hackathon.  This is a quick-and-dirty snomed / rxnorm / icd10 dict 

term_dict = {
    "ulcer": ["SNOMED", "46742003"],
    "vein": ["SNOMED", "29092000"],
    "leg": ["SNOMED", "30021000"],
    "arm": ["SNOMED", "53120007"],
    "finger": ["SNOMED", "7569003"],
    "toe": ["SNOMED", "29707007"],
    "foot": ["SNOMED", "56459004"],
    "hand": ["SNOMED", "85562004"],
    "feet": ["SNOMED", "56459004"],
    "bruise": ["SNOMED", "125667009"],
    "hurt": ["SNOMED", "22253000"],
    "aches": ["SNOMED", "22253000"],
    "ached": ["SNOMED", "22253000"],
    "pain": ["SNOMED", "22253000"],
    "discomfort": ["SNOMED", "22253000"],
    "blister": ["SNOMED", "417237009"],
    "aspirin": ["RXNorm", "1191"],
    "ibuprofen": ["RXNorm", "5640"],
    "advil": ["RXNorm", "5640"],
    "took": ["SNOMED", "416118004"],
    "take": ["SNOMED", "416118004"]
}

conjugated_dict = {}
conjugated_dict.update(**term_dict)

for key in term_dict.keys():
    value = term_dict[key]
    conjugated_dict[key + "s"] = value
    conjugated_dict[key + "d"] = value
    conjugated_dict[key + "ed"] = value