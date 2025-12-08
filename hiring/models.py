# hiring/models.py
from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=150, verbose_name="Department")
    page_link = models.URLField(blank=True, null=True, verbose_name="Dept Page Link (BO Internal Site)")
    head_email = models.EmailField(blank=True, null=True, verbose_name="Dept Head Email")
    group_email = models.EmailField(blank=True, null=True, verbose_name="Dept Group Email")
    external_id = models.CharField(max_length=50, blank=True, null=True, verbose_name="External Id")
    parent_department = models.CharField(max_length=100, blank=True, null=True, verbose_name="Parent Department")
    department_type = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        choices=[("Delivery", "Delivery"), ("Support", "Support")],
        verbose_name="Department Type"
    )

    class Meta:
        verbose_name = "Department"
        verbose_name_plural = "Departments"

    def __str__(self):
        return self.name


class Designation(models.Model):
    name = models.CharField(max_length=150, verbose_name="Designation")
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    role_document_link = models.URLField(blank=True, null=True)
    jd_link = models.URLField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    role_document = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Designation"
        verbose_name_plural = "Designations"

    def __str__(self):
        if self.department:
            return f"{self.name} ({self.department.name})"
        return self.name


class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Employee"
        verbose_name_plural = "Employees"

    def __str__(self):
        return f"{self.name} ({self.email})"


class HiringRequisition(models.Model):
    STATUS_CHOICES = [
        ("Open", "Open"),
        ("Closed", "Closed"),
        ("On Hold", "On Hold"),
    ]

    DESIGNATION_STATUS_CHOICES = [
        ("Existing Designation", "Existing Designation"),
        ("New Designation", "New Designation"),
    ]

    serial_no = models.IntegerField(unique=True, blank=True, null=True)

    requisitioner = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="requisitions",
        null=True,
        blank=True
    )
    hiring_dept = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="requisitions",
        null=True,
        blank=True
    )

    designation_status = models.CharField(
        max_length=50,
        choices=DESIGNATION_STATUS_CHOICES,
        default="Existing Designation"
    )
    hiring_designation = models.CharField(max_length=150, blank=True, default="")
    new_designation = models.CharField(max_length=150, blank=True, default="")
    joining_days = models.CharField(max_length=50, blank=True, default="30 Days")
    special_instructions = models.TextField(blank=True, default="")
    hiring_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Open")
    role_link = models.URLField(blank=True, null=True)
    jd_link = models.URLField(blank=True, null=True)

    cc_employees = models.TextField(blank=True, default="")
    role_n_jd_exist = models.CharField(max_length=3, default="No")
    role_n_jd_read = models.CharField(max_length=3, default="No")
    role_n_jd_good = models.CharField(max_length=3, default="No")
    days_well_thought = models.CharField(max_length=3, default="No")

    class Meta:
        verbose_name = "Hiring Requisition"
        verbose_name_plural = "Hiring Requisitions"

    def save(self, *args, **kwargs):
        if not self.serial_no:
            last = HiringRequisition.objects.order_by("-serial_no").first()
            self.serial_no = (last.serial_no + 1) if last else 1001
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Req {self.serial_no}"
