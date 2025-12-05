# hiring/views.py  ← FINAL BULLETPROOF VERSION
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.db.models import Max
from django.views.decorators.csrf import csrf_exempt
from .models import Department, Employee, Designation, HiringRequisition
import json


@require_GET
def next_serial(request):
    last = HiringRequisition.objects.aggregate(Max('serial_no'))['serial_no__max']
    next_num = (last or 1000) + 1
    return JsonResponse({'nextSerial': next_num})

@require_GET
def get_departments(request):
    depts = list(Department.objects.values('id', 'name'))
    return JsonResponse(depts, safe=False)

@require_GET
def get_employees(request):
    emps = list(Employee.objects.values('id', 'name', 'email'))
    return JsonResponse(emps, safe=False)

@require_GET
def all_designations(request):
    designations = Designation.objects.all()
    data = [
        {
            "id": d.id,
            "name": d.name,
            "role_link": d.role_document_link,
            "jd_link": d.jd_link,
        }
        for d in designations
    ]
    return JsonResponse(data, safe=False)

@csrf_exempt
def submit_requisition(request):
    if request.method == "POST":
        data = json.loads(request.body)

        requisitioner_id = data.get("requisitioner")
        hiring_dept_id = data.get("hiring_dept")

        req = HiringRequisition.objects.create(
            requisitioner_id=requisitioner_id if requisitioner_id else None,
            hiring_dept_id=hiring_dept_id if hiring_dept_id else None,
            designation_status=data.get("designation_status"),
            hiring_designation=data.get("hiring_designation"),
            new_designation=data.get("new_designation"),
            joining_days=data.get("joining_days"),
            special_instructions=data.get("special_instructions"),
            hiring_status=data.get("hiring_status"),
            cc_employees=data.get("cc_employees"),
            role_n_jd_exist=data.get("role_n_jd_exist"),
            role_n_jd_read=data.get("role_n_jd_read"),
            role_n_jd_good=data.get("role_n_jd_good"),
            days_well_thought=data.get("days_well_thought"),
            role_link=data.get("role_link"),   # ✅ save role link
            jd_link=data.get("jd_link"),       # ✅ save jd link
        )

        return JsonResponse({
                "success": True,
                "id": req.id,
                "serial_no": req.serial_no
            })
