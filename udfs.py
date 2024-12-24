import pandas as pd

def req_finder(requirements, student):
    cols = ['choice_list_1','choice_list_2','choice_list_3','choice_list_4','choice_list_5']
    
    filtered_requirements = requirements[requirements['required_courses'].apply(lambda x: any(item in student for item in x))]
    filtered_requirements = filtered_requirements.copy()
    filtered_requirements['required_courses'] = filtered_requirements['required_courses'].apply(tuple)

    overall_list = filtered_requirements.copy()

    for col_name in cols:
        overall_list = req_finder_helper(requirements, overall_list, col_name, student)
        overall_list = overall_list.copy()
        overall_list[col_name] = overall_list[col_name].apply(tuple)
        
    overall_tuples = overall_list.apply(lambda col: col.map(lambda x: tuple(x) if isinstance(x, list) else x))
    overall_no_dupes = overall_tuples.drop_duplicates()

    return overall_no_dupes

def req_finder_helper(requirements, data, list_name, student):
    filtered_choice_list = requirements[requirements[list_name].apply(lambda x: any(item in student for item in x))]
    filtered_choice_list = filtered_choice_list.copy()
    filtered_choice_list[list_name] = filtered_choice_list[list_name].apply(tuple)
    filtered_courses = pd.concat([filtered_choice_list, data])
    return filtered_courses

def completion_separator(student_courses, student):
    cols = ['choice_list_1','choice_list_2','choice_list_3','choice_list_4','choice_list_5']
    
    student_courses['completed_required_courses'] = student_courses['required_courses'].apply(lambda x: tuple(value for value in x if value in student))
    student_courses['remaining_required_courses'] = student_courses['required_courses'].apply(lambda x: tuple(value for value in x if value not in student))

    for col_name in cols:
        student_courses = completion_separator_choice_helper(student_courses,col_name, student)
        student_courses = student_courses.drop(columns={col_name, col_name+'_num'})

    return student_courses

def completion_separator_choice_helper(data, list_name, student):
    data['completed_'+list_name] = data[list_name].apply(lambda x: tuple(value for value in x if value in student))
    data['remaining_'+list_name] = data[list_name].apply(lambda x: tuple(value for value in x if value not in student))

    data[list_name+'_num_completed'] = data['completed_'+list_name].apply(lambda x: 0 if x == () else len(x))
    data[list_name+'_num_remaining'] = data[list_name+'_num'] - data[list_name+'_num_completed']
    data[list_name+'_num_remaining'] = data[list_name+'_num_remaining'].apply(lambda x: max(x, 0))
    
    return data

