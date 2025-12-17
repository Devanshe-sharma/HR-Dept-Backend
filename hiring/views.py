from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.db.models import Max
import json

from .models import (
    Department,
    Designation,
    Employee,
    HiringRequisition,
    CandidateApplication,
    Onboarding,
    OnboardingUpdate,
)

# -------------------------
# Departments / Employees / Designations
# -------------------------
@require_GET
def get_departments(request):
    depts = list(Department.objects.values('id', 'name'))
    return JsonResponse(depts, safe=False)


@require_GET
def employees(request):
    data = list(Employee.objects.values("id", "name", "email"))
    return JsonResponse(data, safe=False)


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


# -------------------------
# Hiring Requisitions
# -------------------------
@require_GET
def next_serial(request):
    last = HiringRequisition.objects.aggregate(Max('serial_no'))['serial_no__max']
    next_num = (last or 1000) + 1
    return JsonResponse({'nextSerial': next_num})


@require_GET
def all_requisitions(request):
    data = [
        {
            "id": r.id,
            "serial_no": r.serial_no,
            "created_at": r.created_at,
            "requisitioner": {"id": r.requisitioner.id, "name": r.requisitioner.name} if r.requisitioner else None,
            "hiring_dept": {"id": r.hiring_dept.id, "name": r.hiring_dept.name} if r.hiring_dept else None,
            "hiring_designation": r.hiring_designation,
            "new_designation": r.new_designation,
            "hiring_status": r.hiring_status,
        }
        for r in HiringRequisition.objects.all().order_by("-created_at")
    ]
    return JsonResponse(data, safe=False)


@require_http_methods(["GET", "PUT"])
@csrf_exempt
def requisition_detail(request, pk):
    req = get_object_or_404(HiringRequisition, pk=pk)

    if request.method == "GET":
        data = {
            "id": req.id,
            "serial_no": req.serial_no,
            "created_at": req.created_at,
            "requisitioner": {"id": req.requisitioner.id, "name": req.requisitioner.name} if req.requisitioner else None,
            "hiring_dept": {"id": req.hiring_dept.id, "name": req.hiring_dept.name} if req.hiring_dept else None,
            "hiring_designation": req.hiring_designation,
            "new_designation": req.new_designation,
            "hiring_status": req.hiring_status,
            "special_instructions": req.special_instructions,
        }
        return JsonResponse(data)

    if request.method == "PUT":
        data = json.loads(request.body)
        req.hiring_status = data.get("hiring_status", req.hiring_status)
        req.special_instructions = data.get("special_instructions", req.special_instructions)
        req.save()
        return JsonResponse({"success": True, "id": req.id, "serial_no": req.serial_no})


@csrf_exempt
def submit_requisition(request):
    if request.method == "POST":
        data = json.loads(request.body)
        req = HiringRequisition.objects.create(
            requisitioner_id=data.get("requisitioner"),
            hiring_dept_id=data.get("hiring_dept"),
            designation_status=data.get("designation_status"),
            hiring_designation=data.get("hiring_designation"),
            new_designation=data.get("new_designation"),
            joining_days=data.get("joining_days"),
            special_instructions=data.get("special_instructions"),
            hiring_status=data.get("hiring_status", "Open"),
            cc_employees=data.get("cc_employees", ""),
            role_n_jd_exist=data.get("role_n_jd_exist", "No"),
            role_n_jd_read=data.get("role_n_jd_read", "No"),
            role_n_jd_good=data.get("role_n_jd_good", "No"),
            days_well_thought=data.get("days_well_thought", "No"),
            role_link=data.get("role_link"),
            jd_link=data.get("jd_link"),
        )
        return JsonResponse({"success": True, "id": req.id, "serial_no": req.serial_no})


# -------------------------
# Candidate Applications
# -------------------------
@require_GET
def all_candidate_applications(request):
    data = [
        {
            "id": c.id,
            "name": c.name,
            "email": c.email,
            "applied_position": c.applied_position,
            "resume_link": c.resume_link,
            "status": c.status,
            "applied_at": c.applied_at,
            "requisition": c.requisition.serial_no if c.requisition else None,
        }
        for c in CandidateApplication.objects.all().order_by("-applied_at")
    ]
    return JsonResponse(data, safe=False)


