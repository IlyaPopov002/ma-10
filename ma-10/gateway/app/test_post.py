import httpx
from uuid import UUID

# Замените на действительный токен доступа и ID заказа книг
access_token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJEelpTcnhveWJ0TzZxRU1fakI3MzVPdHlzMGd6QnQwYk9BWEVaV1pHbmo4In0.eyJleHAiOjE3MDc5MDc2MTAsImlhdCI6MTcwNzkwNzMxMCwiYXV0aF90aW1lIjoxNzA3OTA2Nzg0LCJqdGkiOiIwZGQ2MzdmYS05YmM4LTQ0ODAtYWVmNS00MWM1YTYzMWJjNzgiLCJpc3MiOiJodHRwOi8vbG9jYWxob3N0OjgwODAvcmVhbG1zL2RlbGl2ZXJ5LXJlYWxtIiwiYXVkIjoiYWNjb3VudCIsInN1YiI6ImVhYTZhMTFiLTJiYTEtNGM4ZC04ZTAzLWU4OTEyZDg1ZGJkOCIsInR5cCI6IkJlYXJlciIsImF6cCI6ImRlbGl2ZXJ5LXNlcnZpY2UtY2xpZW50Iiwic2Vzc2lvbl9zdGF0ZSI6Ijc4ZDFmNzllLTVmMDEtNDA1MC1hYTYxLTNmY2Y2ZjZlNzkyMSIsImFjciI6IjAiLCJhbGxvd2VkLW9yaWdpbnMiOltdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsiZGVmYXVsdC1yb2xlcy1kZWxpdmVyeS1yZWFsbSIsIm9mZmxpbmVfYWNjZXNzIiwiYWRtaW4iLCJ1bWFfYXV0aG9yaXphdGlvbiJdfSwicmVzb3VyY2VfYWNjZXNzIjp7ImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoib3BlbmlkIGVtYWlsIHByb2ZpbGUiLCJzaWQiOiI3OGQxZjc5ZS01ZjAxLTQwNTAtYWE2MS0zZmNmNmY2ZTc5MjEiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwicHJlZmVycmVkX3VzZXJuYW1lIjoiYWRtaW4iLCJlbWFpbCI6ImFkbWluQG1haWwucnUifQ.PcSBO6T6U3Y4En2OT4FwYyTbujz8JNbHUMOqv_Q0sB0ysM_-Y56NFLfM4LgeRhdTnOPt6grzKUdBLaPuhdk476qLGiDAYsYmnqZmgozn-5KhFLU92A6M5MoxAhBksEM0BdhUjtphRcn9JCESDTRkSBQHM3NSlIlun6gLQ0uIWs7_NygUJ1tvPj1C8jhHKID4W6PcrJ7e-LCxeIGDK0LRwdWVnPFJFdJx93jNZO3cWGBrLVxsvMGybjBVA2SCqTXB-uyzE1hcDuvoYzJKXQeHAjiclCpubkiAmbSP73agx_jD8qVLYSctPG7CkcesOpndbTAlHjar7Hbbt0aNEv5lSQ"
# book_id = UUID("2e11fd32-df3a-45da-991e-0128767a18a9")

book_id = UUID("45309954-8e3c-4635-8066-b342f634252c")

url = f"http://localhost:8000/user/order/{book_id}/accepted"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {access_token}"
}


response = httpx.post(url, headers=headers)
if response.status_code == 200:  # Проверьте, что статус ответа  200 OK
    print(response.json())
else:
    print(f"Received status code: {response.status_code}")
    # Посмотрите текст ответа, чтобы увидеть, что вернул сервер
    print(response.text)
