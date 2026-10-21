"""
Utilities package for SahkaarX stage portfolio projects.
"""

from .logger import setup_logger
from .env_helper import load_env_var
from .commit_validator import (
    validate_commit_message,
    validate_commit_list,
    CommitValidationResult,
    STANDARD_COMMIT_TYPES,
)
from .git_ops import (
    GitCommitInfo,
    WorkflowStep,
    WorkflowValidationResult,
    GitWorkflowTracker,
    get_current_git_branch,
    is_git_working_tree_clean,
    get_recent_commits,
    check_branch_divergence,
)
from .branch_validator import (
    BranchValidator,
    BranchNameValidationResult,
    BranchType,
)
from .merge_analyzer import (
    MergeAnalyzer,
    MergeHistoryReport,
    MergeCommitRecord,
    CommitHygieneIssue,
    MergeStrategy,
)
from .pr_lifecycle import (
    PRLifecycleManager,
    PullRequestMetadata,
    PRState,
    PRChangeType,
    PRReviewChecklist,
)

__all__ = [
    "setup_logger",
    "load_env_var",
    "validate_commit_message",
    "validate_commit_list",
    "CommitValidationResult",
    "STANDARD_COMMIT_TYPES",
    "GitCommitInfo",
    "WorkflowStep",
    "WorkflowValidationResult",
    "GitWorkflowTracker",
    "get_current_git_branch",
    "is_git_working_tree_clean",
    "get_recent_commits",
    "check_branch_divergence",
    "BranchValidator",
    "BranchNameValidationResult",
    "BranchType",
    "MergeAnalyzer",
    "MergeHistoryReport",
    "MergeCommitRecord",
    "CommitHygieneIssue",
    "MergeStrategy",
    "PRLifecycleManager",
    "PullRequestMetadata",
    "PRState",
    "PRChangeType",
    "PRReviewChecklist",
]
