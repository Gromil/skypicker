#!/bin/bash
wait_for () {
    for _ in `seq 0 100`; do
        (echo > /dev/tcp/$1/$2) >/dev/null 2>&1
        if [[ $? -eq 0 ]]; then
            echo "$1:$2 accepts connections"
            break
        fi
        sleep 1
    done
}
populate_env_variables () {
  set -o allexport
  [[ -f /src/core/.env ]] && source /src/core/.env
  set +o allexport
  echo "env variables are populated"
}
populate_env_variables
case "$PROCESS" in
"LINT")
    wait_for "${DB_HOST}" "${DB_PORT}"
    python manage.py migrate && mypy . && flake8 . && bandit -r . && safety check
    ;;
"DEV_DJANGO")
    wait_for "${DB_HOST}" "${DB_PORT}"
    python manage.py migrate && python manage.py runserver 0.0.0.0:8000
    ;;
"DEV_CELERY")
    wait_for "${BROKER_HOST}" "${BROKER_PORT}"
    celery -A core worker -B --loglevel=INFO --concurrency=1
    ;;
"TEST")
    wait_for "${DB_HOST}" "${DB_PORT}"
    pytest -v --cov . --cov-report term-missing --cov-fail-under=100 \
    --color=yes -n 4 --no-migrations --reuse-db -W error \
    -W ignore::django.utils.deprecation.RemovedInDjango40Warning
    ;;
"DJANGO")
    wait_for "${DB_HOST}" "${DB_PORT}"
    python manage.py collectstatic --noinput && python manage.py migrate
    case "$SERVER" in
    "GUNICORN")
        case "$WORKER_CLASS" in
        "GEVENT")
            gunicorn -c core/gunicorn.py core.wsgi
            ;;
        *)
            echo "NO WORKER_CLASS SPECIFIED!"
            exit 1
            ;;
        esac
        ;;
    *)
        echo "NO SERVER SPECIFIED!"
        exit 1
        ;;
    esac
    ;;
"CELERY")
    wait_for "${BROKER_HOST}" "${BROKER_PORT}"
    case "$NODE" in
    "SCHEDULER")
        celery -A core beat --loglevel=INFO
        ;;
    "CONSUMER")
        celery -A core worker --loglevel=INFO \
        --concurrency=12 --max-tasks-per-child=2048
        ;;
    *)
        echo "NO NODE SPECIFIED!"
        exit 1
        ;;
    esac
    ;;
*)
    echo "NO PROCESS SPECIFIED!"
    exit 1
    ;;
esac
