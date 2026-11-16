"""Permission-checked HTML-preview data and PDFs from one document representation."""
from io import BytesIO
from xml.sax.saxutils import escape

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

from . import models as m
from .services import patient_scope, read_audit
from .serializers import serialize

DISCLAIMER = "DEMO - SYNTHETIC DATA ONLY - NOT FOR CLINICAL USE."


def display_date(value):
    return value.strftime("%b %d, %Y, %I:%M %p UTC" if hasattr(value, "hour") else "%b %d, %Y") if value else "Not recorded"


def document_data(request, kind, pk):
    section = {"lab": "results", "document": "documents", "invoice": "billing", "receipt": "billing"}.get(kind)
    if not section:
        raise NotFound("This document is unavailable.")
    patient = patient_scope(request, section)
    result = {"patient": str(patient), "birth_date": display_date(patient.birth_date), "disclaimer": DISCLAIMER,
              "sections": [], "kind": kind, "id": pk}
    if kind == "lab":
        row = get_object_or_404(m.LabResult.objects.select_related("provider__department"), patient=patient, published=True, pk=pk)
        result.update(title=row.name, subtitle="Laboratory report", identifier=f"LAB-{pk}", date=display_date(row.resulted_at),
            facts=[["Provider", str(row.provider)], ["Collected", display_date(row.collected_at)], ["Resulted", display_date(row.resulted_at)],
                   ["Result", f"{row.value if row.value is not None else 'Pending'} {row.unit}"], ["Flag", row.flag or "Not available"],
                   ["Reference range", f"{row.reference_low if row.reference_low is not None else 'Not recorded'} to {row.reference_high if row.reference_high is not None else 'Not recorded'} {row.unit}"], ["Status", row.status]])
        result["sections"] = [{"title": "Care team comments", "body": row.comments or "No comments recorded."}]
    elif kind == "document":
        row = get_object_or_404(m.Document.objects.filter(patient=patient, published=True).filter(Q(encounter__published=True) | Q(encounter__isnull=True)).select_related("encounter__provider"), pk=pk)
        result.update(title=row.title, subtitle=row.kind, identifier=f"DOC-{pk}", date=display_date(row.created_at),
            facts=[["Document type", row.kind], ["Document created", display_date(row.created_at)]])
        if row.encounter:
            result["facts"] += [["Visit date", display_date(row.encounter.date)], ["Provider", str(row.encounter.provider)]]
        result["sections"] = [{"title": "Summary", "body": row.content}]
    elif kind == "invoice":
        row = get_object_or_404(m.Invoice, patient=patient, pk=pk)
        result.update(title=row.description, subtitle="Billing statement", identifier=row.number, date=display_date(row.service_date),
            facts=[["Status", serialize(row)["status"]], ["Service date", display_date(row.service_date)], ["Due date", display_date(row.due_date)],
                   ["Charges", f"${row.amount:.2f}"], ["Insurance adjustment", f"${row.adjustment:.2f}"],
                   ["Patient responsibility", f"${row.responsibility:.2f}"], ["Paid", f"${row.paid:.2f}"], ["Remaining", f"${row.balance:.2f}"]])
        result["sections"] = [{"title": "Payment history", "body": "\n".join(f"Receipt {p.pk} | {display_date(p.created_at)} | ${p.amount:.2f}" for p in row.payment_set.order_by("created_at")) or "No payments recorded."}]
    else:
        row = get_object_or_404(m.Payment.objects.select_related("invoice"), invoice__patient=patient, pk=pk)
        result.update(title="Payment receipt", subtitle="Simulated transaction", identifier=f"RECEIPT-{pk}", date=display_date(row.created_at),
            facts=[["Receipt number", str(pk)], ["Invoice", row.invoice.number], ["Service", row.invoice.description],
                   ["Payment date", display_date(row.created_at)], ["Amount paid", f"${row.amount:.2f}"]])
        result["sections"] = [{"title": "Payment confirmation", "body": "This receipt confirms a simulated payment. No real money was collected."}]
    result["filename"] = f"careconnect-{kind}-{slugify(result['title'])[:65]}-{pk}.pdf"
    read_audit(request, patient, "document export " + kind, pk)
    return result


def pdf_response(data):
    stream = BytesIO()
    doc = SimpleDocTemplate(stream, pagesize=A4, leftMargin=48, rightMargin=48, topMargin=83, bottomMargin=60,
                            title=data["title"], author="CareConnect", subject=data["subtitle"])
    body = ParagraphStyle("Body", fontName="Helvetica", fontSize=10, leading=15, textColor=colors.HexColor("#243e49"), spaceAfter=9, alignment=TA_LEFT, wordWrap="CJK")
    title = ParagraphStyle("Title", parent=body, fontName="Helvetica-Bold", fontSize=22, leading=27, spaceAfter=14)
    heading = ParagraphStyle("Heading", parent=body, fontName="Helvetica-Bold", fontSize=12, spaceBefore=15, spaceAfter=9)
    def p(text, style=body):
        return Paragraph(escape(str(text)).replace("\n", "<br/>"), style)
    flow = [p(data["subtitle"].upper()), p(data["title"], title), p(f"Reference: {data['identifier']} | {data['date']}"), Spacer(1, 9)]
    facts = [["Patient", data["patient"]], ["Date of birth", data["birth_date"]], *data["facts"]]
    table = Table([[p(k), p(v)] for k, v in facts], colWidths=[156, doc.width-156], hAlign="LEFT")
    table.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#edf5f2")),
        ("LINEBELOW", (0, 0), (-1, -1), .5, colors.HexColor("#dce7e3")), ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
    flow.append(table)
    for section in data["sections"]:
        flow.append(p(section["title"], heading))
        # Separate paragraphs allow long letters and summaries to paginate naturally.
        for line in section["body"].splitlines() or ["No additional information."]:
            flow.append(p(line or " "))
    def page(canvas, document):
        w, h = A4
        canvas.saveState()
        canvas.setFillColor(colors.HexColor("#176e60"))
        canvas.setFont("Helvetica-Bold", 17)
        canvas.drawString(48, h-39, "CareConnect")
        canvas.setFont("Helvetica", 8)
        canvas.drawRightString(w-48, h-39, data["identifier"])
        canvas.setStrokeColor(colors.HexColor("#cbded5"))
        canvas.line(48, h-53, w-48, h-53)
        canvas.setFont("Helvetica-Bold", 7)
        canvas.drawString(48, 37, DISCLAIMER)
        canvas.setFont("Helvetica", 8)
        canvas.drawRightString(w-48, 37, f"Page {document.page}")
        canvas.restoreState()
    doc.build(flow, onFirstPage=page, onLaterPages=page)
    response = HttpResponse(stream.getvalue(), content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{data["filename"]}"'
    response["Cache-Control"] = "private, no-store"
    response["X-Content-Type-Options"] = "nosniff"
    return response


@api_view(["GET"])
def preview(request, kind, pk, file=False):
    data = document_data(request, kind, pk)
    response = pdf_response(data) if file else Response(data)
    response["Cache-Control"] = "private, no-store"
    return response
