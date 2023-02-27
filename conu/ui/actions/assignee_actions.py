from conu.ui.PageEnum import Page
from conu.classes.Assignee import Assignee
from conu.db.SQLiteConnection import select_by_attrs_dict
from conu.helpers import navigate, load_entities_into_table


def load_listingview(main_window):
        
    entities = list(select_by_attrs_dict(Assignee).values())

    main_window.ui.assignee_listingview_txtSearch.clear()

    load_entities_into_table(main_window.ui.assignee_listingview_tblAssignee, entities, {"id": "ID", "name": "Name", "description": "Description"})

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
    print("edit")


def delete(main_window):
    print("delete")


def save(main_window):
    print("save")


def back(main_window):

    clear_entryform(main_window)

    navigate(main_window, Page.ASSIGNEE_LISTINGVIEW)


def connect(main_window):
        
    main_window.ui.assignee_listingview_btnNew.clicked.connect(lambda: new(main_window))
    main_window.ui.assignee_listingview_btnEdit.clicked.connect(lambda: edit(main_window))
    main_window.ui.assignee_listingview_btnDelete.clicked.connect(lambda: delete(main_window))
    main_window.ui.assignee_entryform_btnSave.clicked.connect(lambda: save(main_window))
    main_window.ui.assignee_entryform_btnBack.clicked.connect(lambda: back(main_window))