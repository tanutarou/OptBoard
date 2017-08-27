from django.shortcuts import render, get_object_or_404, redirect
from optboard.settings import MEDIA_ROOT
from collections import OrderedDict
from queue import Queue
import subprocess
import base64
import io
import os
import re
import ast

from .models import Solver, Result, Project
from .forms import SolverForm, ProjectForm


def project_select(request):
    """ projectの選択 """
    projects = Project.objects.all()
    return render(request, 'dashboard/project_select.html', {'projects': projects})


def project_edit(request, edit_project_id=None):
    """ projectの編集 """

    if edit_project_id:
        edit_project = get_object_or_404(Project, pk=edit_project_id)
    else:
        edit_project = Project()

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=edit_project)
        if form.is_valid():
            edit_project = form.save(commit=False)
            edit_project.save()
            return redirect('dashboard:project_select')
    else:
        form = ProjectForm(instance=edit_project)
    return render(request, 'dashboard/project_edit.html', dict(form=form, project=None, edit_project=edit_project))


def project_del(request, del_project_id):
    del_project = Project.objects.get(pk=del_project_id)
    del_project.delete()
    return redirect('dashboard:project_select')


def main_page(request, project_id):
    """ main page """

    select_solver = None
    sort_type = 'id'
    for key, val in request.GET.items():
        if key == 'solver_id':
            select_solver_id = request.GET['solver_id']
            select_solver = Solver.objects.get(pk=select_solver_id)
        elif key == 'sort-type':
            sort_type = request.GET['sort-type']

    project = Project.objects.get(pk=project_id)
    solvers = Solver.objects.all().filter(project_id=project_id).order_by('id')
    results = Result.objects.all().filter(project_id=project_id).order_by(sort_type)

    if request.method == 'POST':
        solver = Solver.objects.get(name=request.POST['solver'])
        params = OrderedDict()
        for key in solver.get_keys():
            params[key] = request.POST[key]
        run(project, solver, params, request.POST['comment'])

    return render(request, 'dashboard/main_page.html', {'project': project, 'solvers': solvers, 'results': results, 'select_solver': select_solver})


def result_del_all(request, project_id):
    project = Project.objects.get(pk=project_id)
    results = Result.objects.all().filter(project_id=project_id).order_by('id')

    for r in results:
        r.delete()

    return redirect('dashboard:main', project_id=project.id)


def loopstr2obj(v):
    """ loopを表す文字列(float, list, range)をそれらのクラスへ変換 """

    p = re.compile('range\(\d+(, *\d+)?(, *\d+)?\)')
    if p.match(v) is not None:
        return list(eval(v))  # rangeを評価
    else:
        return ast.literal_eval(v)


def run(project, solver, runlist, comment):
    cmds = Queue()

    # 拡張子によって実行コマンドの切り替え
    root, ext = os.path.splitext(str(solver.solver_file))
    if ext == '.py':
        cmds.put("python {}/{} ".format(MEDIA_ROOT, solver.solver_file))
    else:
        cmds.put("./{}/{} ".format(MEDIA_ROOT, solver.solver_file))

    for k, v in runlist.items():
        v = loopstr2obj(v)

        ncmds = Queue()
        while not cmds.empty():
            cmd = cmds.get()
            if isinstance(v, list) or isinstance(v, range):
                v = list(v)
                for t in v:
                    ncmds.put(cmd + "{} ".format(t))
            else:
                cmd += "{} ".format(v)
                ncmds.put(cmd)
        cmds = ncmds

    while not cmds.empty():
        cmd = cmds.get()
        try:
            res = subprocess.check_output(cmd, shell=True)
            res = res.split(b'\n')
            res = res[-2].strip()  # 最終行の値だけ取得
        except subprocess.CalledProcessError as e:
            print("Error:{}".format(e))
            res = "-1.0"

        values = cmd.split()
        params = []
        for i, k in enumerate(runlist.keys()):
            params.append((k, values[i + 2]))

        result = Result(name="no name", project=project, params=str(params), eval_val=res, solver=solver, elapsed_time=-1.0, comment=comment)
        result.save()   # id付与のため一回保存
        result.name = "result_{0:05d}".format(result.pk)
        result.save()


def result_del(request, project_id, del_result_id):
    project = Project.objects.get(pk=project_id)
    del_result = Result.objects.get(pk=del_result_id)
    del_result.delete()
    return redirect('dashboard:main', project_id=project.id)


def solver_list(request, project_id):
    """ 手法一覧 """
    project = Project.objects.get(pk=project_id)
    solvers = Solver.objects.all().filter(project_id=project_id).order_by('id')
    return render(request, 'dashboard/solver_list.html', {'project': project, 'solvers': solvers})


