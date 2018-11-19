"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

# VARIABLES of this file must be unique
from django_hpc_job_controller.client.scheduler.status import JobStatus


# Dictionary to map names and corresponding display names (for UI)
DISPLAY_NAME_MAP = dict()
DISPLAY_NAME_MAP_HPC_JOB = dict()


# Job Status
NONE = 'none'
NONE_DISPLAY = 'None'
DRAFT = 'draft'
DRAFT_DISPLAY = 'Draft'
PENDING = 'pending'
PENDING_DISPLAY = 'Pending'
SUBMITTING = 'submitting'
SUBMITTING_DISPLAY = 'Submitting'
SUBMITTED = 'submitted'
SUBMITTED_DISPLAY = 'Submitted'
QUEUED = 'queued'
QUEUED_DISPLAY = 'Queued'
IN_PROGRESS = 'in_progress'
IN_PROGRESS_DISPLAY = 'In Progress'
CANCELLING = 'cancelling'
CANCELLING_DISPLAY = 'Cancelling'
CANCELLED = 'cancelled'
CANCELLED_DISPLAY = 'Cancelled'
ERROR = 'error'
ERROR_DISPLAY = 'Error'
WALL_TIME_EXCEEDED = 'wall_time_exceeded'
WALL_TIME_EXCEEDED_DISPLAY = 'Wall Time Exceeded'
OUT_OF_MEMORY = 'out_of_memory'
OUT_OF_MEMORY_DISPLAY = 'Out of Memory'
COMPLETED = 'completed'
COMPLETED_DISPLAY = 'Completed'
SAVED = 'saved'
SAVED_DISPLAY = 'Saved'
DELETING = 'deleting'
DELETING_DISPLAY = 'Deleting'
DELETED = 'deleted'
DELETED_DISPLAY = 'Deleted'
PUBLIC = 'public'
PUBLIC_DISPLAY = 'Public'

DISPLAY_NAME_MAP.update({
    DRAFT: DRAFT_DISPLAY,
    PENDING: PENDING_DISPLAY,
    SUBMITTING: SUBMITTING_DISPLAY,
    SUBMITTED: SUBMITTED_DISPLAY,
    QUEUED: QUEUED_DISPLAY,
    IN_PROGRESS: IN_PROGRESS_DISPLAY,
    CANCELLING: CANCELLING_DISPLAY,
    CANCELLED: CANCELLED_DISPLAY,
    ERROR: ERROR_DISPLAY,
    WALL_TIME_EXCEEDED: WALL_TIME_EXCEEDED_DISPLAY,
    OUT_OF_MEMORY: OUT_OF_MEMORY_DISPLAY,
    COMPLETED: COMPLETED_DISPLAY,
    SAVED: SAVED_DISPLAY,
    DELETING: DELETING_DISPLAY,
    DELETED: DELETED_DISPLAY,
    PUBLIC: PUBLIC_DISPLAY,
})

DISPLAY_NAME_MAP_HPC_JOB.update({
    JobStatus.DRAFT: DRAFT,
    JobStatus.PENDING: PENDING,
    JobStatus.SUBMITTING: SUBMITTING,
    JobStatus.SUBMITTED: SUBMITTED,
    JobStatus.QUEUED: QUEUED,
    JobStatus.RUNNING: IN_PROGRESS,
    JobStatus.CANCELLING: CANCELLING,
    JobStatus.CANCELLED: CANCELLED,
    JobStatus.ERROR: ERROR,
    JobStatus.WALL_TIME_EXCEEDED: WALL_TIME_EXCEEDED,
    JobStatus.OUT_OF_MEMORY: OUT_OF_MEMORY,
    JobStatus.DELETING: DELETING,
    JobStatus.DELETED: DELETED,
    JobStatus.COMPLETED: COMPLETED,
})
