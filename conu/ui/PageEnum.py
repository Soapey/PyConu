from enum import Enum


class Page(Enum):

    ASSIGNEE_LISTINGVIEW = 0
    ASSIGNEE_ENTRYFORM = 1

    DEPARTMENT_LISTINGVIEW = 2
    DEPARTMENT_ENTRYFORM = 3

    FORM_LISTINGVIEW = 4
    FORM_ENTRYFORM = 5

    PRIORITYLEVEL_LISTINGVIEW = 6
    PRIORITYLEVEL_ENTRYFORM = 7

    SITE_LISTINGVIEW = 8
    SITE_ENTRYFORM = 9

    USER_LISTINGVIEW = 10
    USER_ENTRYFORM = 11

    ITEM_LISTINGVIEW = 12
    ITEM_ENTRYFORM = 13

    SERVICETRACKER_LISTINGVIEW = 14
    SERVICETRACKER_ENTRYFORM = 15

    WORKORDER_LISTINGVIEW = 16
    WORKORDER_ENTRYFORM = 17

    RECURRINGWORKORDER_LISTINGVIEW = 18
    RECURRINGWORKORDER_ENTRYFORM = 19
