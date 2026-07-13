import type { Cart, Order, Product } from './types';

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000';

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(init?.headers ?? {}),
    },
    ...init,
  });

  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || `Request failed with status ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export async function getProducts(query: string, category: string, maxPrice: string) {
  const params = new URLSearchParams();
  if (query.trim()) params.set('query', query.trim());
  if (category.trim()) params.set('category', category.trim());
  if (maxPrice.trim()) params.set('max_price', maxPrice.trim());
  const suffix = params.toString() ? `?${params.toString()}` : '';
  return request<Product[]>(`/products${suffix}`);
}

export async function getCart(sessionId: string) {
  return request<Cart>(`/cart/${encodeURIComponent(sessionId)}`);
}

export async function addToCart(sessionId: string, productId: number, quantity: number) {
  return request<Cart>(`/cart/${encodeURIComponent(sessionId)}/items`, {
    method: 'POST',
    body: JSON.stringify({ product_id: productId, quantity }),
  });
}

export async function removeFromCart(sessionId: string, productId: number) {
  return request<Cart>(`/cart/${encodeURIComponent(sessionId)}/items/${productId}`, {
    method: 'DELETE',
  });
}

export async function chat(sessionId: string, message: string) {
  return request<{ session_id: string; reply: string }>(`/chat`, {
    method: 'POST',
    body: JSON.stringify({ session_id: sessionId, message }),
  });
}

export async function checkout(sessionId: string, shippingAddress: string) {
  return request<Order>(`/checkout/${encodeURIComponent(sessionId)}`, {
    method: 'POST',
    body: JSON.stringify({ shipping_address: shippingAddress }),
  });
}

export async function getOrderHistory(sessionId: string) {
  return request<{ orders: Order[] }>(`/orders/${encodeURIComponent(sessionId)}`);
}
