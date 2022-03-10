from flask_pydantic_spec import FlaskPydanticSpec
import app.common.constants as C
apispec = FlaskPydanticSpec('flask',title=C.APP_NAME, version="v1.0", path=C.DOCS_URL)