from datetime import datetime
from typing import Optional, Any, Literal
from pydantic import BaseModel, Field

class AlertLabel(BaseModel):
    alertname: str
    namespace: str
    pod: Optional[str] = None
    service: Optional[str] = None
    severity: Optional[str] = None
    instance: Optional[str] = None

class AlertAnnotation(BaseModel):
    summary: Optional[str] = None
    description: Optional[str] = None
    message: Optional[str] = None

class Alert(BaseModel):
    status: str
    labels: AlertLabel
    annotations: AlertAnnotation
    startsAt: datetime
    endsAt: Optional[datetime] = None
    generatorURL: str
    fingerprint: str

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat() if v else None}

class AlertGroup(BaseModel):
    version: str
    groupKey: str
    truncatedAlerts: int = 0
    status: str
    receiver: str
    groupLabels: dict[str, str]
    commonLabels: dict[str, str]
    commonAnnotations: dict[str, str]
    externalURL: str
    alerts: list[Alert]

class DebugRequest(BaseModel):
    alert_group: AlertGroup = Field(..., description="Alert group from Alertmanager")
    kubeconfig: Optional[str] = Field(None, description="Optional kubeconfig data if not using the default")

class DebuggingStep(BaseModel):
    step_id: int
    description: str
    command: str
    result: Optional[Any] = None
    timestamp: datetime = Field(default_factory=datetime.now)

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat() if v else None}

class DebugReport(BaseModel):
    alert_id: str
    start_time: datetime = Field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    alert_summary: str
    steps: list[DebuggingStep] = Field(default_factory=list)
    root_cause: Optional[str] = None
    recommendations: list[str] = Field(default_factory=list)
    status: Literal["in_progress", "completed", "failed"] = "in_progress"

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat() if v else None}

class OncallK8sResponse(BaseModel):
    root_cause: str = Field(..., description="The root cause of the Kubernetes issue")
    conclusion: str = Field(..., description="Overall conclusion about the alert or issue")
    diagnosis: str = Field(..., description="Detailed diagnosis of what went wrong")
    summary_of_findings: str = Field(..., description="Summary of the collected data and observations")
    recommended_actions: str = Field(..., description="Actions recommended to resolve the issue")
    recommendations: str = Field(..., description="Additional recommendations for prevention or improvement")
    solution: str = Field(..., description="The final solution or fix to apply")
