# Shopping Query Agent

A full-stack AI-powered shopping assistant application that combines a FastAPI backend with a React frontend. Users can search products, manage shopping carts, and place orders through natural language conversations powered by Google's Gemini AI.

## Features

- 🤖 **AI Shopping Assistant** - Chat-based product discovery and cart management using Gemini
- 🛍️ **Product Catalog** - Search products by query, category, and price
- 🛒 **Smart Cart Management** - Add/remove items with real-time cart updates
- 📦 **Order Management** - Track order history with detailed order information
- 💬 **Conversational Commerce** - Use natural language to find products and checkout
- 🗄️ **SQLite Database** - Persistent product and order storage
- 🎨 **Modern UI** - Beautiful React frontend with responsive design

## Architecture

```
shopping_query_agent/
├── app/                        # FastAPI Backend
│   ├── api/                    # HTTP layer (routes/controllers)
│   │   └── routes/
│   │       ├── cart.py
│   │       ├── chat.py
│   │       ├── health.py
│   │       ├── orders.py
│   │       └── products.py
│   ├── core/                   # Core app config
│   │   └── config.py
│   ├── db/                     # Database session, models, seed
│   │   ├── session.py
│   │   ├── models.py
│   │   └── seed.py
│   ├── schemas/                # Pydantic schemas by domain
│   │   ├── cart.py
│   │   ├── chat.py
│   │   ├── order.py
│   │   └── product.py
│   ├── ai/                     # AI assistant integration
│   │   ├── assistant.py
│   │   └── tools.py
│   ├── services/               # Business logic layer
│   │   ├── cart_service.py
│   │   ├── catalog_service.py
│   │   └── order_service.py
│   └── main.py                 # FastAPI application entrypoint
├── frontend/                 # React TypeScript Frontend
│   ├── src/
│   │   ├── App.tsx          # Main component
│   │   ├── api.ts           # API client
│   │   ├── types.ts         # TypeScript types
│   │   └── styles.css       # Styling
│   └── vite.config.ts
└── requirements.txt          # Python dependencies
```

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM for database operations
- **LangChain** - Framework for AI chains and agents
- **Google Generative AI** - Gemini API integration
- **Pydantic** - Data validation and settings

### Frontend
- **React** - UI library
- **TypeScript** - Type-safe JavaScript
- **Vite** - Fast build tool
- **Fetch API** - HTTP client

## Getting Started

### Prerequisites
- Python 3.9+
- Node.js 18+ & npm
- Google API Key (get one from [Google AI Studio](https://aistudio.google.com/apikey))

### Backend Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create `.env` file in project root:**
   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   GOOGLE_MODEL=gemma-4-31b-it
   DATABASE_URL=sqlite:///./shopping_assistant.db
   ```

3. **Run the FastAPI server:**
   ```bash
   python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
   ```
   Server runs at `http://127.0.0.1:8000`

### Frontend Setup

1. **Install Node dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Create `.env` file in `frontend/` (optional):**
   ```env
   VITE_API_BASE_URL=http://127.0.0.1:8000
   ```

3. **Start development server:**
   ```bash
   npm run dev
   ```
   Frontend runs at `http://localhost:5173`

## Usage

### Through the Web UI
1. Open `http://localhost:5173` in your browser
2. Browse the product catalog or use filters
3. Add items to your cart
4. Chat with the AI assistant to find products or manage your order
5. Proceed to checkout with your shipping address
6. View your order history

### Through the Chat
Ask the assistant natural language queries like:
- "Find me wireless earbuds under $50"
- "Add a USB-C charger to my cart"
- "What's in my cart?"
- "Show me my order history"
- "Checkout to 123 Main Street"

## API Endpoints

### Products
- `GET /products` - Search products with filters
  - Query params: `query`, `category`, `max_price`

### Cart
- `GET /cart/{session_id}` - Get cart for a session
- `POST /cart/{session_id}/items` - Add item to cart
- `DELETE /cart/{session_id}/items/{product_id}` - Remove item from cart

### Orders
- `GET /orders/{session_id}` - Get order history
- `POST /checkout/{session_id}` - Place an order

### Chat
- `POST /chat` - Send message to AI assistant
  - Body: `{ "session_id": "string", "message": "string" }`

### Health
- `GET /health` - Server health check

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_API_KEY` | Google Generative AI API key | Yes |
| `GOOGLE_MODEL` | Gemini model ID | No (default: `gemma-4-31b-it`) |
| `DATABASE_URL` | SQLite database URL | No (default: `sqlite:///./shopping_assistant.db`) |
| `VITE_API_BASE_URL` | Backend API URL for frontend | No (default: `http://127.0.0.1:8000`) |

## Project Structure

### Database Models
- **Product** - Product catalog items
- **CartItem** - Items in user carts
- **Order** - Placed orders
- **OrderItem** - Items in orders

### AI Tools
The assistant has access to these tools:
- `search_catalog` - Find products
- `add_to_cart` - Add items to cart
- `remove_from_cart` - Remove items
- `view_cart` - See cart contents
- `place_order` - Checkout
- `view_order_history` - Get past orders

## Development

### Running Tests
```bash
# Backend tests (if available)
pytest

# Frontend tests (if available)
npm test
```

### Building for Production

**Backend:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
npm run build
npm run preview
```

## Troubleshooting

### "GOOGLE_API_KEY is not configured"
- Ensure `.env` file exists in the project root
- Check that `GOOGLE_API_KEY` is set with a valid API key

### CORS errors from frontend
- Verify backend is running on `http://127.0.0.1:8000`
- Check `VITE_API_BASE_URL` in frontend `.env`

### Database errors
- Delete `shopping_assistant.db` to reset the database
- The database will be recreated with sample data on startup

## License

MIT License - feel free to use this project for your own purposes.

## Contributing

Contributions are welcome! Feel free to submit issues and pull requests.
