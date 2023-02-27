from conu.ui.PageEnum import Page
from conu.classes.Assignee import Assignee
from conu.db.SQLiteConnection import select_by_attrs_dict, delete_by_attrs_dict, save_by_list
from conu.helpers import navigate, load_entities_into_table, selected_row_id
from tkinter.messagebox import askyesno


def load_listingview(main_window):
    
    global global_assignees
    global_assignees = select_by_attrs_dict(Assignee)

    main_window.ui.assignee_listingview_txtSearch.clear()

    entities_by_search(main_window, None)

    navigate(main_window, Page.ASSIGNEE_LISTINGVIEW)


def clear_entryform(main_window):
        
    main_window.ui.assignee_entryform_lblId.clear()
    main_window.ui.assignee_entryform_txtName.clear()
    main_window.ui.assignee_entryform_txtDescription.clear()

def new(main_window):

    clear_entryform(main_window)

    main_window.ui.assignee_entryform_txtName.setFocus()

    navigate(main_window, Page.ASSIGNEE_ENTRYFORM)

def edit(main_window):

    selected_id = selected_row_id(main_window.ui.assignee_listingview_tblAssignee)

    global global_assignees
    entity = global_assignees[selected_id]

    main_window.ui.assignee_entryform_lblId.setText(str(entity.id))
    main_window.ui.assignee_entryform_txtName.setText(entity.name)
    main_window.ui.assignee_entryform_txtDescription.setPlainText(entity.description)

    main_window.ui.assignee_entryform_txtName.setFocus()

    navigate(main_window, Page.ASSIGNEE_ENTRYFORM)


def delete(main_window):

    if not askyesno("Confirm delete", "Are you sure you would like to delete the selected record?"):
        return

    selected_id = selected_row_id(main_window.ui.assignee_listingview_tblAssignee)

    global global_assignees
    entity = global_assignees[selected_id]

    delete_by_attrs_dict(Assignee, {"id": entity.id})

    load_listingview(main_window)


def save(main_window):
    
    if not askyesno("Confirm save", "Are you sure you would like to save the current record?"):
        return
    
    entity = Assignee(
        main_window.ui.assignee_entryform_txtName.text(),
        main_window.ui.assignee_entryform_txtDescription.toPlainText(),
        None if len(main_window.ui.assignee_entryform_lblId.text()) == 0 else int(main_window.ui.assignee_entryform_lblId.text())
    )

    save_by_list([entity])

    load_listingview(main_window)

    clear_entryform(main_window)


def back(main_window):

    clear_entryform(main_window)

    navigate(main_window, Page.ASSIGNEE_LISTINGVIEW)


def entities_by_search(main_window, search_text):

    global global_assignees

    if not search_text:
        matches = list(global_assignees.values())
    else:
        matches = list(filter(lambda e: search_text in "".join([str(e.id), e.name.lower(), e.description.lower()]), global_assignees.values()))

    load_entities_into_table(main_window.ui.assignee_listingview_tblAssignee, matches, {"id": "ID", "name": "Name", "description": "Description"})
    

def connect(main_window):
        
    main_window.ui.assignee_listingview_btnNew.clicked.connect(lambda: new(main_window))
    main_window.ui.assignee_listingview_btnEdit.clicked.connect(lambda: edit(main_window))
    main_window.ui.assignee_listingview_btnDelete.clicked.connect(lambda: delete(main_window))
    main_window.ui.assignee_entryform_btnSave.clicked.connect(lambda: save(main_window))
    main_window.ui.assignee_entryform_btnBack.clicked.connect(lambda: back(main_window))

    main_window.ui.assignee_listingview_txtSearch.textChanged.connect(
        lambda: entities_by_search(main_window, main_window.ui.assignee_listingview_txtSearch.text().lower())
    )