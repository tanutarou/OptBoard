from django.forms import ModelForm
from .models import Solver, Project


class SolverForm(ModelForm):
    """ 最適化手法のフォーム """
    class Meta:
        model = Solver
        fields = ('name', 'params_info', 'solver_file', 'project', 'comment')


class ProjectForm(ModelForm):
    """ 最適化手法のフォーム """
    class Meta:
        model = Project
        fields = ('name', 'comment')
