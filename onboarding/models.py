"""
models.py

This module is used to register models for onboarding app

"""

from datetime import datetime

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from base.sleektiv_company_manager import SleektivCompanyManager
from employee.models import Employee
from sleektiv.models import SleektivModel
from sleektiv_audit.models import SleektivAuditInfo, SleektivAuditLog
from recruitment.models import Candidate, Recruitment


class OnboardingStage(SleektivModel):
    """
    OnboardingStage models
    """

    stage_title = models.CharField(max_length=200)
    recruitment_id = models.ForeignKey(
        Recruitment,
        verbose_name=_("Recruitment"),
        null=True,
        related_name="onboarding_stage",
        on_delete=models.CASCADE,
    )
    employee_id = models.ManyToManyField(Employee, verbose_name="Stage managers")
    sequence = models.IntegerField(null=True)
    is_final_stage = models.BooleanField(default=False)
    objects = SleektivCompanyManager("recruitment_id__company_id")

    def __str__(self):
        return f"{self.stage_title}"

    class Meta:
        """
        Meta class for additional options
        """

        ordering = ["sequence"]


@receiver(post_save, sender=Recruitment)
def create_initial_stage(sender, instance, created, **kwargs):
    """
    This is post save method, used to create initial stage for the recruitment
    """
    if created or not instance.onboarding_stage.first():
        initial_stage = OnboardingStage()
        initial_stage.sequence = 0
        initial_stage.stage_title = "Initial"
        initial_stage.recruitment_id = instance
        initial_stage.save()


class OnboardingTask(SleektivModel):
    """
    OnboardingTask models
    """

    task_title = models.CharField(max_length=200)
    # recruitment_id = models.ManyToManyField(Recruitment, related_name="onboarding_task")
    stage_id = models.ForeignKey(
        OnboardingStage,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="onboarding_task",
    )
    candidates = models.ManyToManyField(
        Candidate,
        blank=True,
        related_name="cand_onboarding_task",
    )
    employee_id = models.ManyToManyField(
        Employee, related_name="onboarding_task", verbose_name=_("Task Managers")
    )

    objects = SleektivCompanyManager("stage_id__recruitment_id__company_id")

    def __str__(self):
        return f"{self.task_title}"


class CandidateStage(SleektivModel):
    """
    CandidateStage model
    """

    candidate_id = models.OneToOneField(
        Candidate, on_delete=models.PROTECT, related_name="onboarding_stage"
    )
    onboarding_stage_id = models.ForeignKey(
        OnboardingStage, on_delete=models.PROTECT, related_name="candidate"
    )
    onboarding_end_date = models.DateField(blank=True, null=True)
    sequence = models.IntegerField(null=True, default=0)
    objects = SleektivCompanyManager("candidate_id__recruitment_id__company_id")

    def __str__(self):
        return f"{self.candidate_id}  |  {self.onboarding_stage_id}"

    def save(self, *args, **kwargs):
        if self.onboarding_stage_id.is_final_stage:
            self.onboarding_end_date = datetime.today()
        super(CandidateStage, self).save(*args, **kwargs)

    def task_completion_ratio(self):
        """
        function that used for getting the numbers between task completed v/s tasks assigned
        """
        cans_tasks = self.candidate_id.candidate_task
        completed_tasks = cans_tasks.filter(status="done")
        return f"{completed_tasks.count()}/{cans_tasks.count()}"

    class Meta:
        """
        Meta class for additional options
        """

        verbose_name = _("Candidate Onboarding stage")
        ordering = ["sequence"]


class CandidateTask(SleektivModel):
    """
    CandidateTask model
    """

    choice = (
        ("todo", _("Todo")),
        ("scheduled", _("Scheduled")),
        ("ongoing", _("Ongoing")),
        ("stuck", _("Stuck")),
        ("done", _("Done")),
    )
    candidate_id = models.ForeignKey(
        Candidate, on_delete=models.PROTECT, related_name="candidate_task"
    )
    # managers = models.ManyToManyField(Employee)
    stage_id = models.ForeignKey(
        OnboardingStage,
        null=True,
        on_delete=models.PROTECT,
        related_name="candidate_task",
    )
    status = models.CharField(
        max_length=50, choices=choice, blank=True, null=True, default="todo"
    )
    onboarding_task_id = models.ForeignKey(OnboardingTask, on_delete=models.PROTECT)
    objects = SleektivCompanyManager("candidate_id__recruitment_id__company_id")
    history = SleektivAuditLog(
        related_name="history_set",
        bases=[
            SleektivAuditInfo,
        ],
    )

    def __str__(self):
        return f"{self.candidate_id}|{self.onboarding_task_id}"

    class Meta:
        """
        Meta class to add some additional options
        """

        verbose_name = _("Candidate onboarding task")
        # unique_together = ("candidate_id", "onboarding_task_id")


class OnboardingPortal(SleektivModel):
    """
    OnboardingPortal model
    """

    candidate_id = models.OneToOneField(
        Candidate, on_delete=models.PROTECT, related_name="onboarding_portal"
    )
    token = models.CharField(max_length=200)
    used = models.BooleanField(default=False)
    count = models.IntegerField(default=0)
    profile = models.ImageField(upload_to="employee/profile", null=True, blank=True)
    objects = SleektivCompanyManager("candidate_id__recruitment_id__company_id")

    def __str__(self):
        return f"{self.candidate_id} | {self.token}"
