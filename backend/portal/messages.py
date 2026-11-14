from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from . import models as m
from .serializers import select, serialize, text, validated
from .services import TEAMS, atomic_change, audit, notify, roles


@api_view(["GET", "POST"])
@atomic_change
def threads(request, pk=None):
    user = request.user
    patient = getattr(user, "patient", None)
    staff_roles = roles(user)
    qs = m.Thread.objects.select_related("patient__user")
    if patient:
        qs = qs.filter(patient=patient)
    elif "Administrator" not in staff_roles:
        qs = qs.filter(team__in=[team for team, allowed in TEAMS.items() if staff_roles.intersection(allowed)])
    if request.method == "GET":
        audit(user, "Read messages", patient, pk or "")
        if pk:
            thread = get_object_or_404(qs, pk=pk)
            messages = list(thread.messages.select_related("sender").order_by("pk"))
            for message in messages:
                if message.sender_id != user.id:
                    message.read_by.add(user)
            return Response({**serialize(thread), "messages": [
                {"id": msg.id, "sender": msg.sender.get_full_name() or msg.sender.username,
                 "body": msg.body, "created_at": msg.created_at, "mine": msg.sender_id == user.id} for msg in messages]})
        box = request.query_params.get("box", "inbox")
        qs = qs.filter(archived_by=user) if box == "archive" else qs.exclude(archived_by=user)
        if box == "sent":
            qs = qs.filter(messages__sender=user).distinct()
        return Response([{**serialize(row), "patient_name": str(row.patient),
                          "unread": row.messages.exclude(sender=user).exclude(read_by=user).count()} for row in qs.order_by("-pk")])
    if not pk:
        if not patient:
            raise PermissionDenied
        data = validated(request.data, subject=text(length=150), category=select(m.CATEGORIES),
                         team=select(tuple(TEAMS)), body=text())
        body = data.pop("body")
        thread = m.Thread.objects.create(patient=patient, **data)
    else:
        thread = get_object_or_404(qs, pk=pk)
        data = validated(request.data, action=select(("reply", "archive", "restore")), body=text(False))
        if data["action"] != "reply":
            if data["action"] == "archive":
                thread.archived_by.add(user)
            else:
                thread.archived_by.remove(user)
            return Response({"detail": "Conversation updated."})
        body = validated({"body": data.get("body", "")}, body=text())["body"]
    m.Message.objects.create(thread=thread, sender=user, body=body)
    if not patient:
        thread.archived_by.remove(thread.patient.user)
        notify(thread.patient, "Message", "New reply from your care team", f"/messages/{thread.pk}")
    audit(user, "Message sent", thread.patient, thread.pk)
    return Response({"id": thread.pk}, status=201)
