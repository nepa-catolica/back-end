from src import create_app

app = create_app()

if __name__ == '__main__':
    app.run(
        debug=True,
        # ssl_context=(
        #     '/home/nepa/ssl-cert-front/certificate.crt',
        #     '/home/nepa/ssl-cert-front/private.key'
        # )
    )