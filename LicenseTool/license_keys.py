import json, base64, hashlib, hmac, datetime
DEMO_SECRET = b"VS_DEMO_SECRET_CHANGE_ME"

def _mac(payload:bytes)->str:
    return hmac.new(DEMO_SECRET, payload, hashlib.sha256).hexdigest()

def make_license(product:str, customer:str, days:int|None=None)->str:
    lic = {"product": product, "customer": customer, "issued": datetime.date.today().isoformat()}
    if days:
        lic["expiry"] = (datetime.date.today() + datetime.timedelta(days=days)).isoformat()
    payload = json.dumps(lic, separators=(",",":")).encode()
    token = base64.urlsafe_b64encode(payload).decode().rstrip("=")
    sig = _mac(payload)
    return f"{token}.{sig}"

def verify_license(product:str, token:str)->dict:
    try:
        token, sig = token.split(".")
        payload = base64.urlsafe_b64decode(token + "="*((4-len(token)%4)%4))
        if _mac(payload).lower() != sig.lower():
            raise ValueError("Signatur ungültig")
        data = json.loads(payload.decode())
        if data.get("product") != product:
            raise ValueError("Produkt passt nicht")
        exp = data.get("expiry")
        if exp and datetime.date.today() > datetime.date.fromisoformat(exp):
            raise ValueError("Lizenz abgelaufen")
        return data
    except Exception as e:
        raise ValueError(str(e))
