from eve import Eve
from flask import Blueprint

import view

app = Eve()

if __name__ == '__main__':
    view.init_app(app)
    app.run()

