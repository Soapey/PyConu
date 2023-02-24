from conu.db.SQLiteConnection import save_by_list, delete_by_attrs_dict, select_by_attrs_dict
from conu.classes.Department import Department
from pprint import pprint as pp

if __name__ == "__main__":
    
    entities = list()
    for i in range(500):
        entities.append(Department('test_department', True))
    
    save_by_list(entities)

    pp(select_by_attrs_dict(Department, {'name': 'test_department'}))

    delete_by_attrs_dict(Department, {'name': 'test_department'})

    pp(select_by_attrs_dict(Department, {'name': 'test_department'}))