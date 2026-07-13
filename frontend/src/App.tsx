import { useEffect, useMemo, useState, type ChangeEvent, type FormEvent } from 'react';
import { addToCart, chat, checkout, getCart, getOrderHistory, getProducts, removeFromCart } from './api';
import type { Cart, ChatMessage, Order, Product } from './types';

const DEFAULT_SESSION_ID = 'guest-1';

export default function App() {
  const [sessionId, setSessionId] = useState(DEFAULT_SESSION_ID);
  const [query, setQuery] = useState('');
  const [category, setCategory] = useState('');
  const [maxPrice, setMaxPrice] = useState('');
  const [products, setProducts] = useState<Product[]>([]);
  const [cart, setCart] = useState<Cart | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([
    { role: 'assistant', content: 'Ask me to find products, add items to your cart, or checkout.' },
  ]);
  const [chatInput, setChatInput] = useState('');
  const [shippingAddress, setShippingAddress] = useState('221B Baker Street, London');
  const [loadingProducts, setLoadingProducts] = useState(false);
  const [loadingCart, setLoadingCart] = useState(false);
  const [sendingChat, setSendingChat] = useState(false);
  const [placingOrder, setPlacingOrder] = useState(false);
  const [loadingOrderHistory, setLoadingOrderHistory] = useState(false);
  const [orderHistory, setOrderHistory] = useState<Order[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [lastOrder, setLastOrder] = useState<Order | null>(null);

  const totalValue = useMemo(() => cart?.subtotal ?? 0, [cart]);

  async function loadProducts() {
    setLoadingProducts(true);
    setError(null);
    try {
      const data = await getProducts(query, category, maxPrice);
      setProducts(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load products');
    } finally {
      setLoadingProducts(false);
    }
  }

  async function loadCart() {
    setLoadingCart(true);
    setError(null);
    try {
      const data = await getCart(sessionId.trim());
      setCart(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load cart');
    } finally {
      setLoadingCart(false);
    }
  }

  async function loadOrderHistory() {
    setLoadingOrderHistory(true);
    setError(null);
    try {
      const data = await getOrderHistory(sessionId.trim());
      setOrderHistory(data.orders);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load order history');
    } finally {
      setLoadingOrderHistory(false);
    }
  }

  useEffect(() => {
    void loadProducts();
  }, []);

  useEffect(() => {
    void loadCart();
  }, [sessionId]);

  useEffect(() => {
    void loadOrderHistory();
  }, [sessionId]);

  async function handleAdd(productId: number) {
    setError(null);
    setSuccess(null);
    try {
      const data = await addToCart(sessionId, productId, 1);
      setCart(data);
      setSuccess('Item added to cart');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to add item');
    }
  }

  async function handleRemove(productId: number) {
    setError(null);
    try {
      const data = await removeFromCart(sessionId, productId);
      setCart(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to remove item');
    }
  }

  async function handleChatSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!chatInput.trim()) return;

    const userMessage = chatInput.trim();
    setChatInput('');
    setSendingChat(true);
    setError(null);
    setMessages((current) => [...current, { role: 'user', content: userMessage }]);

    try {
      const result = await chat(sessionId, userMessage);
      setMessages((current) => [...current, { role: 'assistant', content: result.reply }]);
      await Promise.all([loadProducts(), loadCart()]);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Chat request failed');
    } finally {
      setSendingChat(false);
    }
  }

  async function handleCheckout() {
    setPlacingOrder(true);
    setError(null);
    setSuccess(null);
    try {
      const order = await checkout(sessionId, shippingAddress);
      setLastOrder(order);
      setSuccess(`Order #${order.order_id} placed successfully`);
      await Promise.all([loadCart(), loadOrderHistory()]);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Checkout failed');
    } finally {
      setPlacingOrder(false);
    }
  }

  return (
    <div className="app-shell">
      <header className="hero">
        <div>
          <p className="eyebrow">Shopping AI Assistant</p>
          <h1>Find products, manage carts, and checkout with AI.</h1>
          <p className="hero-copy">
            A polished React frontend for your FastAPI backend with product search, cart control,
            conversational shopping, and end-to-end order placement.
          </p>
        </div>

        <div className="session-card">
          <label>
            Session ID
            <input value={sessionId} onChange={(event: ChangeEvent<HTMLInputElement>) => setSessionId(event.target.value)} />
          </label>
          <button onClick={loadCart}>Refresh cart</button>
        </div>
      </header>

      <main className="grid-layout">
        <section className="panel panel-wide">
          <div className="section-heading">
            <div>
              <p className="eyebrow">Catalog</p>
              <h2>Browse products</h2>
            </div>
            <button onClick={loadProducts} disabled={loadingProducts}>
              {loadingProducts ? 'Searching...' : 'Search'}
            </button>
          </div>

          <div className="filters">
            <input placeholder="Search products" value={query} onChange={(event: ChangeEvent<HTMLInputElement>) => setQuery(event.target.value)} />
            <input placeholder="Category" value={category} onChange={(event: ChangeEvent<HTMLInputElement>) => setCategory(event.target.value)} />
            <input
              placeholder="Max price"
              value={maxPrice}
              onChange={(event: ChangeEvent<HTMLInputElement>) => setMaxPrice(event.target.value)}
              inputMode="decimal"
            />
          </div>

          <div className="product-grid">
            {products.map((product) => (
              <article className="product-card" key={product.id}>
                <div className="product-topline">
                  <span>{product.category}</span>
                  <span>{product.stock} in stock</span>
                </div>
                <h3>{product.name}</h3>
                <p>{product.description}</p>
                <div className="product-footer">
                  <strong>${product.price.toFixed(2)}</strong>
                  <button onClick={() => handleAdd(product.id)}>Add to cart</button>
                </div>
              </article>
            ))}
          </div>
        </section>

        <aside className="panel">
          <div className="section-heading">
            <div>
              <p className="eyebrow">Cart</p>
              <h2>Your items</h2>
            </div>
            <span className="total-pill">${totalValue.toFixed(2)}</span>
          </div>

          {loadingCart ? (
            <p>Loading cart...</p>
          ) : cart && cart.items.length > 0 ? (
            <div className="cart-list">
              {cart.items.map((item) => (
                <div className="cart-item" key={item.product_id}>
                  <div>
                    <strong>{item.name}</strong>
                    <p>
                      {item.quantity} × ${item.unit_price.toFixed(2)}
                    </p>
                  </div>
                  <div className="cart-item-actions">
                    <span>${item.line_total.toFixed(2)}</span>
                    <button className="ghost" onClick={() => handleRemove(item.product_id)}>
                      Remove
                    </button>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="muted">Your cart is empty. Add something from the catalog or ask the assistant.</p>
          )}

          <label className="stacked">
            Shipping address
            <textarea value={shippingAddress} onChange={(event: ChangeEvent<HTMLTextAreaElement>) => setShippingAddress(event.target.value)} />
          </label>

          <button className="checkout-button" onClick={handleCheckout} disabled={placingOrder}>
            {placingOrder ? 'Placing order...' : 'Checkout now'}
          </button>

          {lastOrder ? (
            <div className="order-card">
              <p className="eyebrow">Last order</p>
              <strong>Order #{lastOrder.order_id}</strong>
              <p>${lastOrder.total_amount.toFixed(2)}</p>
              <small>{lastOrder.status}</small>
            </div>
          ) : null}
        </aside>

        <section className="panel panel-wide">
          <div className="section-heading">
            <div>
              <p className="eyebrow">Order History</p>
              <h2>Your orders</h2>
            </div>
            <button onClick={loadOrderHistory} disabled={loadingOrderHistory}>
              {loadingOrderHistory ? 'Loading...' : 'Refresh'}
            </button>
          </div>

          {orderHistory.length > 0 ? (
            <div className="orders-grid">
              {orderHistory.map((order) => (
                <div className="order-card-detailed" key={order.order_id}>
                  <div className="order-header">
                    <div>
                      <strong>Order #{order.order_id}</strong>
                      <p className="muted">{new Date(order.created_at).toLocaleDateString()}</p>
                    </div>
                    <span className={`status-badge status-${order.status}`}>{order.status}</span>
                  </div>
                  <div className="order-details">
                    <div>
                      <p className="eyebrow">Amount</p>
                      <strong>${order.total_amount.toFixed(2)}</strong>
                    </div>
                    <div>
                      <p className="eyebrow">Items</p>
                      <strong>{order.items.length}</strong>
                    </div>
                    <div>
                      <p className="eyebrow">Address</p>
                      <p className="muted" style={{ fontSize: '0.875rem' }}>{order.shipping_address}</p>
                    </div>
                  </div>
                  <div className="order-items">
                    {order.items.map((item) => (
                      <div className="order-item" key={item.product_id}>
                        <span>{item.name}</span>
                        <span className="muted">
                          {item.quantity}× ${item.unit_price.toFixed(2)}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="muted">No orders yet. Place an order to see your history here.</p>
          )}
        </section>

        <section className="panel panel-chat">
          <div className="section-heading">
            <div>
              <p className="eyebrow">Assistant</p>
              <h2>Chat with Gemini</h2>
            </div>
          </div>

          <div className="chat-stream">
            {messages.map((message, index) => (
              <div className={`bubble ${message.role}`} key={`${message.role}-${index}`}>
                {message.content}
              </div>
            ))}
          </div>

          <form onSubmit={handleChatSubmit} className="chat-form">
            <textarea
              value={chatInput}
              onChange={(event: ChangeEvent<HTMLTextAreaElement>) => setChatInput(event.target.value)}
              placeholder="Example: Find me budget wireless earbuds and add one to my cart"
            />
            <button type="submit" disabled={sendingChat}>
              {sendingChat ? 'Sending...' : 'Send'}
            </button>
          </form>
        </section>
      </main>

      {error ? <div className="toast error">{error}</div> : null}
      {success ? <div className="toast success">{success}</div> : null}
    </div>
  );
}
