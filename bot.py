from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from groq import Groq

app = Flask(__name__)

client = Groq(api_key= "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")

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "")
    resp = MessagingResponse()
    msg = resp.message()

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": """Aap ek helpful customer service bot ho ek clothing store ke liye.
                Aap Hindi aur English dono mein baat kar sakte ho.
                Customer jo bhi pooche — stock, price, delivery, size — sab ka jawab do.
                Hamesha friendly aur helpful raho.
                Stock available hai, delivery 3-5 din mein hoti hai, price 500 se 2000 rupaye tak hai."""
            },
            {
                "role": "user",
                "content": incoming_msg
            }
        ],
        model="llama-3.3-70b-versatile",
    )

    reply = chat_completion.choices[0].message.content
    msg.body(reply)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)