def solver_edit(request, project_id, solver_id=None):
    """ 手法の編集 """
    project = Project.objects.get(pk=project_id)

    if solver_id:
        solver = get_object_or_404(Solver, pk=solver_id)
    else:
        solver = Solver()

    if request.method == 'POST':
        form = SolverForm(request.POST, request.FILES, instance=solver)
        if form.is_valid():
            solver = form.save(commit=False)
            solver.save()
            return redirect('dashboard:solver_list', project_id=project.id)
    else:
        form = SolverForm(instance=solver)
    return render(request, 'dashboard/solver_edit.html', dict(project=project, form=form, solver_id=solver_id))


def solver_del(request, project_id, solver_id):
    project = Project.objects.get(pk=project_id)
    return render(request, 'dashboard/main_page.html', {'project': project})


def analysis1D(request, project_id):
    project = Project.objects.get(pk=project_id)
    solvers = Solver.objects.all().filter(project_id=project_id).order_by('id')
    results = Result.objects.all().filter(project_id=project_id).order_by('id')

    select_solver = None
    select_param = None
    for key, val in request.GET.items():
        if key == 'solver_id':
            select_solver_id = request.GET['solver_id']
            select_solver = Solver.objects.get(pk=select_solver_id)
        elif key == 'select_param':
            select_param = request.GET['select_param']

    # 選択されたパラメータと評価値とのペアを格納していく
    x = []
    y = []
    for r in results:
        params = ast.literal_eval(r.params)
        for p in params:
            if p[0] == select_param:
                x.append(float(p[1]))
                y.append(float(r.eval_val))

    graphic = make_plot(x, y, select_param)

    return render(request, 'dashboard/1Dplot.html', {'project': project, 'graphic': graphic, 'solvers': solvers, 'select_solver': select_solver})


def make_plot(x, y, xlabel):
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure

    fig = Figure()
    ax = fig.add_subplot(111)
    ax.plot(x, y, 'o')
    ax.set_xlabel(xlabel)
    ax.set_ylabel('eval_val')

    canvas = FigureCanvas(fig)
    buf = io.BytesIO()
    canvas.print_png(buf)
    graphic = buf.getvalue()
    graphic = base64.b64encode(graphic)
    buf.close()

    return graphic


def analysis2D(request, project_id):
    import sys
    import numpy as np

    project = Project.objects.get(pk=project_id)
    solvers = Solver.objects.all().filter(project_id=project_id).order_by('id')
    graphic = None

    select_solver = None
    select_param1 = None
    select_param2 = None
    IS_PARAM = False

    for key, val in request.GET.items():
        if key == 'solver_id':
            select_solver_id = request.GET['solver_id']
            select_solver = Solver.objects.get(pk=select_solver_id)
        elif key == 'select_param1':
            select_param1 = request.GET['select_param1']
            IS_PARAM = True
        elif key == 'select_param2':
            select_param2 = request.GET['select_param2']

    if IS_PARAM:
        results = Result.objects.all().filter(project_id=project_id, solver=select_solver).order_by('id')
        # 選択されたパラメータの値の最大値と最小値を取得する
        xmin = sys.float_info.max
        xmax = sys.float_info.min
        ymin = sys.float_info.max
        ymax = sys.float_info.min

        for r in results:
            params = ast.literal_eval(r.params)
            for p in params:
                if p[0] == select_param1:
                    xmin = min(xmin, float(p[1]))
                    xmax = max(xmax, float(p[1]))
                elif p[0] == select_param2:
                    ymin = min(ymin, float(p[1]))
                    ymax = max(ymax, float(p[1]))

        # 最大値と最小値をもとにnumpyの配列を生成
        delta = 1.0
        xn = int((xmax - xmin) * delta)
        yn = int((ymax - ymin) * delta)
        data = np.zeros((xn + 1, yn + 1))

        # 配列への評価値の代入
        for r in results:
            params = ast.literal_eval(r.params)
            for p in params:
                if p[0] == select_param1:
                    x = int((float(p[1]) - xmin) * delta)
                elif p[0] == select_param2:
                    y = int((float(p[1]) - ymin) * delta)
            data[x][y] = r.eval_val

        graphic = make_heatmap(data, select_param1, select_param2)

    return render(request, 'dashboard/2Dplot.html', {'project': project, 'graphic': graphic, 'solvers': solvers, 'select_solver': select_solver})


def make_heatmap(data, xlabel, ylabel):
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    import matplotlib.pyplot as plt
    import numpy as np

    fig = Figure()
    ax = fig.add_subplot(111)
    heatmap = ax.pcolor(data, cmap=plt.cm.Blues)
    fig.colorbar(heatmap)

    ax.set_xticks(np.arange(data.shape[0]) + 0.5, minor=False)
    ax.set_yticks(np.arange(data.shape[1]) + 0.5, minor=False)

    ax.invert_yaxis()
    ax.xaxis.tick_top()

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    canvas = FigureCanvas(fig)
    buf = io.BytesIO()
    canvas.print_png(buf)
    graphic = buf.getvalue()
    graphic = base64.b64encode(graphic)
    buf.close()

    return graphic
