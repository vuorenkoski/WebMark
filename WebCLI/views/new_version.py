from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from ..models import Algorithm, Algorithm_version
from ..forms import AlgorithmVersionForm
from WebCLI.celery import celery_app


def add_version(request):
    a = Algorithm.objects.get(pk=request.GET.get("index"))
    if request.user.pk != a.user.pk:
        raise PermissionDenied

    if request.method == "POST":
        algorithm = AlgorithmVersionForm(request.POST).data['algorithm']
        version = Algorithm_version(algorithm_id=a, timestamp=timezone.now(), algorithm=algorithm)
        version.save()
        celery_app.send_task("benchmark.benchmark_task", args=["i am a parameter"])
        return redirect(a)
    last_version = Algorithm_version.objects.filter(algorithm_id=a).order_by('-timestamp')[0]
    form = AlgorithmVersionForm(initial={'algorithm': last_version.algorithm})
    data = {'algorithm': a, 'form': form}
    return render(request, 'WebCLI/addVersion.html', data)
