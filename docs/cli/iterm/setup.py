"""
Setup development environment on Iterm2
"""
import iterm2


async def main(connection):
    app = await iterm2.async_get_app(connection)
    window = app.current_window
    if window is not None:

        # Create docker tab and start DB and Hasura
        docker_tab = await window.async_create_tab()
        await docker_tab.async_activate()
        docker_session = docker_tab.current_session
        await docker_session.async_send_text('cd /Users/chakshugautam/Work/PDF-Package;\n')
        await docker_session.async_send_text('docker-compose down && docker-compose up -d db graphql-engine\n')

        # Create Server Tab
        server_tab = await window.async_create_tab()
        await server_tab.async_activate()

        # Setup Server Tab
        sess = server_tab.current_session
        await sess.async_send_text('cd /Users/chakshugautam/Work/PDF-Package; source venv/bin/activate; cd src;\n')
        await sess.async_send_text('python3 manage.py runserver_plus\n')

        # Setup Celery Beat Tab
        celery_tab = await sess.async_split_pane(vertical=True)
        await celery_tab.async_send_text('cd /Users/chakshugautam/Work/PDF-Package; source venv/bin/activate; cd src;\n')
        await celery_tab.async_send_text('celery --app=pdf.celery.app beat --loglevel=debug --scheduler django_celery_beat.schedulers:DatabaseScheduler\n')

        # Setup Celery Worker Tab
        worker_tab = await sess.async_split_pane(vertical=False)
        await worker_tab.async_send_text('cd /Users/chakshugautam/Work/PDF-Package; source venv/bin/activate; cd src;\n')
        await worker_tab.async_send_text('celery --app=pdf.celery.app worker --loglevel=debug\n')
    else:
        print("No current window")

iterm2.run_until_complete(main)
