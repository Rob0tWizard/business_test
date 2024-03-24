from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from employers.forms import DailyReportForm
from employers.models import Report


@login_required
def old_reports(request):
    reports = Report.objects.filter(date__month=datetime.now().month)
    return render(request, 'old_reports.html', {'reports': reports})


@staff_member_required
def edit_report(request, pk):
    report = Report.objects.get(pk=pk)
    form = DailyReportForm(instance=report)

    if request.method == 'POST':
        form = DailyReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            return redirect('old_reports')
        else:
            return render(request, 'edit_report.html', {'form': form})


@staff_member_required
def reports(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    manager = request.GET.get('manager')

    if start_date and end_date:
        reports = Report.objects.filter(date__range=[start_date, end_date])
    else:
        reports = Report.objects.all()

    if manager:
        reports = reports.filter(user__username=manager)

    return render(request, 'reports.html', {'reports': reports})


@staff_member_required
def summary_report(request):
    month = request.GET.get('month')

    if month:
        reports = Report.objects.filter(date__month=month)
        total_revenue = sum(report.revenue for report in reports)
    else:
        reports = []
        total_revenue = 0

    return render(request, 'summary_report.html', {'reports': reports, 'total_revenue': total_revenue})
