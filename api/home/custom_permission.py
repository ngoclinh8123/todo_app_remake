from rest_framework import permissions


class CustomPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        action = view.action
        if request.user.is_staff is True:
            return True
        alias = {
            "view": ["list", "retrieve"],
            "delete": ["delete", "delete_list"],
            "add": [],
            "change": [],
        }

        # from pprint import pprint
        # pprint(vars(view))

        main_action = view.basename
        # print(main_action)
        for key, value in alias.items():
            if action in value:
                action = key

        permission = f"{action}_{main_action}"

        is_allow = False
        if request.user.user_permissions.filter(codename=permission).count():
            is_allow = True
        if request.user.groups.filter(permissions__codename=permission).count():
            is_allow = True
        return is_allow
