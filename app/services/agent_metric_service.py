from app.models.agent_metric_model import (
    AgentMetric
)


def save_agent_metric(
    db,
    agent_name,
    execution_time
):

    metric = AgentMetric(
        agent_name=agent_name,
        execution_time=execution_time
    )

    db.add(metric)

    db.commit()