from app.app import create_app, envinfo
#

application_cloudtool = create_app()

if __name__ == '__main__':

    # envinfo()
    application_cloudtool.run(host='0.0.0.0', port=5200)
