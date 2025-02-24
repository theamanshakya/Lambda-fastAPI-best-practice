from mangum import Mangum
from src.core.application import create_app

app = create_app()
handler = Mangum(app) 