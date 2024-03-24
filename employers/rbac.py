
from django.contrib.auth.models import User
from rbac.models import RBACRole, RBACPermission

# Create roles
admin_role = RBACRole.objects.create(name='Admin')
manager_role = RBACRole.objects.create(name='Manager')

# Create permissions
can_view_all_reports = RBACPermission.objects.create(name='Can view all reports')
can_edit_all_reports = RBACPermission.objects.create(name='Can edit all reports')
can_view_summary_report = RBACPermission.objects.create(name='Can view summary report')
can_view_daily_report = RBACPermission.objects.create(name='Can view daily report')
can_edit_daily_report = RBACPermission.objects.create(name='Can edit daily report')
can_view_old_reports = RBACPermission.objects.create(name='Can view old reports (current month)')

# Assign permissions to roles
admin_role.permissions.add(can_view_all_reports, can_edit_all_reports, can_view_summary_report)
manager_role.permissions.add(can_view_daily_report, can_edit_daily_report, can_view_old_reports)

# Assign roles to users
admin_user = User.objects.get(username='Admin')
admin_user.roles.add(admin_role)

manager_user = User.objects.get(username='Manager')
manager_user.roles.add(manager_role)


def has_permission(user, permission_name):
    return user.roles.filter(permissions__name=permission_name).exists()
