
import base64
from geopy.geocoders import Nominatim

def geocode_address(rua, numero, cidade, estado):
    geolocator = Nominatim(user_agent="streamlit-app")
    endereco = f"{rua}, {numero}, {cidade}, {estado}, Brasil"
    try:
        location = geolocator.geocode(endereco)
        return location.latitude, location.longitude if location else (None, None)
    except:
        return None, None

def img_to_data_url(path):
    try:
        with open(path, "rb") as img_file:
            b64_str = base64.b64encode(img_file.read()).decode()
        ext = path.split('.')[-1]
        return f"data:image/{ext};base64,{b64_str}"
    except Exception as e:
        print(f"Erro ao converter imagem: {e}")
        return None
