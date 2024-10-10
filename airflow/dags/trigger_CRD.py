from datetime import datetime
from airflow import DAG
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import BranchPythonOperator

default_args = {
    'owner': 'airflow',
}

# 분기 함수 정의
def choose_dags(**kwargs):
    """
    DAG 실행 시 전달된 'action' 파라미터에 따라 트리거할 DAG을 결정합니다.
    """
    action = kwargs['dag_run'].conf.get('action', 'none')
    # action은 다음 중 하나: 'create', 'run', 'delete', 'create_run', 'create_run_delete', 'run_delete'
    valid_actions = ['create', 'run', 'delete', 'create_run', 'create_run_delete', 'run_delete']
    if action not in valid_actions:
        return 'no_action'

    if action == 'create':
        return 'trigger_create_one_cluster'
    elif action == 'create_run':
        return 'trigger_create_one_cluster'
    elif action == 'create_run_delete':
        return 'trigger_create_one_cluster'
    elif action == 'run':
        return 'trigger_run_job_one'
    elif action == 'run_delete':
        return 'trigger_run_job_one'
    elif action == 'delete':
        return 'trigger_delete_cluster_one'

with DAG(
        dag_id='master_dag',
        description='Master DAG to trigger other DAGs based on parameters',
        default_args=default_args,
        schedule_interval=None,  # 수동 트리거
        catchup=False,
        start_date=datetime(2023, 1, 1),  # 시작 날짜 지정 (예시)
) as dag:

    # 분기 태스크
    branching = BranchPythonOperator(
        task_id='branching',
        python_callable=choose_dags,
        provide_context=True,
    )

    # TriggerDagRunOperators 정의
    trigger_create_one_cluster = TriggerDagRunOperator(
        task_id='trigger_create_one_cluster',
        trigger_dag_id='create_one_cluster',
        wait_for_completion=True,  # 자식 DAG 완료를 기다림
    )

    trigger_run_job_one = TriggerDagRunOperator(
        task_id='trigger_run_job_one',
        trigger_dag_id='run_job_one',
        wait_for_completion=True,
    )

    trigger_delete_cluster_one = TriggerDagRunOperator(
        task_id='trigger_delete_cluster_one',
        trigger_dag_id='delete_cluster_one',
        wait_for_completion=True,
    )

    # 아무 작업도 하지 않는 태스크
    no_action = EmptyOperator(
        task_id='no_action',
    )

    # 분기 후 태스크 연결
    branching >> trigger_create_one_cluster
    branching >> trigger_run_job_one
    branching >> trigger_delete_cluster_one
    branching >> no_action

    # create -> run
    trigger_create_one_cluster >> trigger_run_job_one
    # create -> run -> delete
    trigger_run_job_one >> trigger_delete_cluster_one
    # run -> delete
    trigger_run_job_one >> trigger_delete_cluster_one
