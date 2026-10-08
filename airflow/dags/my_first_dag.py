from airflow.sdk import dag,task

@dag(
    dag_id="Party_DAG"
)

def first_my_dag():


    @task
    def second_task():
        print("fir khana khao")

    @task
    def third_task():
        print("fir movie dekho")

    @task
    def fourth_task():
        print("fir so jao")

    first_task() >> second_task() >> third_task() >> fourth_task()

first_my_dag()