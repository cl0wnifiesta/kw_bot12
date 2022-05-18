def convert_dict_of_df_to_list(category, df_dict):
    result = []
    values_list = list(df_dict.values())
    row_count = len(values_list[0])
    for i in range(row_count):
        temp = [str(category)]
        for element in values_list:
            temp.append(str(element[i]))
        result.append(tuple(temp))
    return result
