import datetime
import logging
from typing import List

from metricflow.model.objects.materialization import Materialization
from metricflow.model.objects.user_configured_model import UserConfiguredModel
from metricflow.model.semantic_model import SemanticModel
from metricflow.model.semantics.data_source_container import PydanticDataSourceContainer
from metricflow.model.semantics.semantic_containers import DataSourceSemantics
from metricflow.model.validations.validator_helpers import (
    MaterializationContext,
    ModelValidationRule,
    ValidationError,
    ValidationIssueType,
    validate_safely,
    ValidationFutureError,
)
from metricflow.naming.linkable_spec_name import StructuredLinkableSpecName
from metricflow.query.query_parser import MetricFlowQueryParser
from metricflow.specs import TimeDimensionReference

logger = logging.getLogger(__name__)


class ValidMaterializationRule(ModelValidationRule):
    """Check that a materialization config is valid.

    * Metrics listed are valid.
    * Dimensions or identifiers are valid for the listed metrics.
    * Primary time dimension is listed in the dimensions section.
    """

    @staticmethod
    @validate_safely(whats_being_done="checking materialization is defined correctly")
    def _validate_materialization(
        materialization: Materialization,
        primary_time_dimensions_reference: TimeDimensionReference,
        mf_query_parser: MetricFlowQueryParser,
    ) -> List[ValidationIssueType]:
        issues: List[ValidationIssueType] = []

        context = MaterializationContext(
            file_name=materialization.metadata.file_slice.filename if materialization.metadata else None,
            line_number=materialization.metadata.file_slice.start_line_number if materialization.metadata else None,
            materialization_name=materialization.name,
        )

        if not materialization.dimensions:
            return [
                ValidationError(
                    context=context,
                    message=f"Materialization '{materialization.name}' does not have dimensions listed",
                )
            ]

        try:
            mf_query_parser.parse_and_validate_query(
                metric_names=materialization.metrics,
                group_by_names=materialization.dimensions,
            )
        # TODO: Using broad exception clause until the query validation returns a list of errors.
        except Exception as err:
            issues.append(
                ValidationFutureError(
                    context=context,
                    message=str(err),
                    error_date=datetime.date(2022, 5, 23),
                )
            )

        # Primary dimension checks
        mat_primary_time_dimension_names: List[str] = []
        for mat_dimension_or_identifier_name in materialization.dimensions:
            structured_spec = StructuredLinkableSpecName.from_name(mat_dimension_or_identifier_name)
            if structured_spec.element_name == primary_time_dimensions_reference.element_name:
                mat_primary_time_dimension_names.append(mat_dimension_or_identifier_name)

        if len(mat_primary_time_dimension_names) == 0:
            issues.append(
                ValidationError(
                    context=context,
                    message=f"Primary time dimension {primary_time_dimensions_reference.element_name} not listed"
                    f" as a dimension in materialization {materialization.name}",
                )
            )

        if len(mat_primary_time_dimension_names) > 1:
            issues.append(
                ValidationError(
                    context=context,
                    message=f"Multiple primary time dimensions {mat_primary_time_dimension_names} listed in "
                    f"materialization {materialization.name}",
                )
            )

        return issues

    @staticmethod
    @validate_safely(whats_being_done="running model validation ensuring materializations are valid")
    def validate_model(model: UserConfiguredModel) -> List[ValidationIssueType]:  # noqa: D
        """Check that all of the metrics and dimensions listed in a materialization are valid."""
        issues: List[ValidationIssueType] = []
        ds_semantics = DataSourceSemantics(
            model=model, configured_data_source_container=PydanticDataSourceContainer(model.data_sources)
        )
        primary_time_dimensions_reference = ds_semantics.primary_time_dimension_reference
        mf_query_parser = MetricFlowQueryParser(
            model=SemanticModel(user_configured_model=model),
            primary_time_dimension_reference=primary_time_dimensions_reference,
        )
        for materialization in model.materializations:
            issues += ValidMaterializationRule._validate_materialization(
                materialization=materialization,
                primary_time_dimensions_reference=primary_time_dimensions_reference,
                mf_query_parser=mf_query_parser,
            )
        return issues
