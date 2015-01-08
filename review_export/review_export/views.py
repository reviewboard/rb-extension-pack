# from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse

# from reviewboard.reviews.models import ReviewRequest
from reviewboard.reviews.views import _find_review_request

from review_export.printer import ReviewRequestPDFPrinter, XMLPrinter


def send_pdf_file(request, review_request_id, local_site=None):
    """
    If the request user has permissions, create and send a PDF file through
    Django without loading the whole file into memory at once
    """
    # retrieve review_request if user has permissions
    review_request, response = _find_review_request(
        request, review_request_id, local_site
    )

    # User does not have permissions or non-existant review_request
    if not review_request:
        return response

    filename = 'ReviewRequest#%s.pdf' % review_request_id
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=' + filename

    # Create the PDF object using the response object as its 'file'
    report = ReviewRequestPDFPrinter(review_request, 'Letter')
    pdf = report.generate_report()

    # Write pdf file to response
    response.write(pdf)
    return response


def send_xml_file(request, review_request_id, local_site=None):
    # retrieve review_request if user has permissions
    review_request, response = _find_review_request(
        request, review_request_id, local_site
    )

    # User does not have permissions or non-existant review_request
    if not review_request:
        return response

    filename = 'ReviewRequest#%s.xml' % review_request_id
    response = HttpResponse(content_type='text/xml')
    response['Content-Disposition'] = 'attachment; filename=' + filename

    # Create the PDF object using the response object as its 'file'
    printer = XMLPrinter(review_request)
    xml = printer.generate_report()

    # Write pdf file to response
    response.write(xml)
    return response