@require_http_methods(["GET", "PUT"])
@csrf_exempt
def candidate_application_detail(request, pk):
    app = get_object_or_404(CandidateApplication, pk=pk)

    if request.method == "GET":
        data = {
            "id": app.id,
            "name": app.name,
            "email": app.email,
            "applied_position": app.applied_position,
            "resume_link": app.resume_link,
            "status": app.status,
            "applied_at": app.applied_at,
            "requisition": app.requisition.serial_no if app.requisition else None,
        }
        return JsonResponse(data)

    if request.method == "PUT":
        data = json.loads(request.body)
        app.status = data.get("status", app.status)
        app.save()
        return JsonResponse({"success": True, "id": app.id})


@csrf_exempt
def submit_candidate_application(request):
    if request.method == "POST":
        data = json.loads(request.body)
        app = CandidateApplication.objects.create(
            requisition_id=data.get("requisition"),
            name=data.get("name"),
            email=data.get("email"),
            applied_position=data.get("applied_position"),
            resume_link=data.get("resume_link"),
            status=data.get("status", "Applied"),
        )
        return JsonResponse({"success": True, "id": app.id})


# -------------------------
# Onboarding
# -------------------------
@require_GET
def all_onboardings(request):
    data = [
        {
            "id": o.id,
            "candidate": o.candidate.name,
            "start_date": o.start_date,
            "onboarding_steps": o.onboarding_steps,
            "buddy": o.buddy.name if o.buddy else None,
            "status": o.status,
            "created_at": o.created_at,
        }
        for o in Onboarding.objects.all().order_by("-created_at")
    ]
    return JsonResponse(data, safe=False)


@require_http_methods(["GET", "PUT"])
@csrf_exempt
def onboarding_detail(request, pk):
    ob = get_object_or_404(Onboarding, pk=pk)

    if request.method == "GET":
        data = {
            "id": ob.id,
            "candidate": ob.candidate.name,
            "start_date": ob.start_date,
            "onboarding_steps": ob.onboarding_steps,
            "buddy": ob.buddy.name if ob.buddy else None,
            "status": ob.status,
            "created_at": ob.created_at,
        }
        return JsonResponse(data)

    if request.method == "PUT":
        data = json.loads(request.body)
        ob.status = data.get("status", ob.status)
        ob.onboarding_steps = data.get("onboarding_steps", ob.onboarding_steps)
        ob.save()
        return JsonResponse({"success": True, "id": ob.id})


@csrf_exempt
def submit_onboarding(request):
    if request.method == "POST":
        data = json.loads(request.body)
        ob = Onboarding.objects.create(
            candidate_id=data.get("candidate"),
            start_date=data.get("start_date"),
            onboarding_steps=data.get("onboarding_steps"),
            buddy_id=data.get("buddy"),
            status=data.get("status", "In Progress"),
        )
        return JsonResponse({"success": True, "id": ob.id})


# -------------------------
# Onboarding Updates
# -------------------------
@require_GET
def all_onboarding_updates(request):
    data = [
        {
            "id": u.id,
            "onboarding": u.onboarding.id,
            "updated_by": u.updated_by.name if u.updated_by else None,
            "notes": u.notes,
            "updated_at": u.updated_at,
        }
        for u in OnboardingUpdate.objects.all().order_by("-updated_at")
    ]
    return JsonResponse(data, safe=False)


@require_http_methods(["GET", "PUT"])
@csrf_exempt
def onboarding_update_detail(request, pk):
    update = get_object_or_404(OnboardingUpdate, pk=pk)

    if request.method == "GET":
        data = {
            "id": update.id,
            "onboarding": update.onboarding.id,
            "updated_by": update.updated_by.name if update.updated_by else None,
            "notes": update.notes,
            "updated_at": update.updated_at,
        }
        return JsonResponse(data)

    if request.method == "PUT":
        data = json.loads(request.body)
        update.notes = data.get("notes", update.notes)
        # optionally allow updating the "updated_by" field
        if "updated_by" in data:
            update.updated_by_id = data["updated_by"]
        update.save()
        return JsonResponse({"success": True, "id": update.id})


@csrf_exempt
def submit_onboarding_update(request):
    if request.method == "POST":
        data = json.loads(request.body)
        update = OnboardingUpdate.objects.create(
            onboarding_id=data.get("onboarding"),
            updated_by_id=data.get("updated_by"),
            notes=data.get("notes"),
        )
        return JsonResponse({"success": True, "id": update.id})
