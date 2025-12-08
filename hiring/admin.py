from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Department, Designation, Employee, HiringRequisition
from import_export import fields
from import_export.widgets import ForeignKeyWidget

# --- Resources for import/export ---
class DepartmentResource(resources.ModelResource):
    class Meta:
        model = Department
        fields = (
            'id',
            'name',
            'page_link',
            'head_email',
            'group_email',
            'external_id',
            'parent_department',
            'department_type',
        )
        import_id_fields = ('name',)


class DesignationResource(resources.ModelResource):
    class Meta:
        model = Designation
        fields = (
            'id',
            'name',
            'department',
            'role_document_link',
            'jd_link',
            'remarks',
            'role_document',
        )
        import_id_fields = ('name',)


class EmployeeResource(resources.ModelResource):
    class Meta:
        model = Employee
        fields = ('id', 'name', 'email', 'department')


class HiringRequisitionResource(resources.ModelResource):
    class Meta:
        model = HiringRequisition
        fields = (
            'serial_no',
            'requisitioner',
            'hiring_dept',
            'designation_status',
            'hiring_designation',
            'new_designation',
            'joining_days',
            'special_instructions',
            'hiring_status',
            'cc_employees',
            'role_n_jd_exist',
            'role_n_jd_read',
            'role_n_jd_good',
            'days_well_thought',
        )


# --- Admin registrations ---
@admin.register(Department)
class DepartmentAdmin(ImportExportModelAdmin):
    resource_class = DepartmentResource
    list_display = ('name', 'department_type', 'head_email', 'group_email', 'page_link')
    search_fields = ('name', 'head_email', 'group_email')
    list_filter = ('department_type',)


@admin.register(Designation)
class DesignationAdmin(ImportExportModelAdmin):
    resource_class = DesignationResource
    list_display = ('name', 'department', 'jd_link', 'role_document_link', 'remarks')
    list_filter = ('department',)
    search_fields = ('name', 'remarks')


@admin.register(Employee)
class EmployeeAdmin(ImportExportModelAdmin):
    resource_class = EmployeeResource
    list_display = ('name', 'email', 'department')
    list_filter = ('department',)
    search_fields = ('name', 'email')


@admin.register(HiringRequisition)
class HiringRequisitionAdmin(ImportExportModelAdmin):
    resource_class = HiringRequisitionResource
    list_display = (
        'serial_no',
        'requisitioner',
        'hiring_dept',
        'designation_status',
        'hiring_designation',
        'new_designation',
        'joining_days',
        'hiring_status',
        'special_instructions',
    )
    list_filter = ('hiring_dept', 'designation_status', 'hiring_status')
    search_fields = ('serial_no', 'hiring_designation', 'new_designation', 'special_instructions')
    ordering = ('-serial_no',)
