import json, base64, hashlib, hmac, datetime
from pathlib import Path

# !!! In Produktion austauschen und NUR im Admin/Licensetool halten !!!
DEMO_SECRET = b"VS_DEMO_SECRET_CHANGE_ME"

def _mac(payload:bytes)->str:
    return hmac.new(DEMO_SECRET, payload, hashlib.sha256).hexdigest()

def _b64e(b:bytes)->str:
    return base64.urlsafe_b64encode(b).decode().rstrip("=")

def _b64d(s:str)->bytes:
    return base64.urlsafe_b64decode(s + "="*((4-len(s)%4)%4))

def make_license(product:str, customer:str, hwid:str, days:int|None=None) -> str:
    lic = {
        "product": product,
        "customer": customer,
        "hwid": hwid,
        "issued": datetime.date.today().isoformat()
    }
    if days and days > 0:
        lic["expiry"] = (datetime.date.today() + datetime.timedelta(days=days)).isoformat()
    payload = json.dumps(lic, separators=(",",":")).encode()
    sig = _mac(payload)
    return f"{_b64e(payload)}.{sig}"

def verify_license(product:str, token:str, current_hwid:str) -> dict:
    try:
        token_part, sig = token.split(".")
        payload = _b64d(token_part)
        if _mac(payload).lower() != sig.lower():
            raise ValueError("Signatur ungültig")
        data = json.loads(payload.decode())
        if data.get("product") != product:
            raise ValueError("Produkt passt nicht")
        if data.get("hwid") != current_hwid:
            raise ValueError("Hardware-ID passt nicht")
        exp = data.get("expiry")
        if exp and datetime.date.today() > datetime.date.fromisoformat(exp):
            raise ValueError("Lizenz abgelaufen")
        return data
    except Exception as e:
        raise ValueError(str(e))

# Variante A: Demo-Lizenz lokal erzeugen
def make_local_demo(product:str, hwid:str, days:int=3) -> str:
    return make_license(product=product, customer="DEMO", hwid=hwid, days=days)
