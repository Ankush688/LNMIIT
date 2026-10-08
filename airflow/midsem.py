from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import dag, task


@dag(dag_id="etl_operators_demo", schedule=None)
def etl_operators_demo():
    @task.python
    def start():
        print("Pipeline Started")

    @task.bash
    def download():
        return 'echo "Downloading file..."'

    process = BashOperator(
        task_id="process",
        bash_command='echo "Processing file..."',
    )

    @task.python
    def finish():
        print("Pipeline finished")

    start() >> download() >> process >> finish()


etl_operators_demo()