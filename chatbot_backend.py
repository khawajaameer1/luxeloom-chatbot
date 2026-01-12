"""
Flask Backend for Luxeloom Chatbot
Handles chatbot API endpoints for the website
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import re
import difflib
import random
from typing import Dict, List

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

class LuxeloomChatbot:
    """Web-adapted chatbot for Luxeloom website"""
    
    def __init__(self):
        # Product information database
        self.product_data = {
            "snoopy tote": {
                "name": "Snoopy Tote",
                "price": "PKR 2,125",
                "original_price": "PKR 2,500",
                "discount": "15% OFF",
                "description": "Tote bag for all the snoopy lovers ❤️ started out rough but we got there in the end.",
                "whatsapp": "+92 307 4674619"
            },
            "sunny tote": {
                "name": "Sunny Tote",
                "price": "PKR 2,125",
                "original_price": "PKR 2,500",
                "discount": "15% OFF",
                "description": "Sunny tote! took ages but worth it because she's literally glowing ☀️",
                "whatsapp": "+92 307 4674619"
            },
            "strawberry miffi tote": {
                "name": "Strawberry Miffi Tote",
                "price": "PKR 2,125",
                "original_price": "PKR 2,500",
                "discount": "15% OFF",
                "description": "Watch how this strawberry miffy tote bag came together! love the outcome 🍓",
                "whatsapp": "+92 307 4674619"
            },
            "miffy": {
                "name": "Strawberry Miffi Tote",
                "price": "PKR 2,125",
                "original_price": "PKR 2,500",
                "discount": "15% OFF",
                "description": "Watch how this strawberry miffy tote bag came together! love the outcome 🍓",
                "whatsapp": "+92 307 4674619"
            }
        }
        
        # Conversation state
        self.conversation_history = []
        self.max_history = 5
        
        # Response templates
        self.responses = {
            "greeting": [
                "Hello! 👋 Welcome to Luxeloom! I'm here to help you with our handmade accessories. What would you like to know?",
                "Hi there! ✨ I'm your Luxeloom assistant. How can I help you today?",
                "Welcome to Luxeloom! 🎀 I'm here to assist you with our collection. What can I help you with?",
                "Hello! 🌸 Ready to explore our handmade accessories? What interests you today?"
            ],
            "mission": [
                "At Luxeloom, we believe in shopping with purpose! All proceeds from our handmade accessories support Edhi Foundation, Pakistan's largest welfare organization. When you shop with us, you're making a difference! 💙",
                "Every purchase you make at Luxeloom directly supports Edhi Foundation! We donate 100% of our profits to help families in need. Shop with your heart! ❤️",
                "Our mission is simple: beautiful handmade accessories that give back! All profits go to Edhi Foundation to support those in need across Pakistan. 💝"
            ],
            "care": [
                "Here's how to care for your Luxeloom tote bags:\n\n• Hand wash in cold water only\n• Use mild detergent; avoid bleach\n• Do not machine wash or tumble dry\n• Air dry flat or hang in the shade (avoid direct sunlight)\n• Iron inside out on low heat if needed\n• The hand-painted design may soften over time, adding to its unique character ✨"
            ],
            "ordering": [
                "To place an order, simply message us on WhatsApp at +92 307 4674619! 📱 We'll be happy to help you with your purchase. Thank you for supporting Luxeloom! 💙",
                "Ready to order? Send us a WhatsApp message at +92 307 4674619 and we'll assist you right away! 🌸"
            ],
            "thanks": [
                "You're very welcome! Happy to help! 💙",
                "Anytime! Feel free to ask if you have more questions! ✨",
                "My pleasure! I'm here whenever you need me! 🌸",
                "You're welcome! Thanks for choosing Luxeloom! 💝"
            ],
            "fallback": [
                "I'm not sure I understand that. Could you ask about our products, mission, care instructions, or how to order? 😊",
                "I'm here to help with Luxeloom! Ask me about our products, our mission, care instructions, or ordering! ✨",
                "Let me help you! I can tell you about our tote bags, our mission, care instructions, or how to place an order! 💙"
            ]
        }
    
    def preprocess_text(self, text: str) -> str:
        """Clean and normalize input text"""
        return re.sub(r'[^\w\s]', '', text.lower().strip())
    
    def find_product(self, query: str) -> Dict:
        """Search for product in query"""
        query_lower = self.preprocess_text(query)
        
        # Direct matches
        for key, product in self.product_data.items():
            if key in query_lower:
                return product
        
        # Fuzzy matching for common terms
        product_names = list(self.product_data.keys())
        matches = difflib.get_close_matches(query_lower, product_names, n=1, cutoff=0.4)
        if matches:
            return self.product_data[matches[0]]
        
        return None
    
    def handle_query(self, query: str) -> str:
        """Process user query and generate response"""
        query_proc = self.preprocess_text(query)
        
        # Add to history
        self.conversation_history.append({"role": "user", "content": query})
        if len(self.conversation_history) > self.max_history * 2:
            self.conversation_history = self.conversation_history[-self.max_history * 2:]
        
        # Check for greetings
        if any(word in query_proc for word in ["hello", "hi", "hey", "greetings", "good morning", "good afternoon"]):
            return random.choice(self.responses["greeting"])
        
        # Check for thanks
        if any(word in query_proc for word in ["thanks", "thank you", "thx", "thankyou", "appreciate"]):
            return random.choice(self.responses["thanks"])
        
        # Check for mission/about
        if any(word in query_proc for word in ["mission", "purpose", "about", "story", "edhi", "charity", "donate", "proceeds"]):
            return random.choice(self.responses["mission"])
        
        # Check for care instructions
        if any(word in query_proc for word in ["care", "wash", "clean", "maintain", "instructions", "how to care"]):
            return random.choice(self.responses["care"])
        
        # Check for ordering
        if any(word in query_proc for word in ["order", "buy", "purchase", "how to buy", "how to order", "price", "cost", "where to buy"]):
            product = self.find_product(query)
            if product:
                return f"✨ {product['name']} ✨\n\nPrice: {product['price']} (Original: {product['original_price']}) - {product['discount']}\n\n{product['description']}\n\nTo order, WhatsApp us at {product['whatsapp']}! 📱"
            else:
                return random.choice(self.responses["ordering"]) + "\n\nOur current collection includes:\n• Snoopy Tote - PKR 2,125\n• Sunny Tote - PKR 2,125\n• Strawberry Miffi Tote - PKR 2,125\n\nAll with 15% OFF!"
        
        # Check for specific product queries
        product = self.find_product(query)
        if product:
            return f"✨ {product['name']} ✨\n\nPrice: {product['price']} (Original: {product['original_price']}) - {product['discount']}\n\n{product['description']}\n\nTo order: WhatsApp +92 307 4674619 📱"
        
        # Check for product listings
        if any(word in query_proc for word in ["products", "items", "collection", "what do you have", "what's available", "show me"]):
            return "🌟 Our Handmade Collection 🌟\n\n1. Snoopy Tote - PKR 2,125 (15% OFF)\n2. Sunny Tote - PKR 2,125 (15% OFF)\n3. Strawberry Miffi Tote - PKR 2,125 (15% OFF)\n\nClick 'View Details' on any product or ask me about a specific one! 💙"
        
        # Fallback
        return random.choice(self.responses["fallback"])

# Initialize chatbot
chatbot = LuxeloomChatbot()

@app.route('/')
def index():
    """Health check endpoint"""
    return jsonify({"status": "online", "message": "Luxeloom Chatbot API"})

@app.route('/api/chat', methods=['POST'])
def chat():
    """Main chat endpoint"""
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({"error": "Message is required"}), 400
        
        # Get bot response
        bot_response = chatbot.handle_query(user_message)
        
        return jsonify({
            "response": bot_response,
            "status": "success"
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all products"""
    try:
        products = list(chatbot.product_data.values())
        # Remove duplicates based on name
        seen = set()
        unique_products = []
        for p in products:
            if p['name'] not in seen:
                seen.add(p['name'])
                unique_products.append(p)
        return jsonify({"products": unique_products, "status": "success"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("🌟 Luxeloom Chatbot API Starting...")
    print("📍 API will be available at: http://localhost:5000")
    print("💬 Chat endpoint: http://localhost:5000/api/chat")
    print("\n✨ Make sure to update the frontend API URL if running on different port!")
    app.run(debug=True, host='0.0.0.0', port=5000)